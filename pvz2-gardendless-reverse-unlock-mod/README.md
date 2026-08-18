# Reverse Almanac Order — a PvZ2 Gardendless mod

Reverses the full plant order in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2) — not just the
main-adventure per-level unlocks, but the whole Almanac-style roster: Main
Adventure (all 12 worlds), Epic Quest rewards, Ticket (Arena) Shop, and Gem
(premium) Shop. Zen Garden **Mint is deliberately excluded** — it's a
Zen-Garden-economy plant, not part of the unlock/Almanac progression this
mod reverses. 61 plants total, whichever plant used to be first is now
last and vice versa.

Two independent, already-finished patches — nothing to build or run:

- **`jsons/features/PlantFeatures.json`** — `BASEUNLOCKLIST` and
  `SEEDCHOOSERDEFAULTORDER` set to the full 61-plant order, reversed.
- **`jsons/worldmap/WorldMap.json`** — for the Main-Adventure-only subset
  (Epic Quest / Ticket / Gem plants aren't tied to a specific level),
  reverses which level rewards which plant *globally* — level 1's reward
  becomes what used to be the very last level's reward, not just swapped
  within its own world.

See `jsons/features/almanac-order-changes.md` (full 61-plant before/after
table) and `jsons/worldmap/unlock-order-changes.md` (per-level before/after)
for exactly what changed.

## What changed from the previous version of this mod

The first version of this mod only reversed 8 plants (Ancient Egypt +
Pirate Seas) — it didn't account for Epic Quest, Ticket Shop, or Gem Shop
plants at all, so most of the real roster wasn't touched. This version
replaces that with the full Almanac-style list across all four acquisition
categories.

## ⚠️ Please read before installing

Same standing caveats as before, still true here:

1. **The plant field names are on solid ground.** `PlantFeatures.json`'s
   `BASEUNLOCKLIST` / `SEEDCHOOSERDEFAULTORDER` arrays, and the "plain
   overwrite on merge" behavior for basic-type array values, come from
   Gardendless's own published docs.
2. **The per-level `WorldMap.json` shape is a best-effort guess** (level
   `ID`, a `RewardPlants` field) since Gardendless doesn't publish its exact
   level-data schema. It may not load as-is.
3. **The roster itself is not extracted from your game.** I don't have
   access to Gardendless's actual current data files. The Main Adventure
   world/plant groupings reuse well-known classic-PvZ2 names; the Epic
   Quest / Ticket Shop / Gem Shop groupings are my best recollection of
   which real PvZ2 plants come from which acquisition method, which is
   lower-confidence the further from the base worlds you get. Gardendless
   itself may not include every plant listed, may categorize some
   differently, or may use different internal `CODENAME`s.

## What's covered (61 plants)

**Main Adventure** (12 worlds, in order): Ancient Egypt, Pirate Seas, Wild
West, Dark Ages, Far Future, Frostbite Caves, Lost City, Neon Mixtape
Tour, Jurassic Marsh, Big Wave Beach, Modern Day, Sky City — 48 plants.

**Epic Quest:** Toadstool, PerfumeShroom, AloeVera, ShrinkingViolet, PeaNut.

**Ticket Shop:** Parsnip, EMPeach, ConcussiveCoconut, SapFling.

**Gem Shop:** TitanFrost, GrapeShot, Spineapple, HighlandCabbage.

**Excluded on purpose:** Zen Garden Mint (per your request), plus any
other Zen-Garden-only or event/arena-exclusive plant not listed above.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/reverse-almanac-order/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level select / world map / seed chooser screens so the
   reversed order takes effect.

## Folder contents

```
pack.json                              - GP-Next mod manifest
jsons/features/PlantFeatures.json      - reversed BASEUNLOCKLIST + SEEDCHOOSERDEFAULTORDER (61 plants)
jsons/features/almanac-order-changes.md - full before/after table
jsons/worldmap/WorldMap.json           - reversed per-level plant rewards (Main Adventure only)
jsons/worldmap/unlock-order-changes.md - per-level before/after table
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
