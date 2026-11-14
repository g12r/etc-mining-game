# Untitled Emmett Game

A realistic 3D gold mine game, designed by Emmett and built by Claude. This file is the handover: read it, then the files it points to, before changing anything.

## Who you are working with

- **Emmett is the game designer and he is at the keyboard.** He is a kid. He decides what the game is. A parent set this up and may step in now and then.
- **Talk to him like a teammate, not a customer.** Short messages, plain words, no jargon. He types fast and spells loosely ("diynamite", "relistic grafics", "bildings"); work out what he means and never correct his spelling.
- **Build first, ask little.** When he asks for something, make it and show him. Ask a question only when two readings would give very different games, and then offer 2 to 4 choices he can pick from.
- **If he says it doesn't work, believe him.** Reproduce it the way a player would hit it (see "When he says it's broken" in `docs/how-it-works.md`), fix it, and tell him what was wrong in one sentence.
- **He likes:** mining, gold and gems, realism ("like you are in a real mine"), machines, blowing things up, and rats, which are his favourite animal.
- **Keep the name.** The game is called "Untitled Emmett Game" until he renames it. He can, whenever he wants.

## What to read

| File | What it gives you |
| --- | --- |
| `docs/requests.md` | Every request Emmett has made, in his own words, and what was built for each. Start here. |
| `docs/how-it-works.md` | How the game is built: world, rock mesh, lighting, hazards, rats, town, save data, and the mistakes already made once. |
| `docs/transcript.md` | The full conversation in which the game was made, word for word. |
| `history/` | The earlier versions (0.1 to 0.3) as playable pages, for comparison. |
| `README.md` | The player-facing description and controls. |

## The files

| File | What it is |
| --- | --- |
| `src/head.html` | Page markup and styles: HUD, hotbar, start screen, the controls and mine-safety notes under the game. Loads three.js r128 from cdnjs. |
| `src/game.js` | The whole game, about 730 long lines. Starts with `<script>` and ends with `</script>`. |
| `vendor/three.min.js` | three.js r128, copied into the standalone page. |
| `build.py` | Joins the above into the two pages below. |
| `index.html` | Built. The game as one page that runs with no internet. This is what a player opens. |
| `releases/index.html` | Built. A copy of `index.html` that GitHub Pages publishes at https://g12r.github.io/etc-mining-game/ on every push to `main` (`.github/workflows/pages.yml`). |
| `artifact.html` | Built. The same game without a page wrapper, for publishing as a Claude artifact. |
| `tests/smoke.js` | Loads the built page headless and checks the 3D world starts with no errors. |

Edit only `src/`. Then:

```bash
python3 build.py
```

```bash
cd tests && node smoke.js
```

## How to work

1. Change `src/game.js` or `src/head.html`.
2. Build, then run the smoke test. For anything he will see or feel, also drive it in a headless browser and look at a screenshot before telling him it is done. `window.__ueg` exposes the game's insides for that.
3. Show him. Publish `artifact.html` as an artifact so he can play right away. The game is published at https://claude.ai/artifact/CiA2R61e7n7WeLSWm5oxZN. It belongs to the account, so a new session can update it: read it with the Artifact tool first, then publish to that URL so Emmett keeps the same link.
4. Bump the version in `src/head.html` (the "Version 0.7" line) when a batch of his requests lands, and add the requests to `docs/requests.md`.
5. Commit to `main` and push. No pull requests for this project. The parent confirmed this in session; the push to `main` also republishes the GitHub Pages site. Write the commit message so that the history reads as the story of the game.

Things that are easy to get wrong:

- **Artifact rules.** `artifact.html` has no doctype, `<html>`, `<head>` or `<body>`; the publisher adds them. Scripts may only come from cdnjs (three.js r128 is there). One dark theme by design.
- **Headless WebGL is slow.** Launch Chromium with `--use-gl=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`. Frame time is capped, so fuses, collapses and water take longer than real time: wait on a condition with `waitForFunction`, not a fixed delay.
- **Saves.** The mine saves in the browser under `ueg-save-v3`. If you change the world format, bump the key or migrate, or his old mine will load broken.
- **Keep it realistic and not blocky.** Two of his requests were exactly that. Do not reintroduce cube-looking rock, and do not leave anything floating in the air.
- **This repository is public.** Do not add surnames, addresses, school names, photos or contact details.

## Where the game stands

Version 0.7. Everything in `docs/requests.md` is built and working as far as scripted tests show. Nobody has written down a list of what Emmett wants next; ask him.
