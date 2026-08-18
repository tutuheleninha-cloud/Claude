# Reverse Almanac Order — a PvZ2 Gardendless mod

Reverses the full plant order in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2) — not just the
main-adventure per-level unlocks, but the whole Almanac-style roster: Main
Adventure (all 12 worlds), Epic Quest rewards, Ticket (Arena) Shop, and Gem
(premium) Shop. Zen Garden **Mint is deliberately excluded** — it's a
Zen-Garden-economy plant, not part of the unlock/Almanac progression this
mod reverses. 61 plants total, whichever plant used to be first is now
last and vice versa.

Four independent, already-finished patches — nothing to build or run:

- **`jsons/features/PlantFeatures.json`** — `BASEUNLOCKLIST` and
  `SEEDCHOOSERDEFAULTORDER` set to the full 61-plant order, reversed. This
  is the seed-chooser *display* order across everything you own — it does
  not by itself reverse the Gem Shop, Ticket Shop, or Epic Quest structures
  below; those needed their own patches.
- **`jsons/worldmap/WorldMap.json`** — for the Main-Adventure-only subset
  (Epic Quest / Ticket / Gem plants aren't tied to a specific level),
  reverses which level rewards which plant *globally* — level 1's reward
  becomes what used to be the very last level's reward, not just swapped
  within its own world.
- **`jsons/objects/StoreCommodityFeatures.json`** — reverses the listing
  order *within* the Gem Shop and *within* the Ticket Shop themselves
  (not just their position in the flat seed-chooser list above).
- **`jsons/features/EpicQuestRewards.json`** — reverses the order Epic
  Quest rewards are handed out in.

See `jsons/features/almanac-order-changes.md` (full 61-plant before/after),
`jsons/worldmap/unlock-order-changes.md` (per-level before/after),
`jsons/objects/shop-order-changes.md` (Gem/Ticket shop slots before/after),
and `jsons/features/epic-quest-order-changes.md` (quest reward slots
before/after) for exactly what changed in each file.

## What changed across the previous two versions of this mod

- **v1** only reversed 8 plants (Ancient Egypt + Pirate Seas) — no Epic
  Quest, Ticket Shop, or Gem Shop plants at all.
- **v2** added those plants to the flat 61-plant Almanac order, but that
  flat order only controls the seed-chooser *display* — it left the Gem
  Shop's own listing order, the Ticket Shop's own listing order, and the
  Epic Quest reward sequence itself untouched, because those live in
  separate data structures.
- **v3 (this version)** adds `StoreCommodityFeatures.json` and
  `EpicQuestRewards.json` so those three structures are now reversed in
  their own right, not just repositioned inside the seed-chooser list.

## ⚠️ Please read before installing

Same standing caveats as before, still true here:

1. **The plant field names are on solid ground.** `PlantFeatures.json`'s
   `BASEUNLOCKLIST` / `SEEDCHOOSERDEFAULTORDER` arrays, and the "plain
   overwrite on merge" behavior for basic-type array values, come from
   Gardendless's own published docs.
2. **The per-level `WorldMap.json` shape is a best-effort guess** (level
   `ID`, a `RewardPlants` field) since Gardendless doesn't publish its exact
   level-data schema. It may not load as-is.
3. **`StoreCommodityFeatures.json` and `EpicQuestRewards.json` are the
   least certain files in this mod, on two different axes:**
   - `StoreCommodityFeatures.json`'s top-level `Plants`/`Upgrade`/`Gem`/
     `Coin`/`Zen` arrays are confirmed to exist by Gardendless's docs, but
     a `Ticket` array is *not* confirmed — I added it as the most plausible
     parallel, since I found no public schema for how Arena tickets are
     spent. More importantly, the docs describe merging as matching
     objects **by `CODENAME` and overwriting their fields** — not as
     "array position determines display order." Simply reordering the
     entries in this patch may not actually reorder the shop in-game; it's
     the most plausible mechanism available, not a confirmed one.
   - `EpicQuestRewards.json` and its `EPICQUESTREWARDORDER` field are an
     outright guess at the file/field name — nothing public documents how
     Epic Quest rewards are sequenced. It mirrors `BASEUNLOCKLIST`'s
     confirmed "plain array, overwritten wholesale" shape on the theory
     that a similarly-named field likely works the same way, but that's an
     analogy, not a citation.
4. **The roster itself is not extracted from your game.** I don't have
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
pack.json                                  - GP-Next mod manifest
jsons/features/PlantFeatures.json          - reversed BASEUNLOCKLIST + SEEDCHOOSERDEFAULTORDER (61 plants)
jsons/features/almanac-order-changes.md    - full before/after table
jsons/features/EpicQuestRewards.json       - reversed Epic Quest reward order (guessed schema)
jsons/features/epic-quest-order-changes.md - before/after table
jsons/worldmap/WorldMap.json               - reversed per-level plant rewards (Main Adventure only)
jsons/worldmap/unlock-order-changes.md     - per-level before/after table
jsons/objects/StoreCommodityFeatures.json  - reversed Gem Shop + Ticket Shop listing order (guessed schema)
jsons/objects/shop-order-changes.md        - before/after table
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
