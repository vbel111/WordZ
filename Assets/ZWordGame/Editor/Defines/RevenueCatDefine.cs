using System;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Keeps two scripting defines in sync with the installed packages on Android, iOS and Standalone:
    ///   REVENUECAT     - RevenueCat Unity SDK (com.revenuecat.purchases-unity)
    ///   REVENUECAT_UI  - RevenueCat Paywalls + Customer Center (com.revenuecat.purchases-ui-unity)
    /// so the game code compiles with or without them. Lives in its own editor assembly so it still runs when the
    /// game scripts fail to compile.
    /// </summary>
    [InitializeOnLoad]
    static class RevenueCatDefine
    {
        static readonly NamedBuildTarget[] Targets = { NamedBuildTarget.Android, NamedBuildTarget.iOS, NamedBuildTarget.Standalone };

        static RevenueCatDefine() => EditorApplication.delayCall += Sync;

        [MenuItem("ZWord/Store/Refresh RevenueCat defines")]
        static void Sync()
        {
            var asms = AppDomain.CurrentDomain.GetAssemblies();
            bool core = asms.Any(a => a.GetName().Name == "revenuecat.purchases-unity");
            bool ui = HasType(asms, "RevenueCatUI.PaywallsPresenter");
            Apply("REVENUECAT", core);
            Apply("REVENUECAT_UI", core && ui);
        }

        static bool HasType(System.Reflection.Assembly[] asms, string fullName)
        {
            foreach (var a in asms)
            {
                try { if (a.GetType(fullName, false) != null) return true; }
                catch { /* dynamic or unloadable assemblies */ }
            }
            return false;
        }

        static void Apply(string define, bool present)
        {
            foreach (var t in Targets)
            {
                var defines = PlayerSettings.GetScriptingDefineSymbols(t).Split(';').Where(d => d.Length > 0).ToList();
                bool has = defines.Contains(define);
                if (present == has) continue;
                if (present) defines.Add(define); else defines.Remove(define);
                PlayerSettings.SetScriptingDefineSymbols(t, string.Join(";", defines));
                UnityEngine.Debug.Log($"[ZWord] {(present ? "Added" : "Removed")} {define} define for {t.TargetName}.");
            }
        }
    }
}
