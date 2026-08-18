# Reverse Almanac Order — a PvZ2 Gardendless mod

Reverses plant order in [PvZ2 Gardendless](https://pvzge.com/en/) (an
open-source, fan-made PC rewrite of Plants vs Zombies 2): the seed-chooser
display order across the full 61-plant roster (Main Adventure + Epic Quest
+ Ticket Shop + Gem Shop, excluding Zen Garden Mint), plus the Gem Shop
and Ticket Shop's own purchase costs.

Two independent, already-finished patches — nothing to build or run:

- **`jsons/features/PlantFeatures.json`** — `SEEDCHOOSERDEFAULTORDER` set
  to the full 61-plant order, reversed.
- **`jsons/objects/StoreCommodityFeatures.json`** — swaps `CurrencyRequired`
  (cost) between the cheapest and priciest items in the Gem Shop and the
  Ticket Shop respectively, so what used to be the most expensive plant is
  now the cheapest, and vice versa.

See `jsons/features/almanac-order-changes.md` and
`jsons/objects/shop-order-changes.md` for exactly what changed.

## v3 → v4: what this rebuild fixes

I went and actually verified the mod's assumptions against Gardendless's
real, published JSON Schema files (found on GitHub, not the docs site,
which stays blocked from this environment — see Sources). Three things
in the previous version turned out to be wrong or unsafe, and are fixed
here:

1. **`BASEUNLOCKLIST` doesn't mean what I treated it as.** It's confirmed
   to hold the plants a *brand-new save* starts with — not an ordered
   unlock progression. Reversing it didn't "reverse unlock order"; it just
   changed which plants a fresh game begins with, which isn't what was
   asked for. **Dropped from this version.**
2. **The per-level and Epic Quest reward files (`WorldMap.json`,
   `EpicQuestRewards.json`) are removed, not just corrected.** The real
   schema (`gpn-worldmap.schema.json`) represents level/gift/plant/
   upgrade/Epic-Quest nodes as one `mainline` array per world, and that
   array is applied in **`"mode": "replace"`** — the whole array gets
   swapped in wholesale, not merged field-by-field like everything else
   in this mod. Shipping a reversed `mainline` would mean fabricating the
   *complete* real node list (every level, gift box, and portal, correctly
   ordered) for all 12 worlds. I don't have that data, and guessing at it
   risks silently deleting or reordering real levels — actually breaking
   your save's progression, not just reordering which plant you get. That
   risk isn't worth taking for a mod that's supposed to be cosmetic, so
   this version doesn't touch per-level or Epic Quest rewards at all.
   *(If you can export your own `mainline` JSON from the in-game Patcher's
   "Open Folder" option and share it, I can build a correct, safe reversal
   from your real data instead of guessing.)*
3. **`StoreCommodityFeatures.json`'s real shape is different than I had
   it.** It's confirmed to be a single flat `Plants` array of
   `{CommodityType, CommodityName, CurrencyType, CurrencyRequired}`
   entries (lowercase `CommodityName`, e.g. `"snowpea"`) — not the separate
   `Gem`/`Ticket` arrays this mod shipped with before. Rebuilt to match,
   and switched the reversal mechanism from "reorder the array" (never
   confirmed to do anything — merging matches by `CommodityName`, not
   position) to "swap the `CurrencyRequired` cost field between items,"
   which **is** the confirmed-safe field-overwrite mechanism used
   everywhere else in this mod.

## ⚠️ Please read before installing

1. **`SEEDCHOOSERDEFAULTORDER` is a confirmed real field** — a plain
   string array, fully overwritten on merge. This is the most solid part
   of the mod.
2. **`StoreCommodityFeatures.json`'s shape is confirmed**, but the
   `CurrencyRequired` values it starts from are illustrative placeholders
   (5/20/50/100 gems, 300/600/1200/2000 tickets) — I don't have your
   game's real prices, so the "reversal" is a swap relative to those
   placeholders, not your actual shop costs. See
   `jsons/objects/shop-order-changes.md` for exactly what values this
   patch will set.
3. **The 61-plant roster itself is not extracted from your game.** Main
   Adventure world/plant groupings reuse well-known classic-PvZ2 names;
   Epic Quest/Ticket Shop/Gem Shop groupings are my best recollection of
   which real PvZ2 plants come from which acquisition method, lower
   confidence the further from the base worlds you get. Gardendless may
   not include every plant listed, or may use different `CODENAME`s.

## What's covered (61 plants)

**Main Adventure** (12 worlds, in order): Ancient Egypt, Pirate Seas, Wild
West, Dark Ages, Far Future, Frostbite Caves, Lost City, Neon Mixtape
Tour, Jurassic Marsh, Big Wave Beach, Modern Day, Sky City — 48 plants.

**Epic Quest:** Toadstool, PerfumeShroom, AloeVera, ShrinkingViolet, PeaNut.

**Ticket Shop:** Parsnip, EMPeach, ConcussiveCoconut, SapFling.

**Gem Shop:** TitanFrost, GrapeShot, Spineapple, HighlandCabbage.

**Excluded on purpose:** Zen Garden Mint, plus any other Zen-Garden-only or
event/arena-exclusive plant not listed above. **Not touched at all:**
per-level unlock rewards and Epic Quest reward assignment (see fix #2
above for why).

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/reverse-almanac-order/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the seed chooser / shop screens so the reversed order and
   costs take effect.

## Folder contents

```
pack.json                                 - GP-Next mod manifest
jsons/features/PlantFeatures.json         - reversed SEEDCHOOSERDEFAULTORDER (61 plants)
jsons/features/almanac-order-changes.md   - full before/after table
jsons/objects/StoreCommodityFeatures.json - reversed Gem Shop + Ticket Shop costs
jsons/objects/shop-order-changes.md       - before/after table
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/) (docs pages
  blocked from this environment)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [pvzg_site — docs source (GitHub)](https://github.com/Gzh0821/pvzg_site)
- [gpn-worldmap.schema.json (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/.vuepress/public/jsons/schema/gpn-worldmap.schema.json) — confirms the `mainline`/`branches`/"replace" mode structure behind fix #2
- [gpn-plant-levels.schema.json (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/.vuepress/public/jsons/schema/gpn-plant-levels.schema.json) — confirms plant "levels" are a seed-packet power-up system, unrelated to roster unlocking
