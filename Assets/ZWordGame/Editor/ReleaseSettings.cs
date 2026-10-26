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
            PlayerSettings.iOS.appleDeveloperTeamID = AppleTeamId;
            UseCocoaPodsForIOS();

            AssetDatabase.SaveAssets();
            Debug.Log($"[ZWord] Release settings applied: {GameConfig.BundleId} v{GameConfig.Version} ({GameConfig.BuildNumber}).");
        }

        /// <summary>Apple Developer team (Membership page) - Xcode needs it to sign every target, incl. package bundles.</summary>
        public const string AppleTeamId = "N62GU9V2QY";

        /// <summary>
        /// RevenueCat's iOS SDK comes through Swift Package Manager by default (EDM4U 1.2.187+). Its SPM resource bundle
        /// then fails to sign on Build Automation ("RevenueCat_RevenueCat requires a development team"). CocoaPods
        /// doesn't have that problem, so switch EDM4U's iOS Resolver to CocoaPods.
        /// Same as Assets > External Dependency Manager > iOS Resolver > Settings > untick "Swift Package Manager Enabled".
        /// </summary>
        public static void UseCocoaPodsForIOS()
        {
            bool done = false;
            foreach (var asm in System.AppDomain.CurrentDomain.GetAssemblies())
            {
                var t = asm.GetType("Google.IOSResolver", false);
                if (t == null) continue;
                foreach (var p in t.GetProperties(System.Reflection.BindingFlags.Static | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic))
                {
                    if (p.PropertyType != typeof(bool) || !p.CanWrite) continue;
                    var name = p.Name.ToLowerInvariant();
                    if (!name.Contains("swiftpackagemanager") && !name.Contains("spm")) continue;
                    if (!name.Contains("enable")) continue;
                    p.SetValue(null, false);
                    Debug.Log("[ZWord] iOS Resolver: " + p.Name + " = false (use CocoaPods)");
                    done = true;
                }
            }
            if (!done) Debug.LogWarning("[ZWord] Couldn't switch the iOS Resolver to CocoaPods automatically - untick 'Swift Package Manager Enabled' in Assets > External Dependency Manager > iOS Resolver > Settings.");
        }

        /// <summary>
        /// Every iOS/Android build gets a new, always-increasing store build number from the build time
        /// (iOS "20261026.2135", Android minutes since 2026). Apple rejects an upload that reuses a build number,
        /// so this works without any Build Automation setting and without remembering to bump BuildNumber.
        /// </summary>
        class AutoBuildNumber : UnityEditor.Build.IPreprocessBuildWithReport
        {
            public int callbackOrder => -100;
            public void OnPreprocessBuild(UnityEditor.Build.Reporting.BuildReport report)
            {
                var now = System.DateTime.UtcNow;
                var t = report.summary.platform;
                if (t == BuildTarget.iOS)
                {
                    PlayerSettings.iOS.buildNumber = now.ToString("yyyyMMdd") + "." + now.ToString("HHmm");
                    Debug.Log("[ZWord] iOS build number " + PlayerSettings.iOS.buildNumber);
                }
                else if (t == BuildTarget.Android)
                {
                    PlayerSettings.Android.bundleVersionCode = (int)(now - new System.DateTime(2026, 1, 1)).TotalMinutes;
                    Debug.Log("[ZWord] Android version code " + PlayerSettings.Android.bundleVersionCode);
                }
            }
        }

#if UNITY_CLOUD_BUILD
        /// <summary>
        /// Build Automation "Pre-export method": ZWord.EditorTools.ReleaseSettings.PreExport
        /// Uses Build Automation's build counter as the store build number, so every cloud build can be uploaded.
        /// </summary>
        public static void PreExport(UnityEngine.CloudBuild.BuildManifestObject manifest)
        {
            PlayerSettings.iOS.appleDeveloperTeamID = AppleTeamId;
            UseCocoaPodsForIOS();
            // build numbers come from AutoBuildNumber (build time), so they always go up
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
