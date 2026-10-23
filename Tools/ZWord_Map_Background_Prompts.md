# Word Z: AI prompts for the 20 category map backgrounds

## How to use
1. Paste the **style block**, then add one **category scene** at the end of it.
2. **Settings:**
   - Portrait, **1080 × 2400** (9:20). If your tool can't do 9:20, use 9:16 and extend the top/bottom with "outpaint".
   - Highest quality, no upscaling artifacts.
3. **Save the result** as `map_<name>.jpg` with the names listed below.
4. **Drop it** into `Assets/ZWordGame/Art/Maps/`, overwriting the current file. The game picks it up automatically.
   - If you save a PNG instead, assign it in `Resources/ZWordTheme` → *Category Art* → *Map Background*.

The game draws the level path, numbered level bubbles, stars and moving effects on top of the image. So **the picture itself must not contain any path, numbers, buttons or text**, and the **middle third must stay calm and open** so the level bubbles stay readable.

---

## Style block (paste before every scene)

> Vertical mobile game level-map background, top-down three-quarter bird's-eye view, painted in a vibrant hand-painted storybook style for a cozy casual puzzle game. Soft cel shading, warm golden sunlight, rich saturated colors, gentle ambient occlusion, crisp clean shapes, high detail, joyful and lively atmosphere with tiny charming background characters and animals going about their day. The scene continues from the bottom to the top of the image like one long journey, with small changes in scenery as it goes up. Keep the central vertical third of the image open and uncluttered (ground, grass, water or floor only) with interesting details concentrated on the left and right sides. No text, no letters, no numbers, no UI, no paths or roads drawn through the middle, no frames, no borders, no watermark, no logos.

**Negative prompt (if your tool has one):** text, letters, numbers, watermark, signature, logo, UI, buttons, frame, border, blurry, photorealistic, dark, gloomy, horror, distorted faces, extra limbs, cropped edges, central road, dotted path

---

## Category scenes

