# Reverse Unlock Order — a PvZ2 Gardendless mod

Reverses the order plants are unlocked in [PvZ2 Gardendless](https://pvzge.com/en/)
(an open-source, fan-made PC rewrite of Plants vs Zombies 2). The plant you'd
normally get last is now the first one you unlock, and vice versa — across
both the base unlock list and the individual level rewards.

## ⚠️ Please read before installing

This pack targets Gardendless's documented **GP-Next** mod system
(`packs/<name>/pack.json` + `jsons/...`, merging by matching id/`CODENAME`
fields). I put it together from public search results and GP-Next's own
docs summaries, because the docs site (`pvzge.com`) was unreachable from
this environment when I built this, so I could not read the exact schema
pages myself. Two things follow from that:

1. **The `BASEUNLOCKLIST` / `SEEDCHOOSERDEFAULTORDER` reversal is on solid
   ground** — those two array fields and their "plain overwrite on merge"
   behavior were confirmed directly.
2. **The per-level `jsons/worldmap/WorldMap.json` patch is a best-effort
   guess at field names** (`RewardPlant`, level `ID`, etc.) since Gardendless
   doesn't publish its exact level-data schema. It may not load as-is.

Either way, the shipped `jsons/` files right now are generated from
**placeholder example data** (`source/*.example.json`), not your real game
data — see below to make this pack actually correct for your install.

## Making it correct for your install

1. Launch Gardendless, open the in-game Patcher/GP-Next UI, and use its
   "Open Folder" button to find your `gp-next/` data directory.
2. Locate your real plant-features JSON (has `BASEUNLOCKLIST` /
   `SEEDCHOOSERDEFAULTORDER`) and your real world/level-map JSON, and copy
   them into `source/` in this pack (e.g. `source/PlantFeatures.json`,
   `source/WorldMap.json`).
3. Regenerate the patch files:
   ```sh
   node scripts/reverse-unlocks.js \
     --plants=source/PlantFeatures.json \
     --worldmap=source/WorldMap.json
   ```
4. Check `jsons/worldmap/unlock-order-changes.md` — a plain before/after
   table of every unlock the script found and swapped, so you can sanity
   check it before playing.

### If the script finds nothing in your worldmap file

Your data may use different field names than the ones this script looks
for (`RewardPlant`, `UnlockPlant`, `PlantReward`, `NewPlant`, in a few
casings). Open `scripts/reverse-unlocks.js`, add your real field name to
the `REWARD_KEYS` array near the top of the "Reverse which plant each
level unlocks" section, and rerun the script.

## Installing the mod in-game

1. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/reverse-unlock-order/`.
2. Enable it from the in-game Patcher/GP-Next mod list.
3. Restart the level select / world map screen so the reversed unlock
   order takes effect.

## Folder contents

```
pack.json                          - GP-Next mod manifest (name/version/author)
jsons/features/PlantFeatures.json  - reversed BASEUNLOCKLIST + SEEDCHOOSERDEFAULTORDER
jsons/worldmap/WorldMap.json       - reversed per-level plant unlock rewards
jsons/worldmap/unlock-order-changes.md - human-readable before/after table
scripts/reverse-unlocks.js         - regenerates the two files above from real data
source/*.example.json              - placeholder data the shipped patch was built from
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [GE Patcher / GP-Next mod format overview](https://pvzge.com/en/guide/mod/)
