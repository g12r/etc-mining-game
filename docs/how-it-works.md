# How the game works

A guide to `src/game.js` for whoever picks this up. Section names below match the `/* ---------- name ---------- */` banners in the file.

## The big picture

- **Engine:** three.js r128, one `<canvas>` inside `#stage`, first-person camera with pointer lock. If the mouse will not lock, the player can drag to look and F digs. R places whether or not the mouse is locked.
- **World:** a 64 × 64 × 64 grid of blocks (`X`, `Y`, `Z`), stored in `W` as one byte per block. Ground level is `SURF = 40`; `BASE = SURF - 1`. Depth in feet is `(BASE - y) * 5`.
- **It does not look like blocks.** The grid is only the data. What you see is a smooth mesh built from it (see "smooth rock mesh").
- **Debug handle:** `window.__ueg` exposes the player, game state `G`, the world arrays, `setBlock`, `breakBlock`, `addObject`, `rats`, `openStore`, `openMill`, `save` and more. Tests use it to set up a situation instead of playing to it.

## Block types

`AIR 0, GRASS 1, DIRT 2, ROCK 3, HARD 4, QUARTZ 5, RICH 6, BED 7, RUBBLE 8, PLANK 9, LOG 10, LEAF 11, ROOF 12`

- `QUARTZ` and `RICH` carry the gold. Deeper quartz holds more.
- `HARD`, `RICH`, and quartz 18 or more blocks down need the rock drill or dynamite (`needsDrill`).
- `PLANK`, `LOG`, `ROOF` are building blocks. They are in `NONNET`, meaning they are drawn as crisp boxes and are left out of the smooth rock mesh.
- `ALLOW` is how far a roof of each material spans from a wall before it starts to fail: 2 in dirt, 3 in rock, 4 in hard rock.

Placed gear lives in `objects`, not in the block grid: `LADDER 1, TIMBER 2, PUMP 3, FAN 4, DYN 5, CANNON 6, ELEV 7`. The revolver is not an object: it is held, with its loaded rounds in `G.cyl` and spare bullets in `G.pack.revolver`.

## Sections of game.js

| Section | What it does |
| --- | --- |
| sound | Small WebAudio synth: pick hits, rumble, drips, canary, squeaks, explosions. No audio files. |
| world constants | Sizes, block ids, spans, the town rectangle `TOWN`, the old mine entrance `ADIT`, the spawn point. |
| three | Renderer, scene, fog, sun with shadows, sky dome, the headlamp (a spot light that casts shadows), and the rock material. |
| smooth rock mesh (surface nets) | Turns the block grid into a smooth surface, in 16³ chunks (`CS`). A chunk is rebuilt when a block in or beside it changes. |
| world generation | Hills, dirt over rock over hard rock, quartz veins with rich pockets, trees, and the town. |
| the old mine entrance, rails, cart, lanterns | The scripted adit into the mountain that the player starts facing. |
| building outsides and insides | Store and mill details, the shopkeeper and assayer, the animated stamp battery, chimney smoke. `kit()` merges many small shapes into one mesh per material so a shelf of cans costs one draw call. Every piece goes through `addDecor` with the blocks that hold it up. `updateTown` runs the stamps, flywheel, smoke and the two people turning to look at you. |
| the saloon | Blocks in `TOWN_BOXES` (so the carpenter repairs it), decor in `buildSaloon`, batwing doors and the bartender in `updateSaloon`. `TOWN.z1` grew from 27 to 37 for its lot; `buildSaloonLot` flattens and builds that lot once in a save made before it existed (`G.saloon`). |
| rats | Wandering, feeding (E), following as a buddy, and bolting before a cave-in. |
| decor needs support / buildings fall down | Decorations and building blocks check for something underneath; without it they drop. This is what stops floating buildings. |
| grass that sways in the wind | Instanced grass blades on the surface. |
| headlamp beam in dusty air | Dust motes lit by the lamp. |
| state | `G` (money, sacks, gear, flags) and the save and load code. |
| objects | Placing and removing ladders, timber sets, pumps, fans, dynamite. |
| HUD | Money, sacks, the rock you are facing, the canary, temperature, depth, and the health, air and heat bars. |
| input | Keys, mouse, pointer lock, hotbar 1 to 7, Q for dynamite, R to place, E to use. |
| raycast | Finds the block the player is looking at. It tests the solid grid cells, not the smooth mesh. |
| player physics | A 0.3-wide, 1.7-tall capsule against the grid: walking, jumping, ladders, swimming. |
| actions | Digging, placing, lighting dynamite (`throwDynamite` falls back to dropping it at your feet). |
| particles, loose ore, falling rock | Debris, ore sacks to pick up, and rocks that fall in a collapse. |
| cave-in check (near the miner) | Measures how far each roof block is from support. Past its span it builds `stress`, creaks, drops dust and then falls. Timber sets reset the span. |
| water | Below the water table (`WTY`, about 60 ft) water seeps from rock into open tunnels and levels out. Pumps drain around them. |
| fresh air | Air spreads about 10 blocks from any opening to the sky and from fans. Beyond that the canary goes quiet and the air bar drops. Dynamite smoke counts as bad air. |
| explosions | Clears a sphere, including hard rock, throws debris, hurts the player if close. |
| cannons | `fireCannon` raycasts from the camera (ignoring the cannon itself), turns the cannon to the hit point and solves the low ballistic angle for a 34 m/s ball. `updateCannons` moves the balls and calls `explodeAt` on the first solid cell or object they touch. |
| the revolver | `shoot` raycasts 70 blocks, tests the five tin cans on the target fence first (ray against a small sphere), then the block or object hit. It never removes blocks. A hit on a lit dynamite object sets its fuse to nearly zero. `goldPop` floats the block's gold above the hit point; `oreGrade(t,y,x,z)` is fixed per block so the reading matches what digging gives. `reload` fills the six-shot cylinder from the spare bullets. Clicking and F call `shoot` instead of digging while item 9 is held. |
| horses | `G.horses` holds each horse's place and is saved. `riding` is the horse you are on: the player's capsule does the moving, speed goes up, the camera rises a metre, and `updateHorses` puts the horse under you and animates the legs from its speed (trot pairs, then a gallop). Idle horses settle onto the ground below them, so they never float. |
| mine elevators | `sinkShaft` levels a 2x2 spot, clears the shaft 12 blocks down and a station tunnel at the bottom, and returns the elevator's `set` (shaft corner, top, bottom), which is saved with the object. The cage height `o.cy` is not saved; it starts at the top. `cageHold` runs right after the player's physics and stands the player on the cage floor; landing on it from a fall still hurts. `shaftBottom` is worked out from the grid each time, so digging the shaft deeper lets the cage go deeper. |
| bandits | `raid` tracks the waves (`WAVES` = 2, 3, 4; the last has the boss with `need` 4 hits). `updateBandits` runs the raid timer and each bandit's state: `come`, `circle` (orbit about 9 blocks out and shoot when `clearLine` sees you), `rob` and `flee`. `moveBandit` steers around walls and settles onto the ground with `groundBelow`. `shoot` checks bandits with `banditHit` (a 0.55 sphere around the rider) before blocks. Bandits are not saved. In a headless test the frame rate is too low to hit a moving bandit by aiming; call `__ueg.hitBandit` instead, and `__ueg.raidIn(seconds)` to bring the next wave without waiting. |
| the shotgun | Slot 9 holds `G.gun`, either `revolver` or `shotgun`; pressing 9 while it is selected swaps. `shootShotgun` casts nine rays with `rayFrom` (the raycast for any start and direction) in a 0.075-radian cone; loaded shells are `G.sh`, spares `G.pack.shells`. |
| health | Damage from falls, rocks, drowning, bad air and heat; recovery. |
| store & mill | The General Store sells gear. The Stamp Mill crushes sacks for $1 each and the assayer pays $20 an ounce. |
| main loop | Per-frame update and draw. |

