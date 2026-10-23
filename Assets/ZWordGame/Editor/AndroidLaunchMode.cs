#if UNITY_ANDROID
using System.IO;
using System.Xml;
using UnityEditor.Android;

namespace ZWord.EditorTools
{
    /// <summary>
    /// RevenueCat: the Android activity must use launchMode standard or singleTop, otherwise a purchase can be
    /// cancelled when the player switches to a banking app to approve it. Unity generates singleTask, so patch it.
    /// </summary>
    class AndroidLaunchMode : IPostGenerateGradleAndroidProject
    {
        public int callbackOrder => 999;

        public void OnPostGenerateGradleAndroidProject(string path)
        {
            var file = Path.Combine(path, "src", "main", "AndroidManifest.xml");
            if (!File.Exists(file)) return;
            const string ns = "http://schemas.android.com/apk/res/android";
            var doc = new XmlDocument();
            doc.Load(file);
            bool changed = false;
            foreach (XmlElement act in doc.GetElementsByTagName("activity"))
            {
                var mode = act.GetAttribute("launchMode", ns);
                if (mode == "singleTask" || mode == "singleInstance")
                {
                    act.SetAttribute("launchMode", ns, "singleTop");
                    changed = true;
                }
            }
            if (changed) doc.Save(file);
        }
    }
}
#endif
