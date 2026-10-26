using System;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Adds the ZWORD_NOTIFICATIONS define when Unity Mobile Notifications (com.unity.mobile.notifications) is
    /// installed, and makes sure iOS does NOT ask for notification permission at launch (Word Z asks only after
    /// the player opts in).
    /// </summary>
    [InitializeOnLoad]
    static class NotificationsDefine
    {
        const string Define = "ZWORD_NOTIFICATIONS";
        static readonly NamedBuildTarget[] Targets = { NamedBuildTarget.Android, NamedBuildTarget.iOS, NamedBuildTarget.Standalone };

        static NotificationsDefine() => EditorApplication.delayCall += Sync;

        [MenuItem("ZWord/Store/Refresh Notifications define")]
        static void Sync()
        {
            var asms = AppDomain.CurrentDomain.GetAssemblies();
            bool present = Find(asms, "Unity.Notifications.NotificationCenter") != null;
            foreach (var t in Targets)
            {
                var defines = PlayerSettings.GetScriptingDefineSymbols(t).Split(';').Where(d => d.Length > 0).ToList();
                if (defines.Contains(Define) == present) continue;
                if (present) defines.Add(Define); else defines.Remove(Define);
                PlayerSettings.SetScriptingDefineSymbols(t, string.Join(";", defines));
                UnityEngine.Debug.Log($"[ZWord] {(present ? "Added" : "Removed")} {Define} for {t.TargetName}.");
            }
            if (present) NoPromptAtLaunch(asms);
        }

        static void NoPromptAtLaunch(System.Reflection.Assembly[] asms)
        {
            try
            {
                var ios = Find(asms, "Unity.Notifications.NotificationSettings+iOSSettings");
                var prop = ios?.GetProperty("RequestAuthorizationOnAppLaunch");
                if (prop == null) return;
                if ((bool)prop.GetValue(null))
                {
                    prop.SetValue(null, false);
                    UnityEngine.Debug.Log("[ZWord] iOS notifications: turned off 'Request Authorization on App Launch' (Word Z asks after opt-in).");
                }
            }
            catch (Exception e) { UnityEngine.Debug.LogWarning("[ZWord] Could not change notification settings: " + e.Message); }
        }

        static Type Find(System.Reflection.Assembly[] asms, string name)
        {
            foreach (var a in asms)
            {
                try { var t = a.GetType(name, false); if (t != null) return t; }
                catch { }
            }
            return null;
        }
    }
}
