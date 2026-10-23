# Word Z art generator

All game art in `Assets/ZWordGame/Art` is original and generated from code here (no third-party art).

1. `python gen_icons.py` and `python gen_scenes.py` write SVGs to `svg/`.
2. `node render.js` renders them to PNG in `png/` with headless Chromium (needs `npm i playwright`).
   Put `Baloo2-ExtraBold.ttf` (from Assets/Hyper_Casual_UI/Fonts) next to render.js first.
3. Copy the PNGs into `Assets/ZWordGame/Art/...` (maps and the home background as JPG).

Edit colours, shapes or props in the Python files and re-run to restyle anything.
