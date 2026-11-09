#!/usr/bin/env python3
"""
Draws every new texture of Wilderness Bound Expanded as 16x16 pixel art in the vanilla style.

Run:  python3 tools/textures.py   (needs Pillow)

Hand-made pixel art is written as ASCII grids: each character is a palette entry, '.' is transparent.
Noisy materials (thatch, peat, iron) are generated with a fixed seed so the output never changes.
Nothing here is copied from Minecraft's own textures.
"""
import os
import random

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "wilderness", "textures")


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def grid(rows, palette, size=(16, 16)):
    """Builds an image from ASCII rows. Rows shorter than the width are padded with transparency."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in (".", " "):
                continue
            px[x, y] = hexc(palette[ch]) if isinstance(palette[ch], str) else palette[ch]
    return img


def rows_of(text):
    lines = text.strip("\n").split("\n")
    return [line.rstrip() for line in lines]


def save(img, path):
    full = os.path.join(TEX, path + ".png")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full)


def save_mcmeta(path, frametime):
    full = os.path.join(TEX, path + ".png.mcmeta")
    with open(full, "w") as f:
        f.write('{\n  "animation": {\n    "frametime": %d\n  }\n}\n' % frametime)


def ramp(*hexes):
    return [hexc(h) for h in hexes]


# ----------------------------------------------------------------------------------------------------------------
# Building blocks
# ----------------------------------------------------------------------------------------------------------------

def thatch_side():
    pal = ramp("#3b2a12", "#56401d", "#715529", "#8d6c35", "#a98642", "#c29f51", "#d6b462")
    rng = random.Random(1907)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for layer in range(4):
        y0 = layer * 4
        tones = [rng.choice((3, 4, 4, 5, 5, 6)) for _ in range(16)]
        for x in range(16):
            t = tones[x]
            # row 0: shadow cast by the layer above, broken by a few hanging strand tips
            px[x, y0] = pal[t - 1] if rng.random() < 0.22 else pal[rng.choice((0, 1))]
            px[x, y0 + 1] = pal[max(1, t - 2)]
            px[x, y0 + 2] = pal[t - 1]
            px[x, y0 + 3] = pal[min(6, t + (1 if rng.random() < 0.45 else 0))]
    return img


def thatch_top():
    pal = ramp("#4a3617", "#64491f", "#7f5f2b", "#9a7536", "#b38c43", "#c9a353", "#dbb964")
    rng = random.Random(2711)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = pal[rng.choice((2, 3, 3, 4))]
    # crossing straws, short diagonal streaks in both directions
    for _ in range(30):
        x, y = rng.randrange(16), rng.randrange(16)
        dx = rng.choice((1, -1))
        length = rng.randint(2, 4)
        tone = rng.choice((4, 5, 5, 6))
        for i in range(length):
            px[(x + i * dx) % 16, (y + i) % 16] = pal[tone]
            if i == 0:
                px[(x - dx) % 16, (y - 1) % 16] = pal[1]
    for _ in range(14):
        x, y = rng.randrange(16), rng.randrange(16)
        px[x, y] = pal[rng.choice((0, 1))]
    return img


def peat():
    pal = ramp("#24170f", "#311f14", "#3f2a1b", "#4d3422", "#5c3f29", "#6e5032")
    fiber = ramp("#7a5c3a", "#8e6d47")
    rng = random.Random(4421)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    # clustered noise: start dark-mid, grow blobs
    for y in range(16):
        for x in range(16):
            px[x, y] = pal[rng.choice((1, 2, 2, 3, 3, 4))]
    for _ in range(9):
        cx, cy = rng.randrange(16), rng.randrange(16)
        tone = rng.choice((0, 1, 4, 5))
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0)):
            if rng.random() < 0.8:
                px[(cx + dx) % 16, (cy + dy) % 16] = pal[tone]
    # fibrous root bits
    for _ in range(7):
        x, y = rng.randrange(16), rng.randrange(16)
        length = rng.randint(2, 3)
        for i in range(length):
            px[(x + i) % 16, (y + (1 if i == 2 else 0)) % 16] = fiber[rng.randrange(2)]
    return img


def peat_bricks():
    mortar = hexc("#2a1b12")
    body = ramp("#4f3524", "#5c3e2a", "#694731", "#765138")
    light = hexc("#86603f")
    dark = hexc("#3e2a1c")
    rng = random.Random(3307)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for course in range(4):
        y0 = course * 4
        offset = 0 if course % 2 == 0 else 4
        for y in range(y0, y0 + 4):
            for x in range(16):
                bx = (x - offset) % 16
                in_mortar_v = bx % 8 == 7
                in_mortar_h = y == y0 + 3
                if in_mortar_v or in_mortar_h:
                    px[x, y] = mortar
                    continue
                c = body[rng.choice((1, 2, 2, 3))]
                if y == y0:
                    c = light if rng.random() < 0.7 else body[3]
                elif bx % 8 == 0:
                    c = light if rng.random() < 0.5 else body[3]
                elif y == y0 + 2 or bx % 8 == 6:
                    c = dark if rng.random() < 0.6 else body[0]
                px[x, y] = c
    return img


# ----------------------------------------------------------------------------------------------------------------
# Plants (cross models)
# ----------------------------------------------------------------------------------------------------------------

CATTAIL_PAL = {
    "d": "#334a20", "g": "#4a6a2b", "l": "#638a36", "h": "#7fa646",
    "s": "#3a2312", "S": "#563419", "B": "#704723", "H": "#8b5d31",
    "t": "#b6a27a", "T": "#d2c194",
}

CATTAIL_TOP = """
.......T........
.......t........
......sSs...T...
......SHs...t...
......BHs..sSs..
......BHs..BHs..
......BHs..BHs..
......sBs..BHs..
.......g...sBs..
.......g....g...
..h....g....g...
..l....g....g.h.
...l...g...g..l.
...l...g...g.l..
....l..g..g..l..
....l..g..g.l...
"""

CATTAIL_BOTTOM = """
....l..g..g.l...
.h..l..g..g.l...
.l...l.g..g.l...
.l...l.g.g.l..h.
..l..lgg.g.l..l.
..l...lg.g.l.l..
..ll..lgg.gl.l..
...l..lgggl.l...
...ll.dggglll...
....l.dgggdl....
....lldgggdl....
.....ldggdl.....
.....ldgggl.....
......dggg......
......dggd......
......dggd......
"""

CATTAIL_ITEM = """
........T.......
........t.......
.......sSs......
.......SHs......
.......BHs......
.......BHs......
.......BHs......
.......sBs......
...h....g.......
...l....g...h...
....l...g..l....
....l..gg..l....
.....l.gg.l.....
.....lgggl......
......dggd......
......dggd......
"""


def cattail_textures():
    pal = CATTAIL_PAL
    save(grid(rows_of(CATTAIL_TOP), pal), "block/cattail_top")
    save(grid(rows_of(CATTAIL_BOTTOM), pal), "block/cattail_bottom")
    save(grid(rows_of(CATTAIL_ITEM), pal), "item/cattail")


CRANBERRY_PAL = {
    "d": "#25401f", "g": "#355a2b", "G": "#467536", "l": "#5a8f41", "s": "#5b2b20",
    "r": "#620b17", "R": "#8f1325", "e": "#b8253a", "w": "#e8737f",
    "p": "#c48f8a", "P": "#e2b9ae",
}

CRANBERRY_STAGES = [
"""
................
................
................
................
................
................
................
................
................
................
................
.......G........
.....lGg.l......
......gGl.......
.......s........
.......s........
""",
"""
................
................
................
................
................
................
................
................
................
......lG........
....lGgGl.lG....
...GgdGgGlgG....
....GgGdgGgdl...
...lgdGsGgdG....
.....gdsdgG.....
.......s........
""",
"""
................
................
................
................
................
................
................
.......lG.......
....lGgGlPgG....
...GgdPgGlgdl...
..lGgGgdGgPgGl..
...gPdGgsgGdg...
..lGgdgGsdPgG...
...gdGPgsGgd....
.....gdgsdg.....
.......s........
""",
"""
................
................
................
................
................
................
................
.....lG.lG......
...lGgewGlgel...
..GgReGgRwgGRd..
..lgRRgdGeRgGl..
..GeRgwGgRRdeG..
..lgRRdgReGgRRl.
...dgGeRsgRegd..
....gdRRsgdg....
.......s........
""",
]


def cranberry_textures():
    for age, text in enumerate(CRANBERRY_STAGES):
        save(grid(rows_of(text), CRANBERRY_PAL), f"block/cranberry_bush_stage{age}")
    berries = """
