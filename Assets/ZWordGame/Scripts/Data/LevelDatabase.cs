using System;
using System.Collections.Generic;
using UnityEngine;

namespace ZWord
{
    // ---------------- Baked file format (Resources/Levels/levels.json) ----------------

    [Serializable]
    public class LevelPack
    {
        public int version = 1;
        public string bakedUtc;
        public List<CategoryPack> categories = new List<CategoryPack>();
    }

    [Serializable]
    public class CategoryPack
    {
        public string name;
        public string color;
        public int group;
        public int cost;
        public List<LevelEntry> levels = new List<LevelEntry>();
    }

    [Serializable]
    public class LevelEntry
    {
        public int[] cells;     // q,r pairs
        public string letters;  // one letter per cell, same order as cells
        public int rot;         // rotation step: 1 = 60 degrees, 3 = 180 degrees, 0 = no rotation
        public float time;      // seconds
        public List<WordEntry> words = new List<WordEntry>();
    }

    [Serializable]
    public class WordEntry
    {
        public string w;
        public int[] p;         // indices into cells, in spelling order
    }

    // ---------------- Source word lists (Content/categories.json, editor only) ----------------

    [Serializable]
    public class CategoryDefFile
    {
        public List<CategoryDef> categories = new List<CategoryDef>();
    }

    [Serializable]
    public class CategoryDef
    {
        public string name;
        public string color;
        public int group;
        public int cost;
        public bool properNouns;
        public string allow;
        public string words;
    }

    /// <summary>Loads the baked levels at runtime. If they're missing, the game falls back to generating levels on the fly.</summary>
    public static class LevelDatabase
    {
        static LevelPack pack;
        static Category[] categories;
        static bool tried;

        public static bool Loaded
        {
            get { EnsureLoaded(); return pack != null; }
        }

        public static Category[] Categories
        {
            get { EnsureLoaded(); return categories; }
        }

        static void EnsureLoaded()
        {
            if (tried) return;
            tried = true;
            var ta = Resources.Load<TextAsset>("Levels/levels");
            if (ta == null)
            {
                Debug.LogWarning("[ZWord] No baked levels found (Resources/Levels/levels.json). Using runtime generation. Run ZWord > Bake Levels.");
                return;
            }
            try
            {
                var p = JsonUtility.FromJson<LevelPack>(ta.text);
                if (p == null || p.categories == null || p.categories.Count == 0) throw new Exception("empty pack");
                pack = p;
                categories = new Category[p.categories.Count];
                for (int i = 0; i < p.categories.Count; i++)
                {
                    var c = p.categories[i];
                    categories[i] = new Category(c.name, c.color, c.group, c.cost, c.levels.Count);
                }
            }
            catch (Exception e)
            {
                Debug.LogError("[ZWord] Could not read baked levels: " + e.Message);
                pack = null;
            }
        }

        public static int LevelCount(int cat) => Loaded ? pack.categories[cat].levels.Count : WordData.FallbackLevels;

        /// <summary>Builds a playable Level from the baked data, or null if unavailable.</summary>
        public static Level Get(int cat, int lvl)
        {
            if (!Loaded || cat < 0 || cat >= pack.categories.Count) return null;
            var levels = pack.categories[cat].levels;
            if (lvl < 0 || lvl >= levels.Count) return null;
            var e = levels[lvl];

            var level = new Level
            {
                CategoryIndex = cat,
                LevelIndex = lvl,
                TimeLimit = e.time,
                RotStep = e.rot
            };
            var cellList = new List<Hex>();
            for (int i = 0; i + 1 < e.cells.Length; i += 2) cellList.Add(new Hex(e.cells[i], e.cells[i + 1]));
            level.Cells = cellList;
            for (int i = 0; i < cellList.Count; i++) level.Letters[cellList[i]] = e.letters[i];
            for (int i = 0; i < e.words.Count; i++)
            {
                var we = e.words[i];
                var path = new List<Hex>();
                foreach (var idx in we.p) path.Add(cellList[idx]);
                level.Words.Add(new PlacedWord
                {
                    Word = we.w,
                    Path = path,
                    Color = Palette.WordColors[i % Palette.WordColors.Length]
                });
            }
            return level;
        }
    }
}
