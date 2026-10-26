using System;
using UnityEngine;
#if ZWORD_NOTIFICATIONS
using Unity.Notifications;
#endif

namespace ZWord
{
    /// <summary>
    /// Opt-in local reminders (Unity Mobile Notifications, unified API). Nothing is asked at launch: the player
    /// turns them on from the soft popup after a Daily Puzzle win or from Settings. At most one reminder a day,
    /// for the next 3 days, re-planned every time the app goes to the background.
    /// </summary>
    public static class Reminders
    {
        const int Hour = 18, Minute = 30;
        static bool initialised;

        public static bool Supported
        {
            get
            {
#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
                return true;
#else
                return false;
#endif
            }
        }

        static void Init()
        {
#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
            if (initialised) return;
            var args = NotificationCenterArgs.Default;
            args.AndroidChannelId = "daily";
            args.AndroidChannelName = "Daily puzzle";
            args.AndroidChannelDescription = "A reminder when a new Daily Puzzle is ready";
            NotificationCenter.Initialize(args);
            initialised = true;
#endif
        }

        /// <summary>Asks the system for permission, then turns reminders on. done(true) when allowed.</summary>
        public static void Enable(Action<bool> done)
        {
#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
            Init();
            Tween.Run(EnableCo(done));
#else
            Save.Data.remindersOn = true;
            Save.Write();
            done?.Invoke(true);
#endif
        }

#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
        static System.Collections.IEnumerator EnableCo(Action<bool> done)
        {
            var request = NotificationCenter.RequestPermission();
            if (request.Status == NotificationsPermissionStatus.RequestPending) yield return request;
            bool ok = request.Status == NotificationsPermissionStatus.Granted;
            Save.Data.remindersOn = ok;
            Save.Write();
            if (ok) Reschedule();
            done?.Invoke(ok);
        }
#endif

        public static void Disable()
        {
            Save.Data.remindersOn = false;
            Save.Write();
#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
            Init();
            NotificationCenter.CancelAllScheduledNotifications();
#endif
        }

        /// <summary>Plans the next reminders (call when the app is paused / quits). Safe to call often.</summary>
        public static void Reschedule()
        {
#if ZWORD_NOTIFICATIONS && (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
            if (!Save.Data.remindersOn) return;
            try
            {
                Init();
                NotificationCenter.CancelAllScheduledNotifications();
                NotificationCenter.CancelAllDeliveredNotifications();
                var now = DateTime.Now;
                for (int day = 0; day < 3; day++)
                {
                    var when = DateTime.Today.AddDays(day).AddHours(Hour).AddMinutes(Minute);
                    if (when <= now.AddMinutes(30)) continue;
                    if (day == 0 && DailyPuzzle.DoneToday) continue;   // already played today
                    var (title, text) = Message(day);
                    var n = new Notification { Title = title, Text = text };
                    NotificationCenter.ScheduleNotification(n, new NotificationDateTimeSchedule(when));
                }
            }
            catch (Exception e) { Debug.LogWarning("[ZWord] Reminders: " + e.Message); }
#endif
        }

        static (string, string) Message(int day)
        {
            int streak = DailyPuzzle.Streak;
            int ev = WordData.ActiveEvent();
            if (streak >= 2 && day <= 1) return ("Keep your streak alive!", "Your " + streak + "-day Daily Puzzle streak is waiting for today's board.");
            if (ev >= 0 && day == 1) return ("Event on now!", "The " + WordData.Categories[ev].Name + " event is live - earn its badge before it ends.");
            if (DailyRewards.CanClaim || day > 0) return ("New Daily Puzzle", "A fresh honeycomb is ready - plus your daily reward.");
            return ("New Daily Puzzle", "A fresh honeycomb is ready. Can you find every word?");
        }
    }
}
