using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace ZWord
{
    /// <summary>Axial coordinate of a flat-top hexagon.</summary>
    public readonly struct Hex : IEquatable<Hex>
    {
        public readonly int Q, R;
        public Hex(int q, int r) { Q = q; R = r; }

        public static readonly Hex[] Dirs =
        {
            new Hex(1, 0), new Hex(1, -1), new Hex(0, -1), new Hex(-1, 0), new Hex(-1, 1), new Hex(0, 1)
        };

        public Hex Neighbor(int i) => new Hex(Q + Dirs[i].Q, R + Dirs[i].R);
        public bool IsAdjacent(Hex o) { int dq = o.Q - Q, dr = o.R - R; return Dirs.Any(d => d.Q == dq && d.R == dr); }
        public int Ring => (Math.Abs(Q) + Math.Abs(R) + Math.Abs(-Q - R)) / 2;

        /// <summary>Rotate 60 degrees around the origin, k times.</summary>
        public Hex Rotate(int k)
        {
            int q = Q, r = R;
            k = ((k % 6) + 6) % 6;
            for (int i = 0; i < k; i++) { int nq = -r, nr = q + r; q = nq; r = nr; }
            return new Hex(q, r);
        }

        public bool Equals(Hex o) => Q == o.Q && R == o.R;
        public override bool Equals(object obj) => obj is Hex h && Equals(h);
        public override int GetHashCode() => Q * 397 ^ R;
        public override string ToString() => $"({Q},{R})";
    }

    public class PlacedWord
    {
        public string Word;
        public List<Hex> Path;
        public bool Found;
        public int Revealed;
        public Color Color;
    }

    public class Level
    {
        public int CategoryIndex, LevelIndex;
        public Category Category => WordData.Categories[CategoryIndex];
        public List<Hex> Cells = new List<Hex>();
        public Dictionary<Hex, char> Letters = new Dictionary<Hex, char>();
        public List<PlacedWord> Words = new List<PlacedWord>();
        public float TimeLimit;
        public int RotStep = 1; // 1 = 60deg, 3 = 180deg, 0 = no rotation
    }

    /// <summary>
    /// Builds a level by choosing category words whose letters exactly fill a hexagonal board,
    /// then tiling the board with snake-like paths (one per word) through adjacent hexes.
    /// </summary>
    public static class LevelGenerator
    {
        public const int BoardRadius = 2; // 19 cells

        public static List<Hex> BoardCells(int radius)
        {
            var list = new List<Hex>();
            for (int q = -radius; q <= radius; q++)
            for (int r = Math.Max(-radius, -q - radius); r <= Math.Min(radius, -q + radius); r++)
                list.Add(new Hex(q, r));
            return list;
        }

        public static Level Generate(int cat, int lvl)
        {
            var category = WordData.Categories[cat];
            var rng = new System.Random(cat * 1009 + lvl * 7919 + 13);
            var cells = BoardCells(BoardRadius);
            int total = cells.Count;

            // Larger word count (shorter words) in early levels, longer words later.
            int minWords = lvl < 4 ? 4 : 3;
            int maxWords = lvl < 4 ? 5 : 4;

            for (int attempt = 0; attempt < 300; attempt++)
            {
                var words = PickWords(category.Words, total, minWords, maxWords, rng);
                if (words == null) { minWords = 3; maxWords = 6; continue; }
                words = words.OrderByDescending(w => w.Length).ToList();

                var paths = Tile(cells, words.Select(w => w.Length).ToList(), rng);
                if (paths == null) continue;

                var level = new Level
                {
                    CategoryIndex = cat,
                    LevelIndex = lvl,
                    Cells = cells,
                    TimeLimit = Mathf.Max(75f, 170f - lvl * 9f - (category.Group - 1) * 20f)
                };
                for (int i = 0; i < words.Count; i++)
                {
                    var pw = new PlacedWord { Word = words[i], Path = paths[i], Color = Palette.WordColors[i % Palette.WordColors.Length] };
                    for (int j = 0; j < pw.Path.Count; j++) level.Letters[pw.Path[j]] = pw.Word[j];
                    level.Words.Add(pw);
                }
                return level;
            }
            throw new Exception($"Could not generate level {lvl} for {category.Name}. Add more words to the category.");
        }

        static List<string> PickWords(string[] pool, int total, int minWords, int maxWords, System.Random rng)
        {
            var shuffled = pool.OrderBy(_ => rng.Next()).ToArray();
            var chosen = new List<string>();
            return Pick(shuffled, 0, total, minWords, maxWords, chosen) ? chosen : null;
        }

        static bool Pick(string[] pool, int start, int remaining, int minWords, int maxWords, List<string> chosen)
        {
            if (remaining == 0) return chosen.Count >= minWords;
            if (chosen.Count >= maxWords || remaining < 3) return false;
            for (int i = start; i < pool.Length; i++)
            {
                var w = pool[i];
                if (w.Length > remaining) continue;
                chosen.Add(w);
                if (Pick(pool, i + 1, remaining - w.Length, minWords, maxWords, chosen)) return true;
                chosen.RemoveAt(chosen.Count - 1);
            }
            return false;
        }

        // ---------- Tiling the board with paths ----------

        /// <summary>Partitions the cells into adjacent-cell paths with the given lengths (null if it can't).</summary>
        public static List<List<Hex>> Tile(List<Hex> cells, List<int> lengths, System.Random rng)
        {
            var free = new HashSet<Hex>(cells);
            var result = new List<List<Hex>>();
            int budget = 40000;
            return TileRec(free, lengths, 0, result, rng, ref budget) ? result : null;
        }

        static bool TileRec(HashSet<Hex> free, List<int> lengths, int wi, List<List<Hex>> result, System.Random rng, ref int budget)
        {
            if (wi == lengths.Count) return free.Count == 0;
            if (--budget < 0) return false;

            var starts = free.OrderBy(_ => rng.Next()).ToList();
            foreach (var s in starts)
            {
                var path = new List<Hex> { s };
                free.Remove(s);
                if (Extend(free, path, lengths, wi, result, rng, ref budget)) return true;
                free.Add(s);
                if (budget < 0) return false;
            }
            return false;
        }

        static bool Extend(HashSet<Hex> free, List<Hex> path, List<int> lengths, int wi, List<List<Hex>> result, System.Random rng, ref int budget)
        {
            if (--budget < 0) return false;
            if (path.Count == lengths[wi])
            {
                if (!ComponentsOk(free, lengths, wi + 1)) return false;
                result.Add(new List<Hex>(path));
                if (TileRec(free, lengths, wi + 1, result, rng, ref budget)) return true;
                result.RemoveAt(result.Count - 1);
                return false;
            }
            var last = path[path.Count - 1];
            var dirs = Enumerable.Range(0, 6).OrderBy(_ => rng.Next()).ToArray();
            foreach (var d in dirs)
            {
                var n = last.Neighbor(d);
                if (!free.Contains(n)) continue;
                free.Remove(n);
                path.Add(n);
                if (Extend(free, path, lengths, wi, result, rng, ref budget)) return true;
                path.RemoveAt(path.Count - 1);
                free.Add(n);
                if (budget < 0) return false;
            }
            return false;
        }

        /// <summary>Prune: every connected empty region must be fillable by the remaining word lengths.</summary>
        static bool ComponentsOk(HashSet<Hex> free, List<int> lengths, int from)
        {
            if (free.Count == 0) return from == lengths.Count;
            int minLen = int.MaxValue;
            for (int i = from; i < lengths.Count; i++) minLen = Math.Min(minLen, lengths[i]);
            var seen = new HashSet<Hex>();
            var stack = new Stack<Hex>();
            foreach (var c in free)
            {
                if (seen.Contains(c)) continue;
                int size = 0;
                stack.Push(c); seen.Add(c);
                while (stack.Count > 0)
                {
                    var h = stack.Pop(); size++;
                    for (int d = 0; d < 6; d++)
                    {
                        var n = h.Neighbor(d);
                        if (free.Contains(n) && seen.Add(n)) stack.Push(n);
                    }
                }
                if (size < minLen) return false;
                if (!SubsetSumPossible(size, lengths, from)) return false;
            }
            return true;
        }

        static bool SubsetSumPossible(int target, List<int> lengths, int from)
        {
            var can = new bool[target + 1];
            can[0] = true;
            for (int i = from; i < lengths.Count; i++)
                for (int s = target; s >= lengths[i]; s--)
                    if (can[s - lengths[i]]) can[s] = true;
            return can[target];
        }
    }

    /// <summary>Finds disjoint paths that spell the remaining words on the unused cells.</summary>
    public static class Solver
    {
        public static List<List<Hex>> Solve(Level level, HashSet<Hex> free, List<string> words)
        {
            var result = new List<List<Hex>>();
            int budget = 60000;
            var ordered = words.OrderByDescending(w => w.Length).ToList();
            if (!Rec(level, free, ordered, 0, result, ref budget)) return null;
            // map back to original order
            var map = new List<List<Hex>>();
            var used = new bool[ordered.Count];
            foreach (var w in words)
            {
                for (int i = 0; i < ordered.Count; i++)
                    if (!used[i] && ordered[i] == w) { used[i] = true; map.Add(result[i]); break; }
            }
            return map;
        }

        static bool Rec(Level level, HashSet<Hex> free, List<string> words, int wi, List<List<Hex>> result, ref int budget)
        {
            if (wi == words.Count) return free.Count == 0;
            var word = words[wi];
            var starts = free.Where(h => level.Letters[h] == word[0]).ToList();
            foreach (var s in starts)
            {
                var path = new List<Hex> { s };
                free.Remove(s);
                if (Walk(level, free, words, wi, path, result, ref budget)) return true;
                free.Add(s);
                if (budget < 0) return false;
            }
            return false;
        }

        static bool Walk(Level level, HashSet<Hex> free, List<string> words, int wi, List<Hex> path, List<List<Hex>> result, ref int budget)
        {
            if (--budget < 0) return false;
            var word = words[wi];
            if (path.Count == word.Length)
            {
                result.Add(new List<Hex>(path));
                if (Rec(level, free, words, wi + 1, result, ref budget)) return true;
                result.RemoveAt(result.Count - 1);
                return false;
            }
            var last = path[path.Count - 1];
            char next = word[path.Count];
            for (int d = 0; d < 6; d++)
            {
                var n = last.Neighbor(d);
                if (!free.Contains(n) || level.Letters[n] != next) continue;
                free.Remove(n); path.Add(n);
                if (Walk(level, free, words, wi, path, result, ref budget)) return true;
                path.RemoveAt(path.Count - 1); free.Add(n);
            }
            return false;
        }
    }
}
