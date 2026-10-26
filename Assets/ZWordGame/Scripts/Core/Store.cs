using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// In-app purchases through RevenueCat:
    ///   * consumables (coin packs, gem packs, the "consumable" product) - granted on every purchase
    ///   * the one-time Supporter Pack (non-consumable, restorable)
    ///   * Word Z Pro - the "wordz_pro" entitlement, sold through a RevenueCat Paywall (subscription or lifetime,
    ///     whatever the current Offering contains) and managed with RevenueCat's Customer Center
    ///
    /// Best practices followed here:
    ///   * access is decided by the ENTITLEMENT ("wordz_pro"), never by product ids, so products and prices can
    ///     change in the RevenueCat dashboard without an app update;
    ///   * CustomerInfo is refreshed on start, after every purchase / restore / paywall / Customer Center, and when
    ///     the app returns to the foreground (renewals, refunds and expirations show up without a restart);
    ///   * the last known Pro state is cached in the save so the game works offline;
    ///   * shop prices come from the store (localised), with GameConfig fallbacks.
    ///
    /// Compiles with or without the SDKs: REVENUECAT / REVENUECAT_UI are added by Editor/Defines when the
    /// packages are installed. In the Unity Editor purchases are simulated (the native SDK can't run there).
    /// </summary>
    public static class Store
    {
        public static event Action Changed;

        /// <summary>True once the real store is configured and talking to RevenueCat.</summary>
        public static bool Available { get; private set; }

        /// <summary>Has the "wordz_pro" entitlement (cached in the save; refreshed from RevenueCat).</summary>
        public static bool IsPro => GameConfig.ProEnabled && Save.Data != null && Save.Data.pro;

        /// <summary>When Pro ends or renews (null = lifetime or unknown).</summary>
        public static DateTime? ProExpires { get; private set; }

        static readonly Dictionary<string, string> prices = new Dictionary<string, string>();
        static bool busy;

        public static IEnumerable<string> AllProductIds =>
            GameConfig.CoinPacks.Select(p => p.id).Concat(GameConfig.GemPacks.Select(p => p.id))
                .Append(GameConfig.SupporterId).Append(GameConfig.ConsumableId);

        /// <summary>Localised price from the store, or the fallback shown before prices load.</summary>
        public static string Price(string id, string fallback) => prices.TryGetValue(id, out var p) && !string.IsNullOrEmpty(p) ? p : fallback;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics() { Available = false; busy = false; prices.Clear(); Changed = null; ProExpires = null; }

        static string ApiKey
        {
            get
            {
                if (GameConfig.UseRevenueCatTestStore) return GameConfig.RevenueCatTestKey;
                return Application.platform == RuntimePlatform.IPhonePlayer ? GameConfig.RevenueCatAppleKey : GameConfig.RevenueCatGoogleKey;
            }
        }

        // ================================================================== setup

        public static void Init(MonoBehaviour runner)
        {
#if REVENUECAT && !UNITY_EDITOR
            runner.StartCoroutine(InitRevenueCat());
#endif
        }

        /// <summary>Call when the app returns to the foreground: picks up renewals, refunds and expirations.</summary>
        public static void OnResume()
        {
#if REVENUECAT && !UNITY_EDITOR
            RefreshCustomerInfo();
#endif
        }

        /// <summary>Re-reads the player's purchases/entitlements from RevenueCat.</summary>
        public static void RefreshCustomerInfo(Action done = null)
        {
#if REVENUECAT && !UNITY_EDITOR
            if (rc == null || !Available) { done?.Invoke(); return; }
            rc.GetCustomerInfo((info, error) =>
            {
                if (error != null) Debug.LogWarning("[ZWord] CustomerInfo: " + error.Message);
                else ApplyCustomerInfo(info);
                done?.Invoke();
            });
#else
            done?.Invoke();
#endif
        }

#if REVENUECAT
        static Purchases rc;

        static IEnumerator InitRevenueCat()
        {
            string key = ApiKey;
            if (string.IsNullOrEmpty(key) || key.StartsWith("REPLACE"))
            {
                Debug.LogWarning("[ZWord] RevenueCat API key missing in GameConfig - store disabled.");
                yield break;
            }
            if (GameConfig.UseRevenueCatTestStore)
                Debug.LogWarning("[ZWord] Using the RevenueCat TEST STORE key - set GameConfig.UseRevenueCatTestStore = false before App Store / Play review.");

            // The SDK sends its callbacks to this GameObject by name, so it lives at the root.
            var go = new GameObject("ZWordPurchases");
            UnityEngine.Object.DontDestroyOnLoad(go);
            rc = go.AddComponent<Purchases>();
            rc.useRuntimeSetup = true;
            yield return null; // let Purchases.Start() pick the native wrapper first

            if (Debug.isDebugBuild) rc.SetDebugLogsEnabled(true);
            // Anonymous app user id for now; add .SetAppUserId(...) here once player accounts exist.
            rc.Configure(Purchases.PurchasesConfiguration.Builder.Init(key).Build());
            Available = true;

            LoadPrices();
            RefreshCustomerInfo();
        }

        static void LoadPrices()
        {
            rc.GetProducts(AllProductIds.ToArray(), (products, error) =>
            {
                if (error != null) { Debug.LogWarning("[ZWord] Store products: " + error.Message); return; }
                foreach (var p in products) prices[p.Identifier] = p.PriceString;
                Changed?.Invoke();
            }, "inapp");
        }

        /// <summary>The single place that turns RevenueCat's CustomerInfo into game state.</summary>
        static void ApplyCustomerInfo(Purchases.CustomerInfo info)
        {
            if (info == null) return;
            bool changed = false;

            // Word Z Pro is decided by the entitlement, not by product ids
            // (only while Pro is switched on - otherwise a coin pack attached to the entitlement must not unlock Pro perks)
            bool pro = GameConfig.ProEnabled && info.Entitlements != null && info.Entitlements.Active != null && info.Entitlements.Active.ContainsKey(GameConfig.ProEntitlement);
            ProExpires = pro ? (DateTime?)info.Entitlements.Active[GameConfig.ProEntitlement].ExpirationDate : null;
            if (Save.Data.pro != pro) { Save.Data.pro = pro; changed = true; }

            // Supporter Pack is non-consumable: re-apply it on a new phone / reinstall
            if (info.AllPurchasedProductIdentifiers != null && info.AllPurchasedProductIdentifiers.Contains(GameConfig.SupporterId) && !Save.Data.supporter)
            {
                Grant(GameConfig.SupporterId, true);
                changed = false; // Grant already saved + notified
            }
            if (changed) Finish();
        }
#endif

        // ================================================================== buying

        /// <param name="done">(success, message) - message is null on success or user cancel.</param>
        public static void Buy(string id, Action<bool, string> done)
        {
            if (busy) return;
#if UNITY_EDITOR
            // Editor: simulate a successful purchase so the flow can be tested without a device.
            Debug.Log("[ZWord] (Editor) simulated purchase of " + id);
            Grant(id, false);
            done?.Invoke(true, null);
#elif REVENUECAT
            if (!Available) { done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW"); return; }
            busy = true;
            rc.PurchaseProduct(id, result =>
            {
                busy = false;
                if (result.UserCancelled) { done?.Invoke(false, null); return; }
                if (result.Error != null)
                {
                    Debug.LogWarning($"[ZWord] Purchase of {id} failed: {result.Error.Message}");
                    done?.Invoke(false, FriendlyError(result.Error.Message));
                    return;
                }
                Grant(id, false);
                RefreshCustomerInfo();
                done?.Invoke(true, null);
            }, "inapp");
#else
            done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW");
#endif
        }

        /// <summary>Restores the Supporter Pack and Pro (Apple requires a restore button).</summary>
        public static void Restore(Action<bool, string> done)
        {
#if UNITY_EDITOR
            done?.Invoke(true, Save.Data.supporter || IsPro ? "PURCHASES RESTORED" : "NOTHING TO RESTORE");
#elif REVENUECAT
            if (!Available) { done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW"); return; }
            rc.RestorePurchases((info, error) =>
            {
                if (error != null) { done?.Invoke(false, "RESTORE FAILED - PLEASE TRY AGAIN"); return; }
                bool had = Save.Data.supporter || IsPro;
                ApplyCustomerInfo(info);
                bool has = Save.Data.supporter || IsPro;
                done?.Invoke(true, has && !had ? "PURCHASES RESTORED" : has ? "ALL PURCHASES ARE ACTIVE" : "NOTHING TO RESTORE");
            });
#else
            done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW");
#endif
        }

        static string FriendlyError(string raw)
        {
            if (string.IsNullOrEmpty(raw)) return "PURCHASE FAILED - PLEASE TRY AGAIN";
            var m = raw.ToLowerInvariant();
            if (m.Contains("network") || m.Contains("offline") || m.Contains("internet")) return "NO CONNECTION - TRY AGAIN LATER";
            if (m.Contains("not allowed") || m.Contains("permission")) return "PURCHASES ARE TURNED OFF ON THIS DEVICE";
            if (m.Contains("pending") || m.Contains("deferred")) return "PAYMENT PENDING - WE'LL ADD IT WHEN IT CLEARS";
            if (m.Contains("already")) return "YOU ALREADY OWN THIS";
            return "PURCHASE FAILED - PLEASE TRY AGAIN";
        }

        // ================================================================== Pro: paywall + Customer Center

        /// <summary>
        /// Shows the RevenueCat Paywall of the current Offering (designed in the dashboard) unless the player already
        /// has "wordz_pro". done(message): a short toast text, or null.
        /// </summary>
        public static async void ShowPaywall(Action<string> done = null)
        {
#if UNITY_EDITOR
            // The paywall UI is native-only; in the Editor this toggles Pro so the perks can be tested.
            Save.Data.pro = !Save.Data.pro;
            Finish();
            done?.Invoke(Save.Data.pro ? "(EDITOR) PRO ON - THE PAYWALL SHOWS ON DEVICES" : "(EDITOR) PRO OFF");
            await System.Threading.Tasks.Task.CompletedTask;
#elif REVENUECAT && REVENUECAT_UI
            if (!Available) { done?.Invoke("STORE NOT AVAILABLE RIGHT NOW"); return; }
            try
            {
                var result = await RevenueCatUI.PaywallsPresenter.PresentIfNeeded(requiredEntitlementIdentifier: GameConfig.ProEntitlement);
                switch (result.Result)
                {
                    case RevenueCatUI.PaywallResultType.Purchased:
                        RefreshCustomerInfo(() => done?.Invoke(IsPro ? "WELCOME TO WORD Z PRO!" : "THANK YOU!"));
                        break;
                    case RevenueCatUI.PaywallResultType.Restored:
                        RefreshCustomerInfo(() => done?.Invoke(IsPro ? "PRO RESTORED" : "NOTHING TO RESTORE"));
                        break;
                    case RevenueCatUI.PaywallResultType.NotPresented:
                        RefreshCustomerInfo(() => done?.Invoke(IsPro ? "YOU ARE ALREADY PRO" : "PRO IS NOT AVAILABLE RIGHT NOW"));
                        break;
                    case RevenueCatUI.PaywallResultType.Error:
                        done?.Invoke("SOMETHING WENT WRONG - PLEASE TRY AGAIN");
                        break;
                    default: // Cancelled
                        done?.Invoke(null);
                        break;
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning("[ZWord] Paywall: " + e.Message);
                done?.Invoke("SOMETHING WENT WRONG - PLEASE TRY AGAIN");
            }
#else
            done?.Invoke("STORE NOT AVAILABLE RIGHT NOW");
            await System.Threading.Tasks.Task.CompletedTask;
#endif
        }

        /// <summary>RevenueCat Customer Center: manage / cancel / restore / request a refund for Pro.</summary>
        public static async void ShowCustomerCenter(Action<string> done = null)
        {
#if UNITY_EDITOR
            done?.Invoke("(EDITOR) CUSTOMER CENTER SHOWS ON DEVICES");
            await System.Threading.Tasks.Task.CompletedTask;
#elif REVENUECAT && REVENUECAT_UI
            if (!Available) { done?.Invoke("STORE NOT AVAILABLE RIGHT NOW"); return; }
            try
            {
                // No callbacks used (they arrive on a background thread); we refresh once it closes.
                await RevenueCatUI.CustomerCenterPresenter.Present();
            }
            catch (Exception e)
            {
                Debug.LogWarning("[ZWord] Customer Center: " + e.Message);
            }
            RefreshCustomerInfo(() => done?.Invoke(null));
#else
            done?.Invoke("STORE NOT AVAILABLE RIGHT NOW");
            await System.Threading.Tasks.Task.CompletedTask;
#endif
        }

        /// <summary>Pro players manage their subscription; everyone else sees the paywall.</summary>
        public static void OpenPro(Action<string> done = null)
        {
            if (IsPro) ShowCustomerCenter(done);
            else ShowPaywall(done);
        }

        // ================================================================== rewards

        static void Grant(string id, bool restored)
        {
            foreach (var p in GameConfig.CoinPacks)
                if (p.id == id) { Save.Coins += p.coins; Finish(); return; }
            foreach (var p in GameConfig.GemPacks)
                if (p.id == id) { Save.Gems += p.gems; Finish(); return; }
            if (id == GameConfig.ConsumableId) { Save.Coins += GameConfig.ConsumableCoins; Finish(); return; }
            if (id == GameConfig.SupporterId)
            {
                if (Save.Data.supporter && !restored) { Finish(); return; }
                Save.Data.supporter = true;
                Save.Coins += GameConfig.SupporterCoins;
                Save.Gems += GameConfig.SupporterGems;
                foreach (Booster b in Enum.GetValues(typeof(Booster)))
                    if (b != Booster.Pause) Save.SetBooster(b, Save.GetBooster(b) + GameConfig.SupporterBoosters);
                Finish();
                return;
            }
            Debug.LogWarning("[ZWord] Purchased unknown product " + id + " - add it to GameConfig.");
        }

        static void Finish()
        {
            Save.Write();
            Changed?.Invoke();
        }
    }
}
