using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Callbacks;
using UnityEngine;

namespace ZWord.EditorTools
{
    /// <summary>
    /// One click store-ready Player Settings (ZWord > Apply Release Settings) and the iOS Info.plist keys
    /// App Store Connect asks about. Unity Build Automation builds with whatever is saved in ProjectSettings,
    /// so run this once, check the values, then commit ProjectSettings.
    /// </summary>
    public static class ReleaseSettings
    {
        [MenuItem("ZWord/Apply Release Settings")]
        public static void Apply()
        {
            if (GameConfig.BundleId.Contains("yourstudio"))
                Debug.LogWarning("[ZWord] Set GameConfig.BundleId to your real bundle id (the one registered in App Store Connect / Play Console) and run this again.");

            PlayerSettings.companyName = GameConfig.CompanyName;
            PlayerSettings.productName = GameConfig.GameName;
            PlayerSettings.bundleVersion = GameConfig.Version;
            PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.Android, GameConfig.BundleId);
            PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.iOS, GameConfig.BundleId);

            // portrait only
            PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait;
            PlayerSettings.allowedAutorotateToPortrait = true;
            PlayerSettings.allowedAutorotateToPortraitUpsideDown = false;
            PlayerSettings.allowedAutorotateToLandscapeLeft = false;
            PlayerSettings.allowedAutorotateToLandscapeRight = false;

            // Android: IL2CPP, 64-bit (+32-bit for older phones), Play-ready bundle
            PlayerSettings.SetScriptingBackend(NamedBuildTarget.Android, ScriptingImplementation.IL2CPP);
            PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64 | AndroidArchitecture.ARMv7;
            PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel26;
            PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;
            PlayerSettings.Android.bundleVersionCode = GameConfig.BuildNumber;
            EditorUserBuildSettings.buildAppBundle = true;

            // iOS
            PlayerSettings.iOS.targetOSVersionString = "15.0";
            PlayerSettings.iOS.buildNumber = GameConfig.BuildNumber.ToString();
            PlayerSettings.iOS.appleEnableAutomaticSigning = false; // Build Automation signs with your .p12 + profile

            AssetDatabase.SaveAssets();
            Debug.Log($"[ZWord] Release settings applied: {GameConfig.BundleId} v{GameConfig.Version} ({GameConfig.BuildNumber}).");
        }

#if UNITY_CLOUD_BUILD
        /// <summary>
        /// Build Automation "Pre-export method": ZWord.EditorTools.ReleaseSettings.PreExport
        /// Uses Build Automation's build counter as the store build number, so every cloud build can be uploaded.
        /// </summary>
        public static void PreExport(UnityEngine.CloudBuild.BuildManifestObject manifest)
        {
            var n = manifest.GetValue<string>("buildNumber");
            if (int.TryParse(n, out int build) && build > 0)
            {
                PlayerSettings.iOS.buildNumber = build.ToString();
                PlayerSettings.Android.bundleVersionCode = build;
                Debug.Log("[ZWord] Cloud build number " + build);
            }
        }
#endif

#if UNITY_IOS
        /// <summary>No custom encryption -> App Store Connect stops asking about export compliance on every upload.</summary>
        [PostProcessBuild(100)]
        public static void OnPostprocessBuild(BuildTarget target, string path)
        {
            if (target != BuildTarget.iOS) return;
            var plistPath = System.IO.Path.Combine(path, "Info.plist");
            var plist = new UnityEditor.iOS.Xcode.PlistDocument();
            plist.ReadFromFile(plistPath);
            plist.root.SetBoolean("ITSAppUsesNonExemptEncryption", false);
            System.IO.File.WriteAllText(plistPath, plist.WriteToString());
        }
#endif
    }
}
