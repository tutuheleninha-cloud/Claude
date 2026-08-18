# Auto Rebalance — a PvZ2 Gardendless mod

Rebalances plants, zombies, and levels in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2). **Plants are
now built directly from the user's real extracted `PlantFeatures.json` +
`PlantProps.json`** (163 real plants); zombies and levels are still
best-effort estimates (48 zombies, 24 levels across 12 estimated worlds
plus 4 premium plants) — see the confidence breakdown below. Three
independent, already-finished patches — nothing to build or run:

- **`jsons/objects/PlantProps.json`** — adjusts each real plant's
  `SunCost` so its (offense + defense) value *per sun spent* trends toward
  the roster average, instead of hand-picking "X is OP." A plant that
  already gives far more power than its current cost gets pricier; an
  overpriced plant gets cheaper. Combat stats (damage, cooldown, health)
  are untouched, so plants keep their feel — only what they cost changes.
- **`jsons/objects/ZombieProps.json`** — adjusts each (estimated) zombie's
  `Toughness` so its overall threat score (built from toughness, damage,
  and speed) converges toward the roster average, independent of the
  plant pass.
- **`jsons/worldmap/WorldMap.json`** — rescales zombie counts within each
  (estimated) level's waves so difficulty ramps smoothly, computed from
  the *original* zombie threat values — independent of the zombie pass.

See `jsons/objects/plants-changes.md`, `jsons/objects/zombies-changes.md`,
and `jsons/worldmap/levels-changes.md` for a plain before/after table of
every value this mod changes.

## Confidence, by piece

1. **Plants: real.** 163 real plants (of 213 total; the 14-plant Mints
   family and 36 non-independent variants/sub-effects excluded), with real
   `SunCost`/`Toughness`/`Cooldown`/`Damage`/`Family` values from the
   user's uploaded `PlantFeatures.json` + `PlantProps.json`. `objclass` is
   confirmed `PlantProperties` (an earlier version of this mod guessed
   `Plant`, which was wrong).
2. **Zombies: estimated.** No real zombie data has been provided (the
   upload only covered plants). The 48-zombie/12-world roster still uses
   the tier + archetype formula from earlier versions — see the old
   confidence notes below. If you can export a real `ZombieFeatures.json`/
   `ZombieProps.json`, the zombie pass can be rebuilt on real data the
   same way plants just were.
3. **Levels: estimated**, for the same reason — no real world-map/level
   data has been provided for this mod. (The separate Reverse Almanac
   Order mod *does* now rebuild its world-map patch from real per-plant
   `OBTAINWORLD` data, but that's a different, more limited kind of
   information than full level/wave data.)

### Old confidence notes (zombies/levels only — plants section below is now obsolete, kept for the zombie/level methodology it still describes)

This pack targets Gardendless's documented **GP-Next** mod system. Two
notes on the zombie/level portion specifically:

- No public schema for zombie stats or level/wave data was reachable
  while building the zombie/level portion (the docs site, `pvzge.com`, is
  blocked from this environment), so `Toughness`/`Damage`/`Speed` for
  zombies and the `Worlds → Levels → Waves → Zombies{codename: count}`
  level shape are guesses mirrored from the confirmed plant schema. They
  may not match your install's real field names.
- The zombie/level numbers are not extracted from your game. Zombie
  *names* are best-effort recollections of real PvZ2 content, generated
  from a documented tier + archetype formula (basic/armored/tank/fast),
  scaled by an assumed world order that itself doesn't match the real
  `OBTAINWORLD` codenames found in the real plant data (e.g. the real
  world order/names are `frontyard, egypt, pirate, cowboy, dark, future,
  ice, lod, water, modern, kongfu, beach, lostcity, eighties, dino, sky,
  epic, market` — quite different from the 12-world guess the zombie/level
  pass still uses). Treat the zombie/level portion as a large, internally
  consistent stress-test of the rebalance math, not a verified guide to
  Gardendless's actual roster.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/auto-rebalance/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level so the new sun costs, zombie toughness, and wave
   pacing take effect.

## What's covered

**Plants (real, 163):** every plant in the user's uploaded data except
the 14-plant Mints family (fed to other plants, not planted directly —
`SunCost: 0` for all of them, which would break the cost-normalization
math) and 36 entries with no independent existence (marigold color
variants, zombie-potion items, tool-projectile sub-objects, growth-stage
forms, or missing `PlantProps` data).

**Zombies & levels (estimated, unchanged from the previous version):** 12
guessed worlds, 4 zombies each, 2 levels each, plus 4 guessed premium
plants — see the old confidence notes above for exactly what that
methodology is and isn't.

## Folder contents

```
pack.json                          - GP-Next mod manifest (name/version/author)
jsons/objects/PlantProps.json      - rebalanced plant SunCost (real 163-plant roster)
jsons/objects/plants-changes.md    - before/after table for plants
jsons/objects/ZombieProps.json     - rebalanced zombie Toughness (estimated roster)
jsons/objects/zombies-changes.md   - before/after table for zombies
jsons/worldmap/WorldMap.json       - rebalanced level wave zombie counts (estimated)
jsons/worldmap/levels-changes.md   - before/after table for levels
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
- [gp-next-datapack.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-datapack.md) — real `pack.json` template
- **User-uploaded `PlantFeatures.json` and `PlantProps.json`** — real source of truth for the plant rebalance
