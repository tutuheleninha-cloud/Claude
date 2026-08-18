# Reverse Almanac Order — a PvZ2 Gardendless mod

Reverses plant order in [PvZ2 Gardendless](https://pvzge.com/en/) (an
open-source, fan-made PC rewrite of Plants vs Zombies 2) three ways: the
seed-chooser display order, the Gem/Ticket Shop costs, and **where in the
game each plant is unlocked** — the plant you'd normally get from the very
first level of Ancient Egypt now comes from the very last Epic Quest
reward, and vice versa, across all 12 worlds + Epic Quest.

Three independent, already-finished patches — nothing to build or run:

- **`jsons/features/PlantFeatures.json`** — `SEEDCHOOSERDEFAULTORDER` set
  to the full 61-plant order, reversed.
- **`jsons/objects/StoreCommodityFeatures.json`** — swaps `CurrencyRequired`
  (cost) between the cheapest and priciest items in the Gem Shop and the
  Ticket Shop respectively.
- **`jsons/worldmap/gpn-worldmap.json`** — replaces the world map's
  progression (`mainline`) for all 12 Main Adventure worlds + Epic Quest,
  reversing which `plant`-type node grants which plant, globally across
  all 53 level/quest reward slots (not just within each world).

See `jsons/features/almanac-order-changes.md`,
`jsons/objects/shop-order-changes.md`, and
`jsons/worldmap/worldmap-changes.md` for exactly what changed in each file.

## 🛑 Back up your save before installing this

This directly quotes Gardendless's own docs on the world-map feature:
**"Users should back up saves before testing."** `gpn-worldmap.json` also
requires enabling **`worldmap-json` in the in-game Experimental settings**
before it does anything at all. Neither of those is me being cautious —
it's the mod author's own stated risk level for this specific feature.

## v4 → v5: why the per-level/Epic-Quest reversal is back

The previous version removed this because I hadn't confirmed the real
schema and didn't want to fabricate something that could silently corrupt
level progression. Since then I found the *actual* official example for
this feature (quoted from the docs source, not paraphrased):

```json5
{
  apiVersion: 1,
  worlds: {
    egypt: {
      map: {
        mode: 'replace',
        mainline: [
          { id: 'lvl-1', type: 'level', appearance: 'normal', levels: ['egypt1'], title: '1' }
        ]
      }
    }
  }
}
```

This confirms: the file path (`jsons/worldmap/gpn-worldmap.json`), the
root shape, the `egypt` world codename, and the `<worldcode><n>` level-ID
convention (e.g. `egypt1`, `egypt2`). `jsons/worldmap/gpn-worldmap.json`
in this mod follows that confirmed shape exactly, with `plant`-type nodes
(`{id, type: 'plant', plantReward: <codename>}`) inserted between level
nodes — one plant node per plant in this mod's roster — and their
`plantReward` values reversed globally across all 53 slots.

**What's still not confirmed, honestly:** the `egypt` codename and the
`<worldcode><n>` level-ID pattern come straight from the docs' own
example. The other 11 world codenames (`pirateseas`, `wildwest`, etc.) and
every specific level ID follow that same confirmed *pattern* but aren't
individually verified against your game — so `level`-type nodes for
worlds other than Egypt may reference level IDs that don't exist in your
install. If a level tile doesn't load, that's why. The `plant`-type reward
nodes don't depend on any external level data, so the actual "which plant
do I get" reversal should work even where a level tile doesn't render
correctly — but "should" is doing real work in that sentence, hence the
save backup.

## ⚠️ Please also read

1. **`SEEDCHOOSERDEFAULTORDER`** is a confirmed real field, plain array,
   fully overwritten on merge — the most solid part of this mod.
2. **`StoreCommodityFeatures.json`'s shape is confirmed**, but the
   `CurrencyRequired` starting values are illustrative placeholders
   (5/20/50/100 gems, 300/600/1200/2000 tickets), not your real prices.
3. **`BASEUNLOCKLIST` is deliberately not touched** — it's confirmed to
   mean "plants a brand-new save starts with," not a progression order, so
   reversing it wouldn't do what "reverse unlock order" asks for.
4. **The 61-plant roster is not extracted from your game.** Main Adventure
   world/plant groupings reuse well-known classic-PvZ2 names; Epic
   Quest/Ticket Shop/Gem Shop groupings are my best recollection of which
   real PvZ2 plants come from which acquisition method. Gardendless may
   not include every plant listed, or may use different `CODENAME`s.

## What's covered (61 plants, 53 reversed via the world map)

**Main Adventure** (12 worlds, in order): Ancient Egypt, Pirate Seas, Wild
West, Dark Ages, Far Future, Frostbite Caves, Lost City, Neon Mixtape
Tour, Jurassic Marsh, Big Wave Beach, Modern Day, Sky City — 48 plants,
2–5 per world, each behind its own level+plant node pair in the world map.

**Epic Quest:** Toadstool, PerfumeShroom, AloeVera, ShrinkingViolet, PeaNut
— represented as an `epicPortal` node leading to 5 quest levels, each
with its own plant reward.

**Ticket Shop:** Parsnip, EMPeach, ConcussiveCoconut, SapFling — cost
reversal only (not level-based, so not part of the world map).

**Gem Shop:** TitanFrost, GrapeShot, Spineapple, HighlandCabbage — cost
reversal only.

**Excluded on purpose:** Zen Garden Mint, plus any other Zen-Garden-only or
event/arena-exclusive plant not listed above.

## Installing the mod in-game

1. Back up your save (see above).
2. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/reverse-almanac-order/`.
3. Enable it from the in-game Patcher/GP-Next mod list.
4. Enable `worldmap-json` in the in-game **Experimental** settings page
   (required for `gpn-worldmap.json` to take effect at all).
5. Restart the world map / seed chooser / shop screens so the reversed
   order, costs, and unlock locations take effect.

## Folder contents

```
pack.json                                 - GP-Next mod manifest
jsons/features/PlantFeatures.json         - reversed SEEDCHOOSERDEFAULTORDER (61 plants)
jsons/features/almanac-order-changes.md   - full before/after table
jsons/objects/StoreCommodityFeatures.json - reversed Gem Shop + Ticket Shop costs
jsons/objects/shop-order-changes.md       - before/after table
jsons/worldmap/gpn-worldmap.json          - reversed world-map plant rewards (12 worlds + Epic Quest)
jsons/worldmap/worldmap-changes.md        - before/after table, per node
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/) (docs pages
  blocked from this environment; content below was reached via GitHub
  mirrors of the same docs source instead)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [pvzg_site — docs source (GitHub)](https://github.com/Gzh0821/pvzg_site)
- [gp-next-worldmap.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-worldmap.md) — source of the confirmed example above, the `worldmap-json` experimental-flag requirement, and the save-backup warning
- [gpn-worldmap.schema.json (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/.vuepress/public/jsons/schema/gpn-worldmap.schema.json) — confirms node types and the `mainline`/`branches`/"replace"-mode structure
- [gpn-plant-levels.schema.json (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/.vuepress/public/jsons/schema/gpn-plant-levels.schema.json) — confirms plant "levels" are a seed-packet power-up system, unrelated to roster unlocking
