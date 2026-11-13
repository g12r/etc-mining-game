#!/usr/bin/env python3
"""Build the game from the pieces in src/.

    python3 build.py

Writes two files:

  index.html     The game as one self-contained page. The 3D engine (three.js)
                 is copied inside it, so it runs with no internet connection.
  artifact.html  The same game for publishing as a Claude artifact. It has no
                 page wrapper and loads three.js from a CDN instead.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


head = read('src/head.html')
game = read('src/game.js')   # starts with <script> and ends with </script>
three = read('vendor/three.min.js')
assert head.count(CDN) == 1, 'src/head.html should load three.js exactly once'

inline = ('<script>\n/* three.js r128, included so the game works without the internet. '
          'MIT licence, see vendor/THREE-LICENSE. */\n' + three + '\n</script>')
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + head.replace(CDN, inline) + game)

with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
with open(os.path.join(ROOT, 'artifact.html'), 'w', encoding='utf-8') as f:
    f.write(head + game)
print('built index.html (%d bytes) and artifact.html (%d bytes)' % (len(page), len(head) + len(game)))