| File name | Scene to append |
|---|---|
| `map_city.jpg` | A charming old European-style city along a sparkling river: terracotta rooftops, colorful townhouses, domed cathedral and clock tower on the sides, stone bridges, market stalls with striped awnings, flower boxes, tiny pedestrians, bicycles, pigeons, a little tram, park trees, warm late-afternoon light. |
| `map_electronic.jpg` | A glowing techno-garden at dusk: giant friendly circuit boards as terrain, neon-blue and violet light trails, cute little robots tending glowing plants, floating holographic screens on the sides, antennas, tiny drones with lights, soft cyan glow, starry purple sky peeking at the top. |
| `map_things.jpg` | A cozy giant attic seen from above: warm wooden floor planks in the middle, and on the sides oversized everyday objects (books stacked like towers, teacups, lamps, clocks, toy blocks, balls of yarn, a rocking horse), a sleepy cat, dust motes in sunbeams from round windows. |
| `map_meals.jpg` | A delicious food-land picnic: a soft checkered picnic blanket meadow in the center, with sides of cake hills, pancake stacks, burger houses, strawberry bushes, chocolate river edges, candy flowers, little chefs and happy picnicking critters, warm sunny light. |
| `map_music.jpg` | A magical concert valley at night: purple and magenta stage lights sweeping the sky, piano-key hills, giant guitars and drums as scenery on the sides, glowing floating music notes, fireflies, tiny band members and dancing animals, sparkling stars at the top. |
| `map_sport.jpg` | A huge sunny sports park: fresh striped green turf in the center, with tennis courts, a running track, basketball hoops, a small stadium with flags, goals, cheering mini crowds, balloons and bunting along the sides, bright midday light. |
| `map_countries.jpg` | A whimsical world-travel ocean: bright turquoise sea with gentle waves, and along the sides tiny islands each showing a famous-style landmark silhouette (pyramids, pagoda, windmill, castle, temple, totem, lighthouse), sailboats, hot-air balloons, dolphins, seagulls. |
| `map_cinema.jpg` | A glamorous movie-studio backlot: red velvet curtain edges, golden spotlights, film reels and clapperboards as scenery, a red carpet area, studio sets (a castle facade, a pirate ship, a space set) on the sides, popcorn carts, tiny film crews with cameras, twinkling marquee bulbs. |
| `map_animals.jpg` | A lush savanna and jungle safari: golden grassland in the center, acacia trees, a watering hole on one side, friendly cartoon elephants, giraffes, zebras, lions resting, monkeys in trees, parrots, butterflies, warm sunset glow toward the top. |
| `map_nature.jpg` | An enchanted forest valley: a soft mossy meadow in the center, a sparkling stream and waterfall on the side, tall pines and blossoming trees, mushrooms, ferns, wildflowers, deer, rabbits, foxes, birds, sunbeams through leaves, misty mountains at the top. |
| `map_fruit_veg.jpg` | A happy farm and orchard: neat vegetable rows and soft soil in the center, with fruit trees heavy with apples and oranges, pumpkin patches, a red barn, a windmill, a scarecrow, chickens, a friendly tractor, beehives, sunflowers on the sides. |
| `map_jobs.jpg` | A busy miniature town of workers: a small square in the center, with a fire station and red truck, a bakery, a hospital, a school, a construction site with a crane, a post office, a police box, tiny workers in uniforms, delivery vans, trees. |
| `map_body.jpg` | A soft, cute, playful wellness park: pastel pink and peach terrain in the center, with a yoga lawn, a fruit smoothie stand, a playground, a gym with tiny dumbbells, heart-shaped bushes, jogging critters, a swimming pool, floating bubbles, gentle candy-colored light. |
| `map_clothes.jpg` | A fashionable boutique street from above: a pastel plaza in the center, with tailor shops, hat stands, shoe stores, clotheslines with colorful garments, mannequins, fabric rolls, a little runway with tiny models, buttons and spools as decorations, sparkles. |
| `map_weather.jpg` | A sky kingdom of weather: fluffy cloud islands in the center, with a rainbow arching on the side, a sunny corner, a gentle rain cloud, a snowy cloud with a snowman, a windmill, kites, hot-air balloons, a tiny lightning cloud, birds flying, soft blue sky. |
| `map_space.jpg` | A cute cosmic galaxy: a deep purple and navy starfield in the center, with colorful ringed planets, moons with craters, a friendly rocket, a space station, tiny astronauts floating, comets, nebula clouds in pink and teal, twinkling stars everywhere. |
| `map_ocean.jpg` | A vibrant underwater coral reef: soft sandy seabed and clear blue water in the center, with coral reefs, swaying kelp, sea anemones, colorful fish schools, a smiling turtle, octopus, starfish, seahorses, a sunken treasure chest, light rays from the surface at the top. |
| `map_kitchen.jpg` | A giant cozy kitchen countertop from above: warm cream and terracotta tiles in the center, with pots and pans, a steaming kettle, cutting boards with vegetables, jars of spices, a rolling pin and dough, cookies cooling, a little mouse chef, warm window light. |
| `map_school.jpg` | A cheerful school campus: a green schoolyard in the center, with a red-brick school with a bell tower, a playground, a library, a science garden with a telescope, a chalkboard wall with doodles, a school bus, backpacks, kids playing, autumn trees. |
| `map_travel.jpg` | An adventure travel map come to life: a vintage parchment world below, with a sunny holiday scene on top, an airport with a little plane, a train on tracks along the side, a cruise ship, mountains with a cable car, a campsite with tents, suitcases, a compass rose, a hot-air balloon. |

## Tips for more life
- Add **"tiny characters going about their day, small animals, lights in windows"** to make any scene feel inhabited.
- Generate **3–4 variations** and pick the one with the calmest centre.
- **Keep one style throughout:** reuse the same seed, or use your tool's style reference with your favourite finished map, so all 20 look like one game.
- The game already adds moving effects on top of each map: drifting leaves, rising bubbles, twinkling stars, floating notes and more. Leave room in the sky and edges for them.