................
................
..........gl....
.........gGl....
........sg......
.......s.s......
.....ree.s......
....rRewR.ree...
....rRRRRrRewR..
.....rRRrrRRRR..
......rrreeRRr..
.....reewRrrr...
....rRewRR......
....rRRRRr......
.....rrrr.......
................
"""
    save(grid(rows_of(berries), CRANBERRY_PAL), "item/cranberries")


ASTER = """
................
................
....v.p..v......
.....pPpP...v...
...vpPyYPpv.....
....pPYyPp......
...v.pPpPv......
.....v.g.p......
.......g........
.......g..pv....
.......g.vPp....
...l...g..p.....
..lLl..g........
...lL.lg........
.....lLg........
.......g........
"""


def aster_textures():
    pal = {"v": "#55298a", "p": "#7a48b4", "P": "#a173d8", "y": "#d7a325", "Y": "#f0cb46",
           "g": "#3f6c2a", "l": "#3f6c2a", "L": "#5a9440"}
    save(grid(rows_of(ASTER), pal), "block/aster")


GOLDENROD_TOP = """
.......y.Y......
.....Y.yY.y.....
....y.YyoY.Y....
...Y.yoy.oy.Y...
..y.oYo.g.oYy...
...oy..g..yo.Y..
..Yo..g..g..oy..
..y...g..g...o..
......g..g......
.....g....g.....
.....g....g.....
....l.g..g.l....
....Ll.g.g.Ll...
.....Ll.gg.l....
.......gg.......
.......g........
"""

GOLDENROD_BOTTOM = """
.......g........
......lg........
.....Ll.g.......
.......gLl......
....l..g..Ll....
...Ll..g........
....Llgg........
......gg.lL.....
.......gLl......
..l....g........
..Ll..gg........
...Llg.g..l.....
.....gg.gLl.....
.......gg.......
.......g........
.......g........
"""


def goldenrod_textures():
    pal = {"o": "#a87a10", "y": "#cc9e1d", "Y": "#ebc43a", "g": "#41702b", "l": "#3c6527", "L": "#5c9542"}
    save(grid(rows_of(GOLDENROD_TOP), pal), "block/goldenrod_top")
    save(grid(rows_of(GOLDENROD_BOTTOM), pal), "block/goldenrod_bottom")


# ----------------------------------------------------------------------------------------------------------------
# Camping blocks
# ----------------------------------------------------------------------------------------------------------------

def antler_material():
    pal = ramp("#6f5c40", "#8f7a58", "#a8946f", "#bfaa84", "#d4c19b", "#e6d7b5")
    rng = random.Random(5150)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = pal[rng.choice((2, 3, 3, 4))]
    # grooves running along the antler
    for x in range(0, 16, 3):
        for y in range(16):
            if rng.random() < 0.6:
                px[(x + (y // 5)) % 16, y] = pal[rng.choice((0, 1))]
    for _ in range(12):
        px[rng.randrange(16), rng.randrange(16)] = pal[5]
    return img


def iron(seed, base_tones, sheen=True):
    pal = ramp("#17171a", "#202024", "#29292e", "#323238", "#3c3c43", "#4a4a52", "#5c5c66")
    rng = random.Random(seed)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = pal[rng.choice(base_tones)]
    if sheen:
        for y in range(16):
            px[3, y] = pal[min(6, base_tones[-1] + 1)] if rng.random() < 0.7 else px[3, y]
            px[4, y] = pal[min(6, base_tones[-1])] if rng.random() < 0.5 else px[4, y]
    return img, pal


def cooking_pot_textures():
    side, pal = iron(81, (2, 3, 3, 4))
    px = side.load()
    for x in range(16):
        # rim band at the top of the visible wall (walls cover texture rows 6..15)
        px[x, 6] = pal[6] if x % 5 else pal[5]
        px[x, 7] = pal[5] if x % 4 else pal[4]
        px[x, 8] = pal[1]
        px[x, 15] = pal[1]
    for x in (2, 8, 13):
        px[x, 11] = pal[6]
    save(side, "block/cooking_pot_side")
    top, pal = iron(82, (4, 5, 5), sheen=False)
    save(top, "block/cooking_pot_top")
    inner, _ = iron(83, (0, 1, 1, 2), sheen=False)
    save(inner, "block/cooking_pot_inner")
    bottom, _ = iron(84, (1, 2, 2), sheen=False)
    save(bottom, "block/cooking_pot_bottom")
    handle, _ = iron(85, (4, 5, 6), sheen=False)
    save(handle, "block/cooking_pot_handle")

    # Animated liquids: 4 frames stacked vertically
    rng = random.Random(90)
    water_pal = ramp("#21488f", "#2a57a6", "#3466b9", "#4579c9", "#6a98dc")
    water = Image.new("RGBA", (16, 64))
    wp = water.load()
    for f in range(4):
        for y in range(16):
            for x in range(16):
                wave = ((x + y * 2 + f * 3) % 7)
                tone = 2 if wave < 3 else (1 if wave < 5 else 3)
                if rng.random() < 0.08:
                    tone = 4
                wp[x, f * 16 + y] = water_pal[tone]
    save(water, "block/cooking_pot_water")
    save_mcmeta("block/cooking_pot_water", 6)

    stew_pal = ramp("#4f2d14", "#633a1b", "#784824", "#8d582e")
    bits = [hexc("#d9822b"), hexc("#e6a23c"), hexc("#5d8c2f"), hexc("#d8c38a"), hexc("#a7262b")]
    stew = Image.new("RGBA", (16, 64))
    sp = stew.load()
    base_bits = [(rng.randrange(16), rng.randrange(16), rng.choice(bits)) for _ in range(14)]
    for f in range(4):
        for y in range(16):
            for x in range(16):
                tone = rng.choice((1, 2, 2, 3))
                sp[x, f * 16 + y] = stew_pal[tone]
        for (bx, by, c) in base_bits:
            sp[(bx + f) % 16, f * 16 + (by + (f % 2)) % 16] = c
        # a bubble or two
        for _ in range(2):
            bx, by = rng.randrange(1, 15), rng.randrange(1, 15)
            sp[bx, f * 16 + by] = hexc("#a87444")
            sp[bx + 1, f * 16 + by] = hexc("#bf8a58")
    save(stew, "block/cooking_pot_stew")
    save_mcmeta("block/cooking_pot_stew", 8)


# ----------------------------------------------------------------------------------------------------------------
# Items
# ----------------------------------------------------------------------------------------------------------------

ACORN = """
................
................
................
.........ss.....
........s.......
.....cCCCCc.....
....cCkCkCCc....
....cCCkCCkc....
.....ccccccc....
.....bBBBBb.....
.....bBHBBb.....
.....bBHBBb.....
......bBBb......
.......bb.......
................
................
"""

ANTLER = """
................
.....h..........
.....h.....h....
.....h....h.....
...h.hm..h......
....hhm.hm......
......mhm.......
......mm..h.....
.....mm..hm.....
....mm..hm......
....m.hmm.......
...mm.mm........
...m.mm.........
..mmmm..........
..Dmm...........
................
"""

WALKING_STICK = """
............kK..
...........kKKk.
...........KKKk.
..........kKkk..
.........kKk....
........kKk.....
.......lLl......
......lLLl......
.....lLl........
....kKk.........
...kKk..........
..kKk...........
.kKk............
kKk.............
Kk..............
................
"""


def item_textures():
    save(grid(rows_of(ACORN), {"s": "#4b3218", "c": "#5e4024", "C": "#7d5a33", "k": "#9c7646",
                               "b": "#7a4a1c", "B": "#9c6527", "H": "#c4893e"}), "item/acorn")
    save(grid(rows_of(ANTLER), {"h": "#e6d7b5", "m": "#bfa982", "D": "#7a6646"}), "item/antler")
    save(grid(rows_of(WALKING_STICK), {"K": "#8a6239", "k": "#4e3420", "L": "#6b3a1f", "l": "#8a4e2b"}), "item/walking_stick")


def stew_contents():
    """Overlays drawn on top of the vanilla bowl; only the bowl's inner area (and a few chunks above it)."""
    inner = {6: range(5, 11), 7: range(3, 13), 8: range(3, 13), 9: range(5, 11)}
    recipes = {
        # base tones, chunk colours, chunks poking over the rim
        "forest_stew": (("#5e3a1c", "#734a26", "#8a5a2f"), ("#c7a46a", "#d9b98a", "#4f7d2a", "#a35e2c"),
                        [(6, 5, "#c7a46a"), (9, 5, "#a35e2c")]),
        "hearty_stew": (("#6b2a1a", "#813622", "#99432a"), ("#d47a2c", "#e7b257", "#5b3220", "#b0402c"),
                        [(5, 5, "#5b3220"), (7, 5, "#d47a2c"), (10, 5, "#5b3220")]),
        "pumpkin_soup": (("#c0651c", "#d9792a", "#e88f38"), ("#f2c070", "#f7e2b5", "#6c8a2c"),
                         [(7, 5, "#6c8a2c")]),
        "berry_compote": (("#5b0f2a", "#741a36", "#8c2240"), ("#b8253a", "#e8737f", "#2e4ea0", "#9b2a7c"),
                          [(6, 5, "#b8253a"), (8, 5, "#2e4ea0")]),
    }
    for name, (base, chunks, over) in recipes.items():
        rng = random.Random(hash(name) & 0xFFFF)
        img = Image.new("RGBA", (16, 16))
        px = img.load()
        for y, xs in inner.items():
            for x in xs:
                px[x, y] = hexc(base[rng.choice((0, 1, 1, 2))] if y > 6 else base[2])
        for _ in range(7):
            y = rng.choice((6, 7, 7, 8))
            x = rng.choice(list(inner[y]))
            px[x, y] = hexc(rng.choice(chunks))
        for x, y, c in over:
            px[x, y] = hexc(c)
        save(img, f"item/{name}_contents")


