using System.Collections.Generic;
using System.Linq;

namespace ZWord
{
    /// <summary>One step of the per-category difficulty curve.</summary>
    public struct RampStep
    {
        public int[] Columns;   // board shape as column heights (flat-top hexes)
        public int MinWords, MaxWords, MinLen, MaxLen;

        public RampStep(int[] cols, int minW, int maxW, int minLen, int maxLen)
        {
            Columns = cols; MinWords = minW; MaxWords = maxW; MinLen = minLen; MaxLen = maxLen;
        }
    }

    /// <summary>
    /// Board shapes and the 25-level difficulty ramp used by the level baker.
    /// Shapes are lists of column heights; alternate columns are offset by half a hex, so
    /// even-indexed columns (from the centre) need odd heights and odd ones even heights
    /// to stay symmetrical.
    /// </summary>
    public static class BoardShapes
    {
        public const int LevelsPerCategory = 25;

        public static readonly int[] S7 = { 2, 3, 2 };
        public static readonly int[] S13 = { 4, 5, 4 };
        public static readonly int[] S17 = { 3, 4, 3, 4, 3 };
        public static readonly int[] S19 = { 3, 4, 5, 4, 3 };
        public static readonly int[] S23 = { 5, 4, 5, 4, 5 };
        public static readonly int[] S27 = { 5, 6, 5, 6, 5 };

        static RampStep[] ramp;

        /// <summary>Level index (0-24) -> shape and word rules. Small boards and short words first.</summary>
        public static RampStep[] Ramp
        {
            get
            {
                if (ramp != null) return ramp;
                var list = new List<RampStep>();
                void Add(int n, int[] cols, int minW, int maxW, int minLen, int maxLen)
                {
                    for (int i = 0; i < n; i++) list.Add(new RampStep(cols, minW, maxW, minLen, maxLen));
                }
                Add(2, S7, 2, 2, 3, 4);
                Add(4, S13, 3, 3, 3, 6);
                Add(4, S17, 3, 4, 3, 7);
                Add(6, S19, 3, 5, 3, 8);
                Add(4, S23, 4, 5, 4, 8);
                Add(5, S27, 4, 6, 4, 8);
                ramp = list.ToArray();
                return ramp;
            }
        }

        /// <summary>Cells of a column-height shape, centred on the origin.</summary>
        public static List<Hex> Cells(int[] cols)
        {
            var cells = new List<Hex>();
            int n = cols.Length;
            for (int i = 0; i < n; i++)
            {
                int q = i - (n - 1) / 2;
                int L = cols[i];
                int shift = Mod2(L - 1) == Mod2(q) ? 0 : (q > 0 ? 1 : -1);
                for (int k = 0; k < L; k++)
                {
                    int v = -(L - 1) + 2 * k + shift; // vertical index: v = 2r + q
                    cells.Add(new Hex(q, (v - q) / 2));
                }
            }
            return cells;
        }

        static int Mod2(int x) => ((x % 2) + 2) % 2;

        /// <summary>Smallest rotation (in 60 degree steps) that maps the shape onto itself: 1, 3, or 0 for none.</summary>
        public static int RotationStep(IEnumerable<Hex> cells)
        {
            var set = new HashSet<Hex>(cells);
            if (set.All(h => set.Contains(h.Rotate(1)))) return 1;
            if (set.All(h => set.Contains(h.Rotate(3)))) return 3;
            return 0;
        }

        /// <summary>Seconds allowed for a board of this many letters.</summary>
        public static float TimeFor(int letters) => System.Math.Max(45f, 25f + 6.5f * letters);
    }
}
