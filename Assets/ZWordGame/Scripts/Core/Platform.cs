using UnityEngine;

namespace ZWord
{
    /// <summary>Short vibrations (respects the Vibration setting).</summary>
    public static class Haptics
    {
        public static void Light() => Vibrate(18);
        public static void Medium() => Vibrate(35);
        public static void Success() => Vibrate(60);

        static void Vibrate(long ms)
        {
            if (!Save.Haptics) return;
#if UNITY_ANDROID && !UNITY_EDITOR
            try
            {
                using (var player = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
                using (var activity = player.GetStatic<AndroidJavaObject>("currentActivity"))
                using (var vibrator = activity.Call<AndroidJavaObject>("getSystemService", "vibrator"))
                {
                    vibrator?.Call("vibrate", ms);
                }
            }
            catch { }
#elif UNITY_IOS && !UNITY_EDITOR
            if (ms >= 35) Handheld.Vibrate();
#endif
        }

#if UNITY_ANDROID
        // Referencing Handheld.Vibrate makes Unity add the VIBRATE permission to the Android manifest.
        static void EnsureVibratePermission() => Handheld.Vibrate();
#endif
    }

    /// <summary>Share text with the system share sheet (Android); copies to the clipboard elsewhere.</summary>
    public static class Share
    {
        public static void Text(string text)
        {
#if UNITY_ANDROID && !UNITY_EDITOR
            try
            {
                using (var intentClass = new AndroidJavaClass("android.content.Intent"))
                using (var intent = new AndroidJavaObject("android.content.Intent"))
                using (var player = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
                using (var activity = player.GetStatic<AndroidJavaObject>("currentActivity"))
                {
                    intent.Call<AndroidJavaObject>("setAction", intentClass.GetStatic<string>("ACTION_SEND"));
                    intent.Call<AndroidJavaObject>("setType", "text/plain");
                    intent.Call<AndroidJavaObject>("putExtra", intentClass.GetStatic<string>("EXTRA_TEXT"), text);
                    using (var chooser = intentClass.CallStatic<AndroidJavaObject>("createChooser", intent, "Share your score"))
                        activity.Call("startActivity", chooser);
                    return;
                }
            }
            catch { }
#endif
            GUIUtility.systemCopyBuffer = text;
            if (ZWordApp.I != null)
                ZWordApp.Toast(ZWordApp.I.CurrentScreen, "COPIED - PASTE IT ANYWHERE!", new Vector2(0, -300), Palette.Yellow);
        }
    }
}

namespace ZWord
{
    /// <summary>
    /// Insets a full-screen RectTransform by the device safe area (top notch / camera hole, bottom home bar).
    /// Only the vertical insets are applied: the game is portrait and centred in a 1080-wide frame.
    /// </summary>
    public class SafeAreaFitter : UnityEngine.MonoBehaviour
    {
        UnityEngine.Rect last;
        int lastW, lastH;
        float lastParentH;

        void LateUpdate()
        {
            var sa = UnityEngine.Screen.safeArea;
            var parent = transform.parent as UnityEngine.RectTransform;
            if (parent == null) return;
            float ph = parent.rect.height;
            if (sa == last && lastW == UnityEngine.Screen.width && lastH == UnityEngine.Screen.height && UnityEngine.Mathf.Approximately(ph, lastParentH)) return;
            last = sa; lastW = UnityEngine.Screen.width; lastH = UnityEngine.Screen.height; lastParentH = ph;
            if (lastH <= 0 || ph <= 1) return;
            float top = (lastH - sa.yMax) / lastH * ph;
            float bottom = sa.yMin / lastH * ph;
            var rt = (UnityEngine.RectTransform)transform;
            rt.offsetMin = new UnityEngine.Vector2(rt.offsetMin.x, bottom);
            rt.offsetMax = new UnityEngine.Vector2(rt.offsetMax.x, -top);
        }
    }
}
