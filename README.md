# Untitled Emmett Game

A realistic 3D gold mine game. You are a hard-rock gold miner: the old EMMETT No. 1 mine is in the mountain straight ahead. Buy gear at the General Store, follow the quartz, and haul your ore sacks to the Stamp Mill.

Designed by Emmett. Built with Claude.

## Play

Play online at https://g12r.github.io/etc-mining-game/, or open `index.html` in a browser. It is one self-contained page and needs no internet. Turn your sound on. Your mine saves in that browser.

## Controls

| Key | What it does |
| --- | --- |
| `W` `A` `S` `D` | Walk. Hold `Shift` to run. |
| Mouse | Look around |
| Left click | Dig (hold it down), pick gear back up, or shoot the revolver |
| `R` or right click | Place the item you are holding |
| `Space` | Jump. Walk into a ladder and hold `W` to climb. |
| `Q` | Light dynamite where you are looking (or at your feet), then run! You start with 3 sticks. |
| `1`–`9` | Choose an item |
| `E` | Use the store or mill, feed a rat, fire a cannon, or get on and off a horse |
| `Esc` | Pause and get your mouse back |

If the mouse will not lock, drag to look and use `F` to dig.

## What can go wrong in a mine

- **Cave-ins.** A tunnel roof only holds so far from a wall: about 2 blocks in dirt, 3 in rock, 4 in hard rock. Past that it creaks, dust falls and it comes down. Put in timber sets: two posts and a cap beam across the tunnel.
- **Groundwater.** Below about 60 feet, water seeps out of the rock and floods your tunnels. You can't breathe underwater. A pump drains everything near it.
- **Bad air.** Fresh air only reaches about 10 blocks from an opening. Watch your canary: if it stops singing, get out, or set up a fan. Dynamite smoke is bad air too.
- **Heat.** Rock gets hotter the deeper you go. Past about 95°F your heat bar fills up. A fan blowing cool air keeps you working.
- **Hard rock.** Hard rock, and quartz deep down, won't break with a pick. Buy a rock drill or use dynamite.

## Also in the mine

- **Rats.** Press `E` next to one to give it a crumb, and it becomes your buddy and follows you. If the rats suddenly run away squeaking, a cave-in is coming!
- **The town.** You can dig or blast anything in town, but the townsfolk bill you $1 for every board you wreck. The carpenter fixes it after a while. Knock out what holds a building up and it falls down. Chop a tree to get a timber set. Walk inside: the store has a shopkeeper at the counter, and the mill has a working stamp battery, a steam boiler and the assayer.
- **Cannons.** Put one down with `R` (item 8), stand next to it and press `E`. It aims at whatever your crosshair is on and the ball blows up where it lands.
- **Revolver.** Item 9. Left click shoots, `R` reloads six shots. Knock the tin cans off the target fence by the store, or set off a lit stick of dynamite from a safe distance.
- **Horses.** Nugget, Midnight and Dusty are tied up east of the store. Press `E` to ride, hold `Shift` to gallop.
- **Shoot to assay.** Shoot a rock and the gold in it pops up on screen.
- **Money and the mill.** Ore sacks aren't gold yet. The stamp mill crushes them for $1 a sack, and the assayer pays $20 an ounce. Deeper quartz holds more gold.

## Working on the game

The game is built from `src/` with `python3 build.py`. `CLAUDE.md` is the handover for anyone, person or AI, picking the project up: it says how to work with the designer and points to the full history in `docs/`.

three.js is used under the MIT licence; see `vendor/THREE-LICENSE`.
