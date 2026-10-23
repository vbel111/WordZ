using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>
    /// The honeycomb of letter tiles. Handles drag-to-select across adjacent hexes,
    /// connector lines, found-word colouring, hint glows and board rotation.
    /// </summary>
    public class HexBoard : MonoBehaviour, IPointerDownHandler, IDragHandler, IPointerUpHandler
    {
        class Tile
        {
            public Hex Hex;
            public RectTransform Root;
            public Image Shadow, Face, Glow;
            public TMP_Text Letter;
            public bool Locked;
            public Color FaceColor = Palette.Cream, ShadowColor = Palette.CreamShadow, LetterColor = Palette.Brown;
        }

        public event Action<List<Hex>> SelectionCompleted;
        public event Action<string> SelectionChanged;
        public bool Interactable = true;

        readonly Dictionary<Hex, Tile> tiles = new Dictionary<Hex, Tile>();
        readonly List<Hex> selection = new List<Hex>();
        readonly List<Image> lines = new List<Image>();
        RectTransform tilesRoot, linesRoot, rt;
        Level level;
        float radius;
        int rotation;
        static readonly float Sqrt3 = Mathf.Sqrt(3f);

        public static HexBoard Create(Transform parent, Level level, float hexRadius)
        {
            var rt = UI.Rect("Board", parent);
            var hit = rt.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            var board = rt.gameObject.AddComponent<HexBoard>();
            board.rt = rt;
            board.level = level;
            board.radius = hexRadius;
            board.Build();
            return board;
        }

        Vector2 Pos(Hex h)
        {
            var r = h.Rotate(rotation);
            return new Vector2(radius * 1.5f * r.Q, -radius * Sqrt3 * (r.R + r.Q * 0.5f));
        }

        void Build()
        {
            var ext = Extents(level, radius);
            rt.sizeDelta = ext + new Vector2(40, 40);

            tilesRoot = UI.Rect("Tiles", rt).Stretch();
            linesRoot = UI.Rect("Lines", rt).Stretch();

            var tileSize = new Vector2(radius * 2f * 0.95f, radius * Sqrt3 * 0.95f);
            int i = 0;
            foreach (var h in level.Cells)
            {
                var t = new Tile { Hex = h };
                t.Root = UI.Rect("Hex " + h, tilesRoot);
                t.Root.Place(new Vector2(0.5f, 0.5f), Pos(h), tileSize);

                t.Glow = UI.Img(t.Root, Sprites.Hexagon, new Color(1f, 1f, 0.7f, 0f), "Glow");
                t.Glow.rectTransform.Stretch(-14, -22, -14, -10);
                t.Shadow = UI.Img(t.Root, Sprites.Hexagon, t.ShadowColor, "Shadow");
                t.Shadow.rectTransform.Stretch(0, -12, 0, 12);
                t.Face = UI.Img(t.Root, Sprites.Hexagon, t.FaceColor, "Face");
                t.Face.rectTransform.Stretch();
                var gloss = UI.Img(t.Face.transform, Sprites.Hexagon, new Color(1, 1, 1, 0.25f), "Gloss");
                gloss.rectTransform.Stretch(14, 30, 14, 6);

                t.Letter = UI.Label(t.Root, level.Letters[h].ToString(), Mathf.RoundToInt(radius * 0.85f), t.LetterColor, TextAnchor.MiddleCenter, false);
                t.Letter.rectTransform.Stretch(0, 4, 0, 0);

                tiles[h] = t;
                Tween.PopIn(t.Root, 0.35f, 0.02f * i++);
            }
        }

        // ---------------- Input ----------------

        bool TryPick(PointerEventData e, out Hex hex)
        {
            hex = default;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, e.position, e.pressEventCamera, out var local))
                return false;
            float best = radius * 0.8f; // inner hit radius to make diagonal drags reliable
            bool found = false;
            foreach (var kv in tiles)
            {
                float d = Vector2.Distance(local, kv.Value.Root.anchoredPosition);
                if (d < best) { best = d; hex = kv.Key; found = true; }
            }
            return found;
        }

        public void OnPointerDown(PointerEventData e)
        {
            if (!Interactable) return;
            ClearSelection();
            if (TryPick(e, out var h) && !tiles[h].Locked) Add(h);
        }

        public void OnDrag(PointerEventData e)
        {
            if (!Interactable || selection.Count == 0) return;
            if (!TryPick(e, out var h)) return;
            var last = selection[selection.Count - 1];
            if (h.Equals(last)) return;
            if (selection.Count >= 2 && h.Equals(selection[selection.Count - 2]))
            {
                RemoveLast();
                return;
            }
            if (selection.Contains(h) || tiles[h].Locked || !last.IsAdjacent(h)) return;
            Add(h);
        }

        public void OnPointerUp(PointerEventData e)
        {
            if (selection.Count == 0) return;
            var result = new List<Hex>(selection);
            ClearSelection();
            if (result.Count > 1) SelectionCompleted?.Invoke(result);
        }

        void Add(Hex h)
        {
            selection.Add(h);
            var t = tiles[h];
            Paint(t, Palette.Yellow, Palette.YellowShadow, Palette.Brown);
            Tween.Punch(t.Root, 0.12f, 0.18f);
            AudioManager.Letter(selection.Count - 1);
            if (selection.Count > 1) AddLine(selection[selection.Count - 2], h);
            SelectionChanged?.Invoke(CurrentWord());
        }

        void RemoveLast()
        {
            var h = selection[selection.Count - 1];
            selection.RemoveAt(selection.Count - 1);
            var t = tiles[h];
            Paint(t, t.FaceColor, t.ShadowColor, t.LetterColor);
            if (lines.Count > 0)
            {
                Destroy(lines[lines.Count - 1].gameObject);
                lines.RemoveAt(lines.Count - 1);
            }
            SelectionChanged?.Invoke(CurrentWord());
        }

        public void ClearSelection()
        {
            foreach (var h in selection)
            {
                var t = tiles[h];
                Paint(t, t.FaceColor, t.ShadowColor, t.LetterColor);
            }
            selection.Clear();
            foreach (var l in lines) if (l) Destroy(l.gameObject);
            lines.Clear();
            SelectionChanged?.Invoke("");
        }

        string CurrentWord()
        {
            var chars = new char[selection.Count];
            for (int i = 0; i < selection.Count; i++) chars[i] = level.Letters[selection[i]];
            return new string(chars);
        }

        void AddLine(Hex a, Hex b)
        {
            var pa = tiles[a].Root.anchoredPosition;
            var pb = tiles[b].Root.anchoredPosition;
            var line = UI.Img(linesRoot, Sprites.Rounded, new Color(1f, 1f, 1f, 0.85f), "Line", 5f);
            var lr = line.rectTransform;
            var dir = pb - pa;
            lr.Place(new Vector2(0.5f, 0.5f), (pa + pb) * 0.5f, new Vector2(dir.magnitude * 0.42f, 18));
            lr.localRotation = Quaternion.Euler(0, 0, Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg);
            var arrow = UI.Img(lr, Sprites.Play, new Color(1f, 1f, 1f, 0.95f), "Arrow");
            arrow.rectTransform.Place(new Vector2(1f, 0.5f), new Vector2(4, 0), new Vector2(40, 40));
            lines.Add(line);
        }

        static void Paint(Tile t, Color face, Color shadow, Color letter)
        {
            t.Face.color = face;
            t.Shadow.color = shadow;
            t.Letter.color = letter;
        }

        // ---------------- Game feedback ----------------

        public void MarkFound(List<Hex> path, Color color)
        {
            for (int i = 0; i < path.Count; i++)
            {
                var t = tiles[path[i]];
                t.Locked = true;
                t.FaceColor = color;
                t.ShadowColor = Palette.Darken(color, 0.7f);
                t.LetterColor = Color.white;
                t.Glow.color = new Color(1, 1, 1, 0);
                var tile = t;
                Tween.Value(0.01f, _ => { }, null, i * 0.06f, () =>
                {
                    Paint(tile, tile.FaceColor, tile.ShadowColor, tile.LetterColor);
                    Tween.Punch(tile.Root, 0.25f, 0.3f);
                });
            }
        }

        /// <summary>Flip the given tiles and show their (new) letters from level.Letters (used by Shuffle).</summary>
        public void Relabel(IEnumerable<Hex> cells)
        {
            ClearSelection();
            int i = 0;
            foreach (var h in cells)
            {
                var tile = tiles[h];
                Tween.Value(0.32f, k =>
                {
                    if (!tile.Root) return;
                    float sx = Mathf.Abs(Mathf.Cos(k * Mathf.PI));
                    tile.Root.localScale = new Vector3(Mathf.Max(0.05f, sx), 1f, 1f);
                    if (k >= 0.5f) tile.Letter.text = level.Letters[tile.Hex].ToString();
                }, null, (i++) * 0.025f, () =>
                {
                    if (!tile.Root) return;
                    tile.Root.localScale = Vector3.one;
                    tile.Letter.text = level.Letters[tile.Hex].ToString();
                });
            }
        }

        public void ShakeTiles(List<Hex> path)
        {
            foreach (var h in path) Tween.Shake(tiles[h].Root, 10f, 0.3f);
        }

        /// <summary>Pulse a glow around the given cells (used by hint boosters).</summary>
        public void Glow(List<Hex> cells, float duration, float stagger = 0.12f)
        {
            for (int i = 0; i < cells.Count; i++)
            {
                var t = tiles[cells[i]];
                if (t.Locked) continue;
                Tween.Value(duration, k =>
                {
                    float a = Mathf.Sin(k * Mathf.PI * 4f) * 0.5f + 0.5f;
                    t.Glow.color = new Color(1f, 0.95f, 0.5f, a * (1f - k * 0.5f));
                }, null, i * stagger, () => t.Glow.color = new Color(1, 1, 1, 0));
            }
        }

        public bool CanRotate => level.RotStep > 0;

        /// <summary>World position of a tile (for tutorial pointers and effects).</summary>
        public Vector3 CellWorldPos(Hex h) => tiles.TryGetValue(h, out var t) ? t.Root.position : transform.position;

        /// <summary>Width/height the board needs at the given hex radius.</summary>
        public static Vector2 Extents(Level level, float radius)
        {
            float minX = float.MaxValue, maxX = float.MinValue, minY = float.MaxValue, maxY = float.MinValue;
            foreach (var h in level.Cells)
            {
                float x = radius * 1.5f * h.Q, y = -radius * Sqrt3 * (h.R + h.Q * 0.5f);
                minX = Mathf.Min(minX, x); maxX = Mathf.Max(maxX, x);
                minY = Mathf.Min(minY, y); maxY = Mathf.Max(maxY, y);
            }
            return new Vector2(maxX - minX + 2f * radius, maxY - minY + Sqrt3 * radius);
        }

        /// <summary>Largest hex radius (capped) at which the board fits the given box.</summary>
        public static float FitRadius(Level level, float maxW, float maxH, float cap = 100f)
        {
            var unit = Extents(level, 1f);
            return Mathf.Min(cap, maxW / unit.x, maxH / unit.y);
        }

        public void Rotate()
        {
            if (!CanRotate) return;
            ClearSelection();
            rotation = (rotation + level.RotStep) % 6;
            foreach (var t in tiles.Values)
            {
                var tile = t;
                var from = tile.Root.anchoredPosition;
                var to = Pos(tile.Hex);
                // move along an arc around the board centre
                float a0 = Mathf.Atan2(from.y, from.x), a1 = Mathf.Atan2(to.y, to.x);
                float r0 = from.magnitude, r1 = to.magnitude;
                if (a1 > a0) a1 -= Mathf.PI * 2f;
                Tween.Value(0.35f, k =>
                {
                    float a = Mathf.Lerp(a0, a1, k), r = Mathf.Lerp(r0, r1, k);
                    tile.Root.anchoredPosition = r < 1f ? to : new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * r;
                }, Tween.OutCubic, 0, () => tile.Root.anchoredPosition = to);
            }
        }
    }
}
