namespace ZWord
{
    /// <summary>Kept only for compatibility with older code. Use <see cref="AudioManager"/> instead. Safe to delete.</summary>
    public static class Sfx
    {
        public static void Blip(int index) => AudioManager.Letter(index);
        public static void Click() => AudioManager.Click();
        public static void Success() => AudioManager.Success();
        public static void Error() => AudioManager.Error();
        public static void Win() => AudioManager.Win();
        public static void Lose() => AudioManager.Lose();
    }
}
