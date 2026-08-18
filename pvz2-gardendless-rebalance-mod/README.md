# Auto Rebalance — a PvZ2 Gardendless mod

Rebalances plants, zombies, and levels in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2), across all 12
mainline PvZ2 worlds plus a cross-world premium/gem plant group: 54 plants,
48 zombies, 24 levels. Three independent, already-finished patches —
nothing to build or run:

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
3. **The base numbers are not extracted from your game, and their
   reliability drops the further into the roster you go.** None of this
   was pulled from Gardendless's actual current data files — I don't have
   access to those. Two different levels of confidence went into the
   starting values this mod's math ran against:
   - **Ancient Egypt & Pirate Seas (10 plants, 8 zombies, 4 levels):**
     well-known, public classic-PvZ2 numbers I'm reasonably confident in.
   - **The other 10 worlds + premium group (44 plants, 40 zombies, 20
     levels):** I don't have reliable per-item stat recall for that much of
     the real PvZ2 roster, so rather than guess specific "facts" I'd likely
     get wrong, these were generated from a documented tier + archetype
     formula (attacker/sun-producer/wall/bomb/utility for plants; basic/
     armored/tank/fast for zombies), scaled by world order. Plant and
     zombie *names* are best-effort recollections of real PvZ2 content and
     may not all be correctly attributed to the world listed, may not use
     Gardendless's real internal `CODENAME`s, and Gardendless itself may
     not include all of them (modding can't add content it doesn't already
     have) — Sky City and the four premium/gem plants in particular are my
     lowest-confidence entries in this mod, both on naming and on whether
     Gardendless includes them at all. Treat worlds 3–12 and the premium
     group below as a large, internally consistent stress-test of the
     rebalance math, not a verified guide to either real PvZ2 or
     Gardendless's actual roster.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/auto-rebalance/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level so the new sun costs, zombie toughness, and wave
   pacing take effect.

## What's covered

12 worlds, 2 levels each (`<world#>_1`, `<world#>_2`), plus 4 cross-world
premium/gem plants (no levels — premium plants aren't tied to a world in
real PvZ2 either). Worlds 1–2 use known real values; everything else uses
the estimated tier/archetype formula (see caveat #3 above).

| # | World | Plants | Zombies |
|---|---|---|---|
| 1 | Ancient Egypt | PeaShooter, SunFlower, WallNut, CherryBomb, PotatoMine | ZombieBasic, ZombieConehead, ZombieBuckethead, ZombieFlag |
| 2 | Pirate Seas | SnowPea, Chomper, Repeater, Threepeater, Bloomerang | ZombieSnorkel, ZombiePole, ZombieBarrelRoller, ZombieSwashbuckler |
| 3 | Wild West | HotPotato, ChiliBean, GraveBuster, BowlingBulb | ZombieProspector, ZombiePianist, ZombieChickenWrangler, ZombieRodeoLegend |
| 4 | Dark Ages | BonkChoy, SpikeweedTrap, Grimrose, WitchHazel | ZombieKnight, ZombieWizard, ZombieFootSoldier, ZombieImp |
| 5 | Far Future | LaserBean, InfiNut, TallNut, SplitPea | ZombieJetpack, ZombieZ7Mech, ZombieBot, ZombieGargantuarFuture |
| 6 | Frostbite Caves | Hurrikale, Toadstool, Bombegranate, IcebergLettuce | ZombieWeaselHoarder, ZombieFrostyRider, ZombieYetiImp, ZombieIceTrooper |
| 7 | Lost City | PerfumeShroom, GoldLeaf, RootsPlant, PowerLily | ZombieExcavator, ZombieTombRaiser, ZombieRelicHunter, ZombieStoneGuard |
| 8 | Neon Mixtape Tour | HyperShroom, BeetBoxer, DiscoPea, RockpultPlant | ZombieBreakdancer, ZombieGlitter, ZombieDiscoBoss, ZombieRollerSkater |
| 9 | Jurassic Marsh | Snapdragon, PrimalPeaShooter, PrimalWallNut, PrimalSunflower | ZombiePrimalGargantuar, ZombieRaptorRider, ZombiePterodactyl, ZombieCaveman |
| 10 | Big Wave Beach | LavaGuava, ShellBean, SeaKelp, CoconutCannon | ZombieFisherman, ZombieSurfer, ZombieLifeguard, ZombieOctopusRider |
| 11 | Modern Day | Gloomshroom, Wintermelon, GatlingPea, Cactus | ZombieNewspaper, ZombieDancing, ZombieBackupDancer, ZombieScreenDoor |
| 12 | Sky City | MagnifyingGrass, AloeVera, Blover, Escapea | ZombieDrone, ZombieHoverboard, ZombieCloudRider, ZombieStormTrooper |
| — | Premium (cross-world) | ShrinkingViolet, PeaNut, TitanFrost, GrapeShot | _(none — zombies aren't a purchased/premium concept in PvZ2)_ |

Still not covered, on purpose: event- or arena-only content (Piñata Party,
Battlez, Epic Quest exclusives), and boss zombies (Zomboss forms) — these
are one-off/unique fights rather than roster entries a cost/toughness
normalization pass makes sense against.

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

## Note on `pack.json`

Updated to match the real manifest schema found in the docs
(`gp-next-datapack.md`): added `uuid`, `packFormatVersion`, `gameVersion`,
and `gpNextVersion` (the earlier `id` field isn't part of the real
schema). See the reverse-almanac-order mod's README for the verbatim
template this was corrected against.

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [Types & Fields — mod format docs (GitHub)](https://github.com/Gzh0821/pvzg_site/blob/main/src/en/guide/mod/format.md)
- [gp-next-datapack.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-datapack.md) — source of the real `pack.json` template
