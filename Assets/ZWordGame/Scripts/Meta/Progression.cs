namespace ZWord
{
    /// <summary>Which level the big PLAY button should start.</summary>
    public static class Progression
    {
        public static void NextLevel(out int cat, out int lvl)
        {
            var cats = WordData.Categories;
            int last = Save.Data.lastCategory;
            if (WordData.IsRegular(last) && Save.Unlocked(last) && Save.Completed(last) < cats[last].LevelCount)
            {
                cat = last;
                lvl = Save.Completed(last);
                return;
            }
            for (int c = 0; c < cats.Length; c++)
            {
                if (WordData.IsRegular(c) && Save.Unlocked(c) && Save.Completed(c) < cats[c].LevelCount)
                {
                    cat = c;
                    lvl = Save.Completed(c);
                    return;
                }
            }
            // everything unlocked is finished: replay the last level of the last category
            cat = WordData.IsRegular(last) ? last : 0;
            lvl = cats[cat].LevelCount - 1;
        }
    }
}
