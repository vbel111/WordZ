#if UNITY_EDITOR
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

namespace ZWord.Testing
{
    /// <summary>
    /// Editor-only automatic walkthrough (menu ZWord > Tests > Run Smoke Test). Plays the tutorial, the first level
    /// of every category, a lost level, the Daily Puzzle and Relax Mode, opens every menu, collects every error or
    /// exception, saves screenshots to Logs/SmokeTest/ and writes Logs/SmokeTest/report.txt.
    /// The player's own progress is snapshotted first and restored at the end.
    /// </summary>
    public class SmokeTest : MonoBehaviour
    {
        public const string PrefKey = "zword_smoketest";
        const string Dir = "Logs/SmokeTest";

        readonly List<string> errors = new List<string>();
        readonly List<string> steps = new List<string>();
        int shot;
        string savedProgress;
        float started;

        void Start()
        {
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir)) File.Delete(f);
            Application.logMessageReceived += OnLog;
            savedProgress = Save.Snapshot();
            started = Time.realtimeSinceStartup;
            StartCoroutine(Run());
        }

        void OnDestroy() => Application.logMessageReceived -= OnLog;

        void OnLog(string msg, string stack, LogType type)
        {
            if (type == LogType.Error || type == LogType.Exception || type == LogType.Assert)
                errors.Add($"[{(steps.Count > 0 ? steps[steps.Count - 1] : "start")}] {type}: {msg}\n{stack}");
        }

        void Step(string s) { steps.Add(s); Debug.Log("[SmokeTest] " + s); }

        static IEnumerator Wait(float s) { yield return new WaitForSecondsRealtime(s); }

        IEnumerator Shot(string name)
        {
            yield return new WaitForSecondsRealtime(0.6f); // let pop-in tweens settle
            ScreenCapture.CaptureScreenshot($"{Dir}/{++shot:00}_{name}.png");
            yield return null;
        }

        static GameScreen Game() => FindAnyObjectByType<GameScreen>();

        IEnumerator SolveAll(float gap = 0.35f)
        {
            for (int guard = 0; guard < 20; guard++)
            {
                var g = Game();
                if (g == null || !g.DebugFindNextWord()) yield break;
                yield return Wait(gap);
            }
        }

        IEnumerator Run()
        {
            var app = ZWordApp.I;
            yield return Wait(3f); // splash -> home / tutorial

            // fresh-player state so the whole flow is reachable
            Save.ResetAll();
            Save.Data.tutorialDone = true;
            Save.Coins = 5000;
            Save.Gems = 100;
            Save.Data.relaxMode = false;

            Step("tutorial");
            app.StartTutorial();
            yield return Shot("tutorial_start");
            yield return SolveAll(1.2f);
            yield return Wait(1.5f);
            yield return Shot("tutorial_done");
            app.ClosePopups();
            yield return Wait(0.8f);

            Step("home");
            app.ShowHome();
            yield return Shot("home");
            app.ClosePopups();

            Step("daily reward popup");
            app.OpenDailyReward();
            yield return Shot("daily_reward");
            app.ClosePopups();

            Step("categories");
            app.ShowCategories();
            yield return Shot("categories");

            var cats = WordData.Categories;
            for (int c = 0; c < cats.Length; c++)
            {
                Step("map + level 1: " + cats[c].Name);
                app.ShowMap(c);
                yield return Wait(0.4f);
                if (c < 3) yield return Shot("map_" + cats[c].Name);
                app.StartLevel(c, 0);
                yield return Wait(0.8f);
                if (c % 5 == 0) yield return Shot("game_" + cats[c].Name);
                yield return SolveAll();
                yield return Wait(1.8f);
                if (c == 0) yield return Shot("level_complete");
            }

            Step("lose a level");
            app.StartLevel(0, 1);
            yield return Wait(0.8f);
            Game()?.DebugRunOutOfTime();
            yield return Wait(0.6f);
            yield return Shot("out_of_time");
            app.ClosePopups(); // give up
            yield return Wait(1.8f);
            yield return Shot("level_failed");

            Step("hints + pause popups");
            app.StartLevel(1, 0);
            yield return Wait(0.8f);
            var hintsCheck = Game();
            if (hintsCheck != null) hintsCheck.SendMessage("OpenHints", SendMessageOptions.DontRequireReceiver);
            yield return Shot("hints");
            app.ClosePopups();
            if (hintsCheck != null) hintsCheck.SendMessage("OpenPause", SendMessageOptions.DontRequireReceiver);
            yield return Shot("pause");
            app.ClosePopups();

            Step("daily puzzle");
            app.StartDailyPuzzle();
            yield return Wait(0.8f);
            yield return Shot("daily_puzzle");
            yield return SolveAll();
            yield return Wait(1.8f);
            yield return Shot("daily_solved");

            Step("relax mode");
            Save.Data.relaxMode = true;
            app.StartLevel(2, 0);
            yield return Wait(0.8f);
            yield return Shot("relax_mode");
            yield return SolveAll();
            yield return Wait(1.8f);
            Save.Data.relaxMode = false;

            Step("shop");
            for (int tab = 0; tab < 3; tab++)
            {
                app.ShowShop(tab);
                yield return Shot("shop_" + tab);
            }
            app.ClosePopups();

            Step("challenges, quests, settings");
            app.ShowChallenges();
            yield return Shot("challenges");
            app.ShowQuests();
            yield return Shot("quests");
            app.OpenSettings();
            yield return Shot("settings");
            app.ClosePopups();

            Step("home again");
            app.ShowHome();
            yield return Shot("home_after");

            Finish();
        }

        void Finish()
        {
            Save.RestoreSnapshot(savedProgress);
            var sb = new StringBuilder();
            sb.AppendLine($"Word Z smoke test - {DateTime.Now:yyyy-MM-dd HH:mm}");
            sb.AppendLine($"Duration: {Time.realtimeSinceStartup - started:0}s, steps: {steps.Count}, screenshots: {shot}");
            sb.AppendLine(errors.Count == 0 ? "RESULT: PASS (no errors or exceptions)" : $"RESULT: FAIL ({errors.Count} errors)");
            sb.AppendLine();
            sb.AppendLine("Steps:");
            foreach (var s in steps) sb.AppendLine("  - " + s);
            if (errors.Count > 0)
            {
                sb.AppendLine();
                sb.AppendLine("Errors:");
                foreach (var e in errors) sb.AppendLine(e).AppendLine();
            }
            File.WriteAllText($"{Dir}/report.txt", sb.ToString());
            Debug.Log($"[SmokeTest] {(errors.Count == 0 ? "PASS" : "FAIL: " + errors.Count + " errors")} - report in {Dir}/report.txt");
            UnityEditor.EditorApplication.isPlaying = false;
        }
    }
}
#endif