BANNER_PATTERN_ITEM = """
................
..rRRRRRRRRRr...
..rWWWWWWWWWr...
...WWWWWWWWW....
...WWaWWWaWW....
...WaWaWaWaW....
...WWaaWaaWW....
...WWWaaaWWW....
...WWWWaWWWW....
...WWWWaWWWW....
...WWWWWWWWW....
...WWWWWWWWW....
..rWWWWWWWWWr...
..rRRRRRRRRRr...
................
................
"""


def paper_background():
    """Parchment for explorer maps (our own drawing)."""
    pal = {"p": "#6c5733", "P": "#8a7246", "c": "#e8dbb4", "d": "#cdb98b"}
    rows = [
        "................",
        ".ppPPPPPPPPPPpp.",
        ".pPccccccccccPp.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PccccccccccccP.",
        ".PcccccccccccdP.",
        ".pPdccccccccddp.",
        "..pPPPPPPPPPPp..",
        "................",
    ]
    return grid(rows, pal)


def lookout_icon(img, ox, oy, scale_small=False):
    """A fire lookout tower: red roof, cabin with a window band, braced stilts. Black outline like vanilla icons."""
    px = img.load()
    k, r, w = hexc("#1e1a14"), hexc("#a8432f"), hexc("#f2ead2")
    pts = []
    pts += [(3, 0, k), (4, 0, k)]
    pts += [(2, 1, k), (3, 1, r), (4, 1, r), (5, 1, k)]
    pts += [(1, 2, k), (2, 2, r), (3, 2, r), (4, 2, r), (5, 2, r), (6, 2, k)]
    pts += [(x, 3, k) for x in range(0, 8)]
    pts += [(1, 4, k), (2, 4, w), (3, 4, w), (4, 4, w), (5, 4, w), (6, 4, k)]
    pts += [(x, 5, k) for x in range(1, 7)]
    pts += [(2, 6, k), (5, 6, k), (2, 7, k), (3, 7, k), (4, 7, k), (5, 7, k), (2, 8, k), (5, 8, k)]
    pts += [(1, 9, k), (6, 9, k)]
    for x, y, c in pts:
        px[ox + x, oy + y] = c


