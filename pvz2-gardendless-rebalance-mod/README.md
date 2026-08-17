# Auto Rebalance — a PvZ2 Gardendless mod

Rebalances plants, zombies, and levels in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2). Three
independent, already-finished patches — nothing to build or run:

- **`jsons/objects/PlantProps.json`** — adjusts each plant's `SunCost` so its
  (offense + defense) value *per sun spent* trends toward the roster
  average, instead of hand-picking "X is OP." A plant that already gives far
  more power than its current cost gets pricier; an overpriced plant gets
  cheaper. Combat stats (damage, cooldown, health) are untouched, so plants
  keep their feel — only what they cost changes.
- **`jsons/objects/ZombieProps.json`** — adjusts each zombie's `Toughness` so
  its overall threat score (built from toughness, damage, and speed)
  converges toward the roster average, independent of the plant pass.
- **`jsons/worldmap/WorldMap.json`** — rescales zombie counts within each
  level's waves so difficulty ramps smoothly (no wave is more than 60%
  harder than the last, and none stalls below 90% of it), computed from
  the *original* zombie threat values — independent of the zombie pass
  above, not chained to it.

Each of the three areas is a self-contained change: you can drop in all
three files, or delete any one of them from your install, without the
others breaking.

See `jsons/objects/plants-changes.md`, `jsons/objects/zombies-changes.md`,
and `jsons/worldmap/levels-changes.md` for a plain before/after table of
every value this mod changes.

## ⚠️ Please read before installing

This pack targets Gardendless's documented **GP-Next** mod system
(`packs/<name>/pack.json` + `jsons/...`, merging by matching
`aliases`/`CODENAME`). Two honesty notes:

1. **The plant field names are on solid ground.** `PlantProps.json`'s
   `objects` array with `aliases` / `objclass` / `objdata`, and the
   `Damage` / `Cooldown` / `CooldownFrom` / `SunCost` / `Toughness` fields,
   come from Gardendless's own published docs
   (`pvzg_site/src/en/guide/mod/format.md`).
2. **Everything else is a best-effort guess.** No public schema for zombie
   stats or level/wave data was reachable while building this (the docs
   site, `pvzge.com`, is blocked from the environment this was built in),
   so `Toughness`/`Damage`/`Speed` for zombies and the `Worlds → Levels →
   Waves → Zombies{codename: count}` level shape are guesses mirrored from
   the confirmed plant schema. They may not match your install's real field
   names — if a file doesn't take effect in-game, that's the most likely
   reason.
3. **The base numbers are a reference roster, not extracted from your
   game.** The `SunCost`/`Damage`/`Toughness` starting values this mod's
   math ran against are well-known, public classic-PvZ2 numbers for a
   ~15-plant / 8-zombie / 4-level slice (Ancient Egypt & Pirate Seas), not
   pulled from Gardendless's actual current data files — I don't have
   access to those. If Gardendless has since added, removed, or re-tuned
   any of the entries below, this mod won't know about it, and it doesn't
   cover plants/zombies/levels outside that list.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/auto-rebalance/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level so the new sun costs, zombie toughness, and wave
   pacing take effect.

## What's covered

**Plants:** PeaShooter, SunFlower, WallNut, CherryBomb, PotatoMine,
SnowPea, Chomper, Repeater, Threepeater, Bloomerang, IcebergLettuce,
BonkChoy, SpikeweedTrap, TallNut, SplitPea.

**Zombies:** ZombieBasic, ZombieConehead, ZombieBuckethead, ZombieFlag,
ZombiePole, ZombieDoorRolling, ZombieSnorkel, ZombieJackInBox.

**Levels:** 1_1, 1_2 (Ancient Egypt), 2_1, 2_2 (Pirate Seas).

## Folder contents

```
pack.json                          - GP-Next mod manifest (name/version/author)
jsons/objects/PlantProps.json      - rebalanced plant SunCost
jsons/objects/plants-changes.md    - before/after table for plants
jsons/objects/ZombieProps.json     - rebalanced zombie Toughness
jsons/objects/zombies-changes.md   - before/after table for zombies
jsons/worldmap/WorldMap.json       - rebalanced level wave zombie counts
jsons/worldmap/levels-changes.md   - before/after table for levels
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
