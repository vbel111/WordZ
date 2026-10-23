using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>
    /// First-launch tutorial on a tiny 7-tile board: drag a word, rotate the board, use a hint, finish the level.
    /// A hand pointer shows each move and a speech card explains it. Skippable; shown once.
    /// </summary>
    public class Tutorial : MonoBehaviour
    {
        enum Step { Drag, Rotate, Hint, Finish, Done }

        GameScreen gs;
        RectTransform root, hand, card;
        TMP_Text cardText;
        Step step;
        PlacedWord first, second;
        RectTransform tapTarget;
        float stepStart;

        public static void Begin(RectTransform root)
        {
            var level = BuildLevel();
            var gs = GameScreen.BuildCustom(root, level, true);
            var t = root.gameObject.AddComponent<Tutorial>();
            t.gs = gs;
            t.root = root;
            t.first = level.Words[0];
            t.second = level.Words[1];
            t.Setup();
        }

        /// <summary>"WORD" and "FUN" tiled over the 7 cells of a radius-1 hex board.</summary>
        static Level BuildLevel()
        {
            var cells = LevelGenerator.BoardCells(1);
            List<List<Hex>> paths = null;
            for (int seed = 3; paths == null && seed < 200; seed++)
                paths = LevelGenerator.Tile(cells, new List<int> { 4, 3 }, new System.Random(seed));
            var level = new Level { CategoryIndex = 0, LevelIndex = 0, TimeLimit = 999f, RotStep = 1 };
            level.Cells.AddRange(cells);
            string[] words = { "WORD", "FUN" };
            for (int i = 0; i < 2; i++)
            {
                for (int k = 0; k < words[i].Length; k++) level.Letters[paths[i][k]] = words[i][k];
                level.Words.Add(new PlacedWord { Word = words[i], Path = paths[i], Color = Palette.WordColors[i % Palette.WordColors.Length] });
            }
            return level;
        }

        void Setup()
        {
            gs.WordFound += OnWordFound;
            gs.Rotated += () => { if (step == Step.Rotate) Next(Step.Hint); };
            gs.BoosterUsed += _ => { if (step == Step.Hint) Next(Step.Finish); };
            gs.TutorialWin = Finish;
            gs.TutorialSkip = Skip;
            ZWordApp.I.OnBack = Skip;

            // speech card under the HUD
            card = UI.Rect("TutorialCard", root).Place(new Vector2(0.5f, 1), new Vector2(0, -520), new Vector2(900, 150));
            UI.Img(card, Sprites.Rounded, new Color(0.42f, 0.25f, 0.06f, 0.35f), "Shadow", 1.6f).rectTransform.Stretch(0, -10, 0, 10);
            UI.Img(card, Sprites.Rounded, Skin.Cream, "Face", 1.6f).rectTransform.Stretch();
            cardText = UI.Label(card, "", 40, Skin.Ink, TextAnchor.MiddleCenter, false);
            cardText.rectTransform.Stretch(30, 10, 30, 10);
            cardText.textWrappingMode = TextWrappingModes.Normal;

            // skip button
            var skip = UI.Chunky(root, new Vector2(170, 76), Skin.Wood, "SKIP", 34, Skip);
            ((RectTransform)skip.transform).Place(new Vector2(1, 0), new Vector2(-110, 360), new Vector2(170, 76));

            // hand pointer (fingertip is the pivot)
            var go = new GameObject("Hand", typeof(RectTransform), typeof(RawImage));
            hand = (RectTransform)go.transform;
            hand.SetParent(root, false);
            hand.sizeDelta = new Vector2(150, 150);
            hand.pivot = new Vector2(0.34f, 0.95f);
            var raw = go.GetComponent<RawImage>();
            raw.texture = Resources.Load<Texture2D>("tutorial_hand");
            raw.raycastTarget = false;
            if (raw.texture == null) raw.color = new Color(1, 1, 1, 0);

            Next(Step.Drag);
        }

        void Next(Step s)
        {
            step = s;
            stepStart = Time.unscaledTime;
            tapTarget = null;
            switch (s)
            {
                case Step.Drag:
                    Say("Drag your finger across the letters to spell  " + first.Word);
                    break;
                case Step.Rotate:
                    if (!gs.Board.CanRotate || gs.RotateButton == null || !gs.RotateButton.gameObject.activeInHierarchy) { Next(Step.Hint); return; }
                    Say("Nice! Tap the arrow to turn the board - it can help you see words.");
                    tapTarget = gs.RotateButton;
                    break;
                case Step.Hint:
                    Say("Stuck? Hints show you letters. Try this one - it's free!");
                    tapTarget = gs.BoosterButton(Booster.Letter);
                    break;
                case Step.Finish:
                    Say("Now find the last word:  " + second.Word);
                    break;
            }
            Tween.Punch(card, 0.08f, 0.2f);
        }

        void Say(string text)
        {
            cardText.text = text;
            card.localScale = Vector3.one;
        }

        void OnWordFound(PlacedWord w)
        {
            if (step == Step.Drag) Next(Step.Rotate);
        }

        void Update()
        {
            if (hand == null || gs == null) return;
            float t = Time.unscaledTime - stepStart;
            if (step == Step.Drag || step == Step.Finish)
            {
                var word = step == Step.Drag ? first : second;
                if (word.Found) { hand.gameObject.SetActive(false); return; }
                hand.gameObject.SetActive(true);
                // glide along the word's path, pause, repeat
                var pts = word.Path.Select(h => (Vector2)root.InverseTransformPoint(gs.Board.CellWorldPos(h))).ToList();
                float seg = 0.45f, total = seg * (pts.Count - 1), cycle = total + 1.1f;
                float u = (t % cycle) - 0.4f;
                Vector2 p;
                if (u <= 0) p = pts[0];
                else if (u >= total) p = pts[pts.Count - 1];
                else
                {
                    int i = Mathf.Min(pts.Count - 2, Mathf.FloorToInt(u / seg));
                    p = Vector2.Lerp(pts[i], pts[i + 1], Mathf.SmoothStep(0, 1, (u - i * seg) / seg));
                }
                SetHand(p, u > 0 && u < total + 0.2f ? 0.9f : 1f);
                var raw = hand.GetComponent<RawImage>();
                float fade = u > total + 0.4f ? 0f : 1f;
                raw.color = new Color(1, 1, 1, raw.texture == null ? 0 : fade);
            }
            else if (tapTarget != null)
            {
                hand.gameObject.SetActive(true);
                Vector2 p = root.InverseTransformPoint(tapTarget.position);
                float press = Mathf.Abs(Mathf.Sin(t * 4f));
                SetHand(p + new Vector2(10, -10 - press * 18f), 1f - press * 0.1f);
                hand.GetComponent<RawImage>().color = hand.GetComponent<RawImage>().texture == null ? Color.clear : Color.white;
            }
            else hand.gameObject.SetActive(false);
        }

        void SetHand(Vector2 local, float scale)
        {
            hand.anchorMin = hand.anchorMax = new Vector2(0.5f, 0.5f);
            hand.anchoredPosition = local + new Vector2(0, -10);
            hand.localScale = Vector3.one * scale;
            hand.SetAsLastSibling();
        }

        void Finish()
        {
            if (step == Step.Done) return;
            step = Step.Done;
            if (hand) hand.gameObject.SetActive(false);
            bool firstTime = !Save.Data.tutorialDone;
            Save.Data.tutorialDone = true;
            if (!firstTime) { Save.Write(); ZWordApp.I.ShowHome(); return; }
            Save.Coins += GameConfig.TutorialCoins;
            Save.Write();
            ZWordApp.I.ShowReward("YOU'RE READY!", GameConfig.TutorialCoins, 0, () =>
            {
                ZWordApp.I.ShowHome();
                RatePrompt.ShowAfterTutorial();
            });
        }

        void Skip()
        {
            if (step == Step.Done) return;
            step = Step.Done;
            Save.Data.tutorialDone = true;
            Save.Write();
            ZWordApp.I.ShowHome();
        }
    }
}
