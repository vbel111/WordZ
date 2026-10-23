using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// In-app purchases through RevenueCat (coin packs, gem packs, the one-time Supporter Pack).
    ///
    /// The RevenueCat code only compiles when the package is installed: the editor adds the REVENUECAT scripting
    /// define automatically once it finds the SDK (see Editor/Defines). Without it - or in the Editor - the shop
    /// still works: in the Editor purchases are simulated so you can test the flow; in a build without the SDK
    /// the buttons say the store is unavailable.
    /// </summary>
    public static class Store
    {
        public static event Action Changed;

        /// <summary>True once the real store is configured and talking to RevenueCat.</summary>
        public static bool Available { get; private set; }

        static readonly Dictionary<string, string> prices = new Dictionary<string, string>();
        static bool busy;

        public static IEnumerable<string> AllProductIds =>
            GameConfig.CoinPacks.Select(p => p.id).Concat(GameConfig.GemPacks.Select(p => p.id)).Append(GameConfig.SupporterId);

        /// <summary>Localised price from the store, or the fallback shown before prices load.</summary>
        public static string Price(string id, string fallback) => prices.TryGetValue(id, out var p) && !string.IsNullOrEmpty(p) ? p : fallback;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics() { Available = false; busy = false; prices.Clear(); Changed = null; }

        // ------------------------------------------------------------------ setup

        public static void Init(MonoBehaviour runner)
        {
#if REVENUECAT && !UNITY_EDITOR
            runner.StartCoroutine(InitRevenueCat());
#endif
        }

#if REVENUECAT
        static Purchases rc;

        static IEnumerator InitRevenueCat()
        {
            string key = Application.platform == RuntimePlatform.IPhonePlayer ? GameConfig.RevenueCatAppleKey : GameConfig.RevenueCatGoogleKey;
            if (string.IsNullOrEmpty(key) || key.StartsWith("REPLACE"))
            {
                Debug.LogWarning("[ZWord] RevenueCat API key missing in GameConfig - store disabled.");
                yield break;
            }
            // The SDK sends its callbacks to this GameObject by name, so it lives at the root.
            var go = new GameObject("ZWordPurchases");
            UnityEngine.Object.DontDestroyOnLoad(go);
            rc = go.AddComponent<Purchases>();
            rc.useRuntimeSetup = true;
            yield return null; // let Purchases.Start() pick the native wrapper first

            rc.Configure(Purchases.PurchasesConfiguration.Builder.Init(key).Build());
            Available = true;

            rc.GetProducts(AllProductIds.ToArray(), (products, error) =>
            {
                if (error != null) { Debug.LogWarning("[ZWord] Store products: " + error.Message); return; }
                foreach (var p in products) prices[p.Identifier] = p.PriceString;
                Changed?.Invoke();
            }, "inapp");

            // Supporter Pack is non-consumable: re-apply it if this account already owns it (new phone, reinstall)
            rc.GetCustomerInfo((info, error) => { if (error == null) ApplyOwned(info); });
        }

        static void ApplyOwned(Purchases.CustomerInfo info)
        {
            if (info?.AllPurchasedProductIdentifiers == null) return;
            if (info.AllPurchasedProductIdentifiers.Contains(GameConfig.SupporterId) && !Save.Data.supporter) Grant(GameConfig.SupporterId, true);
        }
#endif

        // ------------------------------------------------------------------ buying

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
                    Debug.LogWarning("[ZWord] Purchase failed: " + result.Error.Message);
                    done?.Invoke(false, "PURCHASE FAILED - PLEASE TRY AGAIN");
                    return;
                }
                Grant(id, false);
                done?.Invoke(true, null);
            }, "inapp");
#else
            done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW");
#endif
        }

        /// <summary>Restores the non-consumable Supporter Pack (required by Apple).</summary>
        public static void Restore(Action<bool, string> done)
        {
#if UNITY_EDITOR
            done?.Invoke(true, Save.Data.supporter ? "PURCHASES RESTORED" : "NOTHING TO RESTORE");
#elif REVENUECAT
            if (!Available) { done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW"); return; }
            rc.RestorePurchases((info, error) =>
            {
                if (error != null) { done?.Invoke(false, "RESTORE FAILED - PLEASE TRY AGAIN"); return; }
                bool had = Save.Data.supporter;
                ApplyOwned(info);
                done?.Invoke(true, Save.Data.supporter && !had ? "SUPPORTER PACK RESTORED" : "PURCHASES RESTORED");
            });
#else
            done?.Invoke(false, "STORE NOT AVAILABLE RIGHT NOW");
#endif
        }

        // ------------------------------------------------------------------ rewards

        static void Grant(string id, bool restored)
        {
            foreach (var p in GameConfig.CoinPacks)
                if (p.id == id) { Save.Coins += p.coins; Finish(); return; }
            foreach (var p in GameConfig.GemPacks)
                if (p.id == id) { Save.Gems += p.gems; Finish(); return; }
            if (id == GameConfig.SupporterId)
            {
                if (Save.Data.supporter && !restored) { Finish(); return; }
                Save.Data.supporter = true;
                Save.Coins += GameConfig.SupporterCoins;
                Save.Gems += GameConfig.SupporterGems;
                foreach (Booster b in Enum.GetValues(typeof(Booster)))
                    if (b != Booster.Pause) Save.SetBooster(b, Save.GetBooster(b) + GameConfig.SupporterBoosters);
                Finish();
            }
        }

        static void Finish()
        {
            Save.Write();
            Changed?.Invoke();
        }
    }
}