## Money

The player starts with $100,000,000 because Emmett asked for it (request 9). The store prices and the $1-a-board town bill still apply but no longer constrain anything. If he later wants money to matter again, that start value is the thing to change.

## Save data

Saved to `localStorage` under `ueg-save-v3`: the block grid, the height map, trees, `G`, the player's position, and placed objects. "Start a new mine" removes it. The save is per browser and per address, so the standalone file, an artifact and a hosted page each have their own.

## Mistakes already made once

- **Black tunnel walls.** The first smooth mesh shaded rock from a blurred field, which gave a zero gradient inside tunnels and so no lighting. The fix was a 7-point weighted sample for the brightness (`calcB`). If walls go black again, look there.
- **Gold specks the size of dinner plates, and rock that looked like TV static.** The speck and bump patterns were too low-frequency. They are now small, high-frequency specks, and the bump fades with distance.
- **A giant pickaxe filling the screen.** The held tool needed scaling down and moving to the lower right.
- **`smoothstep` with its edges the wrong way round.** GLSL does not define it when the first edge is larger. Use `1.0 - smoothstep(a, b, x)` with `a < b`.
- **Q did nothing.** See request 8: no dynamite in the pack, an aim that had to be exact, and a protected town. Any one of those reads to a player as "the key is broken".
- **R did nothing.** Request 11. R placed things already, but did nothing and said nothing when he held the pickaxe, had none of the item, or aimed at the sky. Now `placeAction` always places (falling back to the spot in front of his feet) or shows why not.
- **The first cannon blew up the player.** It fired along the look direction, the ball dropped onto the slope a few blocks ahead, and the blast hurt him. Aiming at the crosshair's hit point, and refusing targets under 5 blocks, fixed it.
- **Pale horses.** three r128 treats a hex colour as linear, so a black horse came out grey. Horse colours go through `convertSRGBToLinear()`.
- **Space never jumped.** From 0.1 to 0.6 the physics substeps cleared `p.ground` before every vertical move, including moves of zero, so a resting player ended each frame "in the air" and the jump check failed. Now ground is only cleared when there is vertical speed. Stair step-ups, which also check `p.ground`, started working at the same time.
- **Floating buildings.** Blasting under the town left it hanging until the support checks were added.

## When he says it's broken

1. Do what a player would do, with the same keys, starting from a fresh mine as well as a saved one.
2. Check what he had in his pack and where he was standing. Several "bugs" were really "you had none left" or "that only works underground" with no message saying so. The fix is then to make it work anyway or to tell him why on screen.
3. Look at a screenshot yourself before saying it is fixed.

## Testing

`tests/smoke.js` checks the page loads offline, the engine starts, and there are no page errors. For a feature test, set the scene through `window.__ueg`, act with real key presses, and wait on a condition with `waitForFunction`. Software WebGL runs slowly and the game caps the time step, so in-game seconds pass more slowly than wall-clock seconds.
