using System;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Adds the REVENUECAT scripting define on Android, iOS and Standalone when the RevenueCat SDK package is in the
    /// project (and removes it when it isn't), so the game code compiles with or without the store SDK.
    /// Lives in its own editor assembly so it still runs when the game scripts fail to compile.
    /// </summary>
    [InitializeOnLoad]
    static class RevenueCatDefine
    {
        const string Define = "REVENUECAT";
        static readonly NamedBuildTarget[] Targets = { NamedBuildTarget.Android, NamedBuildTarget.iOS, NamedBuildTarget.Standalone };

        static RevenueCatDefine() => EditorApplication.delayCall += Sync;

        [MenuItem("ZWord/Store/Refresh RevenueCat define")]
        static void Sync()
        {
            bool present = AppDomain.CurrentDomain.GetAssemblies().Any(a => a.GetName().Name == "revenuecat.purchases-unity");
            foreach (var t in Targets)
            {
                var defines = PlayerSettings.GetScriptingDefineSymbols(t).Split(';').Where(d => d.Length > 0).ToList();
                bool has = defines.Contains(Define);
                if (present == has) continue;
                if (present) defines.Add(Define); else defines.Remove(Define);
                PlayerSettings.SetScriptingDefineSymbols(t, string.Join(";", defines));
                UnityEngine.Debug.Log($"[ZWord] {(present ? "Added" : "Removed")} {Define} define for {t.TargetName}.");
            }
        }
    }
}
