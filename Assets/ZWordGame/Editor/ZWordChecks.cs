using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEngine;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Automatic checks:
    ///  - ZWord > Tests > Validate All Levels: every baked level is well formed and solvable (no play mode needed).
    ///  - ZWord > Tests > Run Smoke Test: plays through the whole game in play mode (see Testing/SmokeTest.cs).
    /// </summary>
    public static class ZWordChecks
    {
        [MenuItem("ZWord/Tests/Validate All Levels")]
        public static void ValidateLevels()
        {
            var issues = new List<string>();
            var cats = WordData.Categories;
            int checkedLevels = 0;
            for (int c = 0; c < cats.Length; c++)
            {
                for (int l = 0; l < cats[c].LevelCount; l++)
                {
                    var level = LevelDatabase.Get(c, l);
                    string tag = $"{cats[c].Name} level {l + 1}";
                    if (level == null) { issues.Add(tag + ": could not load"); continue; }
                    checkedLevels++;
                    var used = new HashSet<Hex>();
                    var words = new HashSet<string>();
                    foreach (var w in level.Words)
                    {
                        if (!words.Add(w.Word)) issues.Add($"{tag}: '{w.Word}' appears twice");
                        if (w.Word.Length < 3) issues.Add($"{tag}: '{w.Word}' shorter than 3 letters");
                        if (w.Path.Count != w.Word.Length) { issues.Add($"{tag}: '{w.Word}' path length mismatch"); continue; }
                        for (int i = 0; i < w.Path.Count; i++)
                        {
                            if (!level.Letters.TryGetValue(w.Path[i], out char ch) || ch != w.Word[i]) issues.Add($"{tag}: '{w.Word}' letter {i + 1} does not match the board");
                            if (i > 0 && !w.Path[i - 1].IsAdjacent(w.Path[i])) issues.Add($"{tag}: '{w.Word}' path jumps between tiles");
                            if (!used.Add(w.Path[i])) issues.Add($"{tag}: tile used by two words");
                        }
                    }
                    if (used.Count != level.Cells.Count) issues.Add($"{tag}: {level.Cells.Count - used.Count} tiles belong to no word");
                    if (level.TimeLimit < 20f) issues.Add($"{tag}: time limit only {level.TimeLimit:0}s");
                    var solution = Solver.Solve(level, new HashSet<Hex>(level.Cells), level.Words.Select(w => w.Word).ToList());
                    if (solution == null) issues.Add($"{tag}: solver could not solve it");
                }
            }

            var sb = new StringBuilder();
            sb.AppendLine($"Word Z level validation - {System.DateTime.Now:yyyy-MM-dd HH:mm}");
            sb.AppendLine($"{checkedLevels} levels in {cats.Length} categories checked, {issues.Count} issues");
            foreach (var i in issues) sb.AppendLine("  - " + i);
            Directory.CreateDirectory("Logs/SmokeTest");
            File.WriteAllText("Logs/SmokeTest/levels_report.txt", sb.ToString());
            if (issues.Count == 0) Debug.Log($"[ZWord] All {checkedLevels} levels are valid and solvable.");
            else Debug.LogError($"[ZWord] {issues.Count} level issues - see Logs/SmokeTest/levels_report.txt\n" + string.Join("\n", issues.Take(20)));
        }

        [MenuItem("ZWord/Tests/Run Smoke Test (play mode, ~3 min)")]
        public static void RunSmokeTest()
        {
            if (EditorApplication.isPlaying) { Debug.LogWarning("[ZWord] Stop play mode first."); return; }
            PlayerPrefs.SetInt(Testing.SmokeTest.PrefKey, 1);
            PlayerPrefs.Save();
            EditorApplication.isPlaying = true;
        }
    }
}