def map_and_pattern_items():
    img = paper_background()
    lookout_icon(img, 4, 3)
    save(img, "item/ranger_lookout_map")
    # 8x8 map decoration
    deco = Image.new("RGBA", (8, 8))
    dp = deco.load()
    k, r, w, g = hexc("#000000"), hexc("#a8432f"), hexc("#ffffff"), hexc("#7a7a7a")
    rows = [
        "...kk...",
        "..krrk..",
        ".krrrrk.",
        "kkkkkkkk",
        ".kwwwwk.",
        ".kkkkkk.",
        ".kgkkgk.",
        "kk....kk",
    ]
    cmap = {"k": k, "r": r, "w": w, "g": g}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                dp[x, y] = cmap[ch]
    save(deco, "map/decorations/ranger_lookout")
    pal2 = {"r": "#6b4a2a", "R": "#8a6339", "W": "#e9e0c8", "a": "#5a4128"}
    save(grid(rows_of(BANNER_PATTERN_ITEM), pal2), "item/antlers_banner_pattern")


def main():
    save(thatch_side(), "block/thatch_side")
    save(thatch_top(), "block/thatch_top")
    save(peat(), "block/peat")
    save(peat_bricks(), "block/peat_bricks")
    cattail_textures()
    cranberry_textures()
    aster_textures()
    goldenrod_textures()
    save(antler_material(), "block/antler_chandelier")
    cooking_pot_textures()
    item_textures()
    stew_contents()
    map_and_pattern_items()
    print("textures written to", TEX)


if __name__ == "__main__":
    main()
