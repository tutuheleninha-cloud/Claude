# Auto Rebalance — a PvZ2 Gardendless mod

Rebalances plants, zombies, and levels in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2). **Plants and
zombies are now built directly from the user's real extracted game data**
(`PlantFeatures.json`/`PlantProps.json`/`ZombieFeatures.json`/`ZombieProps.json`);
only the level/wave structure is still synthetic — see the confidence
breakdown below. Three independent, already-finished patches — nothing to
build or run:

- **`jsons/objects/PlantProps.json`** — adjusts each of 163 real plants'
  `SunCost` so its (offense + defense) value *per sun spent* trends toward
  the roster average, instead of hand-picking "X is OP." Combat stats
  (damage, cooldown, health) are untouched — only cost changes.
- **`jsons/objects/ZombieProps.json`** — adjusts each of 159 real zombies'
  `WavePointCost` — the real field that controls how many of a zombie can
  appear per wave — toward the roster's average threat-per-point, the same
  normalization approach as the plant pass, independent of it.
- **`jsons/worldmap/WorldMap.json`** — rescales zombie counts within 28
  synthetic levels' waves so difficulty ramps smoothly, using the *real*
  per-zombie threat weights from the same uploaded data.

See `jsons/objects/plants-changes.md`, `jsons/objects/zombies-changes.md`,
and `jsons/worldmap/levels-changes.md` for a plain before/after table of
every value this mod changes.

## Confidence, by piece

1. **Plants: real.** 163 real plants (of 213 total; the 14-plant Mints
   family and 36 non-independent variants/sub-effects excluded), with real
   `SunCost`/`Toughness`/`Cooldown`/`Damage`/`Family` values. `objclass`
   confirmed `PlantProperties`.
2. **Zombies: real.** 159 real zombies (of 382 total; restricted to the 14
   core worlds — holiday/event categories like Birthday, Valentine's,
   Feastivus, Sportzball, Easter, St. Patrick's, Lunar New Year excluded
   as not part of the main progression — and to base forms, excluding
   `_armor1/2/4`, `_flag`, `_flag_veteran`, `_imp`, `_gargantuar` overlay
   variants of the same zombie). Real `Toughness`/`EatDPS`/`WalkSPS`/
   `WavePointCost` values. `objclass` confirmed `ZombieProperties`.
3. **Levels: still synthetic.** No file among what's been uploaded
   contains actual per-level wave composition — `LevelModules.json` (also
   uploaded) turned out to be shared game-mechanic building blocks (lawn
   themes, mower types, loot tables, danger-room generators) referenced
   *by* level files, not the level files themselves. So the 28-level, 2
   levels-per-world structure below is still fabricated — but it now uses
   real zombie codenames and real per-zombie threat weights (pulled from
   the same real data as the zombie rebalance above), instead of the old
   version's fake `ZombieBasic`-style names, which would have silently
   mismatched the now-real `ZombieProps.json` patch.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/auto-rebalance/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level so the new sun costs, zombie WavePointCost, and wave
   pacing take effect.

## What's covered

**Plants (real, 163):** every plant in the uploaded data except the
14-plant Mints family (`SunCost: 0` — fed to other plants, not planted
directly) and 36 entries with no independent existence (marigold color
variants, zombie-potion items, tool-projectile sub-objects, growth-stage
forms, or missing `PlantProps` data).

**Zombies (real, 159):** every zombie in the uploaded data restricted to
14 core worlds (`frontyard, egypt, pirate, cowboy, dark, future, ice,
modern, kongfu, beach, lostcity, eighties, dino, sky` — `market` and
`water` have real zombies too but too few to be worth a level grouping)
and to base forms only.

**Levels (synthetic structure, real names):** 2 levels per world × 14
worlds = 28 levels, each with 3 waves in a deliberately uneven shape
(heavy open → light middle → spiky flag wave) so the smoothing pass has
real work to do — using each world's first 4 real zombies.

## Folder contents

```
pack.json                          - GP-Next mod manifest (name/version/author)
jsons/objects/PlantProps.json      - rebalanced plant SunCost (real 163-plant roster)
jsons/objects/plants-changes.md    - before/after table for plants
jsons/objects/ZombieProps.json     - rebalanced zombie WavePointCost (real 159-zombie roster)
jsons/objects/zombies-changes.md   - before/after table for zombies
jsons/worldmap/WorldMap.json       - rebalanced level wave zombie counts (synthetic levels, real zombies)
jsons/worldmap/levels-changes.md   - before/after table for levels
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
- [gp-next-datapack.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-datapack.md) — real `pack.json` template
- **User-uploaded `PlantFeatures.json`, `PlantProps.json`, `ZombieFeatures.json`, `ZombieProps.json`, `PlantTypes.json`, `ZombieTypes.json`, `LevelModules.json`** — real source of truth for the plant and zombie rebalance
