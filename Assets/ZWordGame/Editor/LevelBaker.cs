using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEngine;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Turns Content/categories.json into Resources/Levels/levels.json (25 levels per category) and,
    /// when Content/enable1.txt is present, Resources/Words/bonus_words.txt.
    /// Every word is checked (A-Z, 3-8 letters, profanity list, dictionary unless allowed) and every
    /// level is validated after baking. Runs automatically when the source files change.
    /// </summary>
    [InitializeOnLoad]
    public static class LevelBaker
    {
        const string ContentDir = "Assets/ZWordGame/Content";
        const string CategoriesPath = ContentDir + "/categories.json";
        const string DictPath = ContentDir + "/enable1.txt";
        const string ReportPath = ContentDir + "/bake_report.txt";
        const string LevelsDir = "Assets/ZWordGame/Resources/Levels";
        const string LevelsPath = LevelsDir + "/levels.json";
        const string WordsDir = "Assets/ZWordGame/Resources/Words";
        const string WordsPath = WordsDir + "/bonus_words.txt";

        static LevelBaker()
        {
            EditorApplication.delayCall += AutoBake;
        }

        static void AutoBake()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(CategoriesPath)) return;

            bool dictExists = File.Exists(DictPath);
            bool need = !File.Exists(LevelsPath)
                        || File.GetLastWriteTimeUtc(CategoriesPath) > File.GetLastWriteTimeUtc(LevelsPath)
                        || (dictExists && (!File.Exists(WordsPath) || File.GetLastWriteTimeUtc(DictPath) > File.GetLastWriteTimeUtc(WordsPath)));
            if (need) Bake();
        }

        [MenuItem("ZWord/Bake Levels")]
        public static void BakeMenu()
        {
            if (Bake()) EditorUtility.DisplayDialog("ZWord", "Levels baked. See Content/bake_report.txt for details.", "OK");
            else EditorUtility.DisplayDialog("ZWord", "Bake failed. See the Console and Content/bake_report.txt.", "OK");
        }

        [MenuItem("ZWord/Validate Baked Levels")]
        public static void ValidateMenu()
        {
            var ta = AssetDatabase.LoadAssetAtPath<TextAsset>(LevelsPath);
            if (ta == null) { Debug.LogError("[ZWord] No levels.json to validate."); return; }
            var pack = JsonUtility.FromJson<LevelPack>(ta.text);
            var errors = new List<string>();
            foreach (var c in pack.categories)
                for (int i = 0; i < c.levels.Count; i++)
                    Validate(c.name, i, c.levels[i], errors);
            if (errors.Count == 0) Debug.Log($"[ZWord] All {pack.categories.Sum(c => c.levels.Count)} levels are valid.");
            else Debug.LogError("[ZWord] Level problems:\n" + string.Join("\n", errors));
        }

        // ---------------------------------------------------------------------------------

        static bool Bake()
        {
            var report = new StringBuilder();
            report.AppendLine("ZWord bake report " + DateTime.Now);
            try
            {
                var defs = JsonUtility.FromJson<CategoryDefFile>(File.ReadAllText(CategoriesPath));
                if (defs?.categories == null || defs.categories.Count == 0) throw new Exception("categories.json has no categories");

                HashSet<string> dict = null;
                if (File.Exists(DictPath))
                {
                    dict = new HashSet<string>(File.ReadAllLines(DictPath)
                        .Select(l => l.Trim().ToUpperInvariant())
                        .Where(l => l.Length > 0));
                    report.AppendLine($"Dictionary: {dict.Count} words");
                }
                else report.AppendLine("Dictionary: MISSING (Content/enable1.txt). Words were not spell-checked and bonus words are disabled.");

                var pack = new LevelPack { bakedUtc = DateTime.UtcNow.ToString("o") };
                var errors = new List<string>();

                foreach (var def in defs.categories)
                {
                    var words = CleanWords(def, dict, report);
                    var cp = new CategoryPack { name = def.name, color = def.color, group = def.group, cost = def.cost };
                    BakeCategory(def.name, words, cp, report, errors);
                    pack.categories.Add(cp);
                }

                for (int ci = 0; ci < pack.categories.Count; ci++)
                    for (int li = 0; li < pack.categories[ci].levels.Count; li++)
                        Validate(pack.categories[ci].name, li, pack.categories[ci].levels[li], errors);

                if (errors.Count > 0)
                {
                    report.AppendLine().AppendLine("ERRORS:");
                    foreach (var e in errors) report.AppendLine("  " + e);
                    File.WriteAllText(ReportPath, report.ToString());
                    Debug.LogError("[ZWord] Bake failed:\n" + string.Join("\n", errors));
                    return false;
                }

                Directory.CreateDirectory(LevelsDir);
                File.WriteAllText(LevelsPath, JsonUtility.ToJson(pack));

                if (dict != null)
                {
                    Directory.CreateDirectory(WordsDir);
                    var bonus = dict.Where(w => w.Length >= 3 && w.Length <= 8 && w.All(ch => ch >= 'A' && ch <= 'Z') && !Profanity.IsBlocked(w))
                        .OrderBy(w => w, StringComparer.Ordinal);
                    File.WriteAllText(WordsPath, string.Join("\n", bonus));
                }

                int total = pack.categories.Sum(c => c.levels.Count);
                report.AppendLine().AppendLine($"OK: {pack.categories.Count} categories, {total} levels.");
                File.WriteAllText(ReportPath, report.ToString());
                AssetDatabase.Refresh();
                Debug.Log($"[ZWord] Baked {total} levels in {pack.categories.Count} categories" +
                          (dict == null ? " (no dictionary: add Content/enable1.txt to spell-check and enable bonus words)." : "."));
                return true;
            }
            catch (Exception e)
            {
                report.AppendLine("EXCEPTION: " + e);
                File.WriteAllText(ReportPath, report.ToString());
                Debug.LogError("[ZWord] Bake failed: " + e);
                return false;
            }
        }

        static List<string> CleanWords(CategoryDef def, HashSet<string> dict, StringBuilder report)
        {
            var allow = new HashSet<string>((def.allow ?? "").Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries)
                .Select(w => w.Trim().ToUpperInvariant()));
            var result = new List<string>();
            var seen = new HashSet<string>();
            foreach (var raw in (def.words ?? "").Split(new[] { ' ', ',', '\n', '\r', '\t' }, StringSplitOptions.RemoveEmptyEntries))
            {
                var w = raw.Trim().ToUpperInvariant();
                if (!seen.Add(w)) { report.AppendLine($"  [{def.name}] duplicate: {w}"); continue; }
                if (w.Length < 3 || w.Length > 8 || !w.All(ch => ch >= 'A' && ch <= 'Z'))
                { report.AppendLine($"  [{def.name}] skipped (must be 3-8 letters A-Z): {w}"); continue; }
                if (Profanity.IsBlocked(w)) { report.AppendLine($"  [{def.name}] skipped (blocked word): {w}"); continue; }
                if (dict != null && !def.properNouns && !allow.Contains(w) && !dict.Contains(w))
                { report.AppendLine($"  [{def.name}] skipped (not in dictionary): {w}"); continue; }
                result.Add(w);
            }
            report.AppendLine($"[{def.name}] {result.Count} usable words");
            return result;
        }

        static void BakeCategory(string name, List<string> pool, CategoryPack cp, StringBuilder report, List<string> errors)
        {
            var usage = pool.ToDictionary(w => w, w => 0);
            var prev = new HashSet<string>();
            var ramp = BoardShapes.Ramp;

            for (int li = 0; li < ramp.Length; li++)
            {
                var step = ramp[li];
                var cells = BoardShapes.Cells(step.Columns);
                var rng = new System.Random(StableHash(name) * 31 + li * 7919);
                int minW = step.MinWords, maxW = step.MaxWords, lo = step.MinLen, hi = step.MaxLen;
                List<string> chosen = null;
                List<List<Hex>> paths = null;

                for (int attempt = 0; attempt < 300 && paths == null; attempt++)
                {
                    chosen = PickWords(pool, usage, cells.Count, minW, maxW, lo, hi, rng, prev);
                    if (chosen == null)
                    {
                        // relax the rules: shorter words, then fewer words, then longer words
                        if (lo > 3) lo--;
                        else if (minW > 1) minW--;
                        hi = Math.Min(8, hi + 1);
                        maxW++;
                        continue;
                    }
                    chosen = chosen.OrderByDescending(w => w.Length).ToList();
                    paths = LevelGenerator.Tile(cells, chosen.Select(w => w.Length).ToList(), rng);
                }

                if (paths == null)
                {
                    errors.Add($"{name} level {li + 1}: could not build a board. Add more words (especially 3-5 letters).");
                    continue;
                }

                foreach (var w in chosen) usage[w]++;
                prev = new HashSet<string>(chosen);

                var index = new Dictionary<Hex, int>();
                for (int i = 0; i < cells.Count; i++) index[cells[i]] = i;
                var letters = new char[cells.Count];
                var entry = new LevelEntry
                {
                    cells = cells.SelectMany(h => new[] { h.Q, h.R }).ToArray(),
                    rot = BoardShapes.RotationStep(cells),
                    time = BoardShapes.TimeFor(cells.Count)
                };
                for (int wi = 0; wi < chosen.Count; wi++)
                {
                    var we = new WordEntry { w = chosen[wi], p = paths[wi].Select(h => index[h]).ToArray() };
                    for (int k = 0; k < we.p.Length; k++) letters[we.p[k]] = chosen[wi][k];
                    entry.words.Add(we);
                }
                entry.letters = new string(letters);
                cp.levels.Add(entry);
            }

            int unused = usage.Count(kv => kv.Value == 0);
            report.AppendLine($"[{name}] {cp.levels.Count} levels, {unused} words unused, max reuse {(usage.Count > 0 ? usage.Values.Max() : 0)}");
        }

        static List<string> PickWords(List<string> pool, Dictionary<string, int> usage, int total, int minW, int maxW,
            int lo, int hi, System.Random rng, HashSet<string> avoid)
        {
            // least-used words first (random among ties), never repeat the previous level's words
            var cand = pool.Where(w => w.Length >= lo && w.Length <= hi && !avoid.Contains(w))
                .OrderBy(_ => rng.Next())
                .OrderBy(w => usage[w])
                .ToList();
            var chosen = new List<string>();
            return Pick(cand, 0, total, minW, maxW, lo, chosen) ? chosen : null;
        }

        static bool Pick(List<string> cand, int start, int remaining, int minW, int maxW, int lo, List<string> chosen)
        {
            if (remaining == 0) return chosen.Count >= minW;
            if (chosen.Count >= maxW || remaining < lo) return false;
            for (int i = start; i < cand.Count; i++)
            {
                var w = cand[i];
                if (w.Length > remaining) continue;
                // no word inside another (e.g. CAR and CART) so players aren't confused
                if (chosen.Any(x => x.Contains(w) || w.Contains(x))) continue;
                chosen.Add(w);
                if (Pick(cand, i + 1, remaining - w.Length, minW, maxW, lo, chosen)) return true;
                chosen.RemoveAt(chosen.Count - 1);
            }
            return false;
        }

        static void Validate(string cat, int li, LevelEntry e, List<string> errors)
        {
            string id = $"{cat} level {li + 1}";
            int n = e.cells.Length / 2;
            if (e.letters == null || e.letters.Length != n) { errors.Add(id + ": letters/cells mismatch"); return; }
            var cells = new List<Hex>();
            for (int i = 0; i < n; i++) cells.Add(new Hex(e.cells[2 * i], e.cells[2 * i + 1]));
            if (new HashSet<Hex>(cells).Count != n) errors.Add(id + ": duplicate cells");
            var covered = new bool[n];
            foreach (var w in e.words)
            {
                if (w.p.Length != w.w.Length) { errors.Add($"{id}: path length wrong for {w.w}"); continue; }
                for (int k = 0; k < w.p.Length; k++)
                {
                    int idx = w.p[k];
                    if (idx < 0 || idx >= n) { errors.Add($"{id}: bad index in {w.w}"); break; }
                    if (covered[idx]) errors.Add($"{id}: cell used twice ({w.w})");
                    covered[idx] = true;
                    if (e.letters[idx] != w.w[k]) errors.Add($"{id}: letter mismatch in {w.w}");
                    if (k > 0 && !cells[w.p[k - 1]].IsAdjacent(cells[idx])) errors.Add($"{id}: {w.w} path not adjacent");
                }
            }
            if (covered.Any(c => !c)) errors.Add(id + ": not every cell is used");
        }

        static int StableHash(string s)
        {
            unchecked
            {
                int h = (int)2166136261;
                foreach (char c in s) h = (h ^ c) * 16777619;
                return h & 0x7fffffff;
            }
        }
    }
}
