using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// Valid English words (3-8 letters) for bonus words. Baked from the ENABLE list with offensive words removed
    /// (Resources/Words/bonus_words.txt). Parsed on a background thread at startup.
    /// </summary>
    public static class WordDictionary
    {
        static HashSet<string> words;
        static Task loading;

        public static bool Ready => words != null;
        public static int Count => words?.Count ?? 0;

        public static void Preload()
        {
            if (loading != null) return;
            var ta = Resources.Load<TextAsset>("Words/bonus_words");
            if (ta == null)
            {
                Debug.LogWarning("[ZWord] Bonus dictionary missing (Resources/Words/bonus_words.txt). Bonus words are disabled until levels are baked with enable1.txt present.");
                loading = Task.CompletedTask;
                return;
            }
            string text = ta.text; // must be read on the main thread
            Resources.UnloadAsset(ta);
            loading = Task.Run(() =>
            {
                var set = new HashSet<string>(StringComparer.Ordinal);
                int start = 0;
                for (int i = 0; i <= text.Length; i++)
                {
                    if (i == text.Length || text[i] == '\n' || text[i] == '\r')
                    {
                        if (i > start) set.Add(text.Substring(start, i - start).Trim().ToUpperInvariant());
                        start = i + 1;
                    }
                }
                set.Remove("");
                words = set;
            });
        }

        public static bool Contains(string word)
        {
            if (words == null || string.IsNullOrEmpty(word)) return false;
            return words.Contains(word.ToUpperInvariant());
        }
    }
}
