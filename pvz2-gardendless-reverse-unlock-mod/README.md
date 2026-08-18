# Reverse Almanac Order — a PvZ2 Gardendless mod

Reverses plant order in [PvZ2 Gardendless](https://pvzge.com/en/) (an
open-source, fan-made PC rewrite of Plants vs Zombies 2), now built
directly from **your real extracted `PlantFeatures.json` and
`PlantProps.json`** instead of guessed data: the seed-chooser order, the
Shop's illustrative costs, and **where in the game each plant is
unlocked** — globally across every real world.

Three independent, already-finished patches — nothing to build or run:

- **`jsons/features/PlantFeatures.json`** — `SEEDCHOOSERDEFAULTORDER` set
  to your real 180-entry order (166 after excluding the 14 "mint" plants,
  per your instruction), reversed.
- **`jsons/objects/StoreCommodityFeatures.json`** — reverses illustrative
  costs across the real 33-plant "market" (Shop) roster.
- **`jsons/worldmap/gpn-worldmap.json`** — rebuilds the world map's
  progression (`mainline`) for 15 real worlds + Epic Quest (excludes
  `frontyard` — see v8→v9 below), reversing which `plant`-type node
  grants which plant, globally across all 133 reward slots.

See `jsons/features/almanac-order-changes.md`,
`jsons/objects/shop-order-changes.md`, and
`jsons/worldmap/worldmap-changes.md` for exactly what changed in each file.

## v8 → v9: two confirmed bugs fixed from real testing

You reported two specific things after the v8 fix got the pack loading:

1. **Frontyard plants didn't change.** This lines up with `BASEUNLOCKLIST`
   — confirmed real, exactly
   `["peashooter","sunflower","wallnut","potatomine"]` — pre-granting
   those plants the moment a save is created, independent of any
   `mainline` node. The frontyard/tutorial levels still exist for onboarding,
   but there's nothing for a reversed `plantReward` to change: you already
   own the plant before reaching the node. **`frontyard` is now excluded
   from the world map reversal entirely** (down from 138 to 133 reward
   slots) rather than shipping a patch that provably does nothing.
2. **The "New Plant!" reveal screen didn't show the reversed plant.**
   Re-checked the docs and found: `plant`/`upgrade`/`giftBox`/`epicPortal`
   nodes all require an explicit `"template"` object (e.g.
   `"template": {"type": "plant"}`) — every plant node in this mod was
   missing it. That's now added to every plant-reward node. This is the
   most likely explanation, but it's still worth confirming after
   reinstalling — if the reveal screen still shows the wrong plant, that
   points to a *different* field driving that specific screen, and I'd
   need another round to track it down.

## v7 → v8: fixed "nothing changes at all" even with the experimental flag on

Reported: after enabling `worldMapJson` in Experimental settings and
installing, none of this mod's changes took effect — not just the world
map, but seed-chooser order and Shop costs too. That points at the whole
pack failing to load, not a world-map-specific problem. The likely cause:
`pack.json` had `"gpNextVersion": ">=1.0.0"` and
`"requiredGpNextFeatures": ["experimental.worldMapJson"]` — both copied
from the docs' generic example, neither individually verified against a
real install. If GP-Next treats either as a hard gate (version mismatch,
unrecognized feature string) it can reject the entire pack silently,
which matches "nothing changes" with no error shown. **Both are removed
in this version.**

### If it's still not working after this fix

That would mean the pack loads but a Shop/Almanac-check is still worth
doing to narrow it down further:
1. Confirm the pack shows up as *enabled* in the in-game Patcher/GP-Next
   mod list (not just present in the folder).
2. Check if `SEEDCHOOSERDEFAULTORDER` took effect (seed-chooser screen
   plant order changed) — if yes but the world map didn't, the problem is
   specific to `gpn-worldmap.json`'s content (most likely: this mod's
   world codenames/level IDs beyond the one confirmed `egypt` example
   don't match your install's real IDs, so those `worlds` entries get
   silently skipped).
3. If even `SEEDCHOOSERDEFAULTORDER` didn't take effect, the pack likely
   still isn't loading at all — check the exact install path
   (`gp-next/packs/<name>/pack.json` at the top level of that folder, not
   nested deeper) and whether GP-Next logs an error anywhere (a log file,
   console output, or in-game notification) that could be shared.

## 🛑 Back up your save before installing this

Gardendless's own docs say **"Users should back up saves before
testing"** the world-map feature specifically. `gpn-worldmap.json` also
requires enabling **`worldMapJson` in the in-game Experimental
settings** (a manual toggle you set yourself — `pack.json` no longer
declares this as a required feature, since that field was implicated in
an earlier "nothing loads" bug; see v7→v8 below).

## v6 → v7: rebuilt from your real uploaded data

You uploaded your own extracted `PlantFeatures.json` (213 real `PLANTS`
entries, the real `SEEDCHOOSERDEFAULTORDER`/`BASEUNLOCKLIST` arrays) and
`PlantProps.json` (real `SunCost`/`Toughness`/`Cooldown`/`Family` per
plant). This replaces almost everything that was previously
estimated/guessed:

- **World attribution was wrong for a lot of plants.** Real
  `OBTAINWORLD` corrected e.g. CherryBomb (`pirate`, not `egypt`),
  SnapDragon (`pirate`, not `dino`), Grimrose (`modern`, not `dark`),
  TallNut/SplitPea/WinterMelon (`cowboy`/Wild West, not where I'd guessed),
  HotPotato/ChardGuard (`ice`/Frostbite Caves), SnowPea (`kongfu`/Kung Fu
  World — a whole real world I'd missed entirely, along with `lod`/Lawn of
  Doom and `sky`/Sky City, `water`).
- **`BASEUNLOCKLIST` is confirmed, in your real data, to be exactly**
  `["peashooter","sunflower","wallnut","potatomine"]` — 4 starting plants,
  not a progression order. This confirms the earlier decision not to
  touch it.
- **`SEEDCHOOSERDEFAULTORDER` has exactly 180 real entries** (matches the
  Almanac's own published plant count). Now reversed directly, mint
  entries removed, instead of a synthesized approximation.
- **The world map now uses your real world codenames and real plant
  rosters per world** (`epic` has 41 real plants, `market`/Shop has 33,
  etc.) instead of an invented 12-world/61-plant roster.
- **`objclass` for `PlantProps.json` patches is confirmed `PlantProperties`**
  (not `Plant`, which was a guess in earlier versions and in the
  Auto Rebalance mod — both are now fixed).
- **"Mint" is confirmed to mean the 14-plant Mints family**
  (`reinforcemint`, `enlightenmint`, `wintermint`, `spearmint`,
  `appeasemint`, `enforcemint`, `peppermint`, `bombardmint`,
  `concealmint`, `ailmint`, `enchantmint`, `filamint`, `containmint`,
  `armamint`) — all excluded, all with `SunCost: 0` (they're fed to other
  plants, not planted directly, which is also why they're excluded from
  the Auto Rebalance mod's cost math).
- **27 blank-`OBTAINWORLD` entries were excluded** — these are sub-effects
  and variants, not independently unlockable plants: marigold color
  variants, zombie-potion items, bowling-bulb tool projectiles, and
  growth-stage entries like the base `atombomb`/`seedling` forms of
  Doom-shroom's seedlings.

## ⚠️ What's still not from real data

1. **Specific level IDs inside each world are still inferred**, not
   individually verified. The docs' own worked example confirms the
   `<worldcode><n>` pattern (e.g. `egypt1`, `egypt2`) for Ancient Egypt
   specifically; this mod applies that same pattern to the other 16 real
   world codenames, which is a reasonable extrapolation but not
   individually confirmed per level.
2. **Shop costs (`CurrencyRequired`) are still illustrative placeholders.**
   `PlantProps.json` only has in-level `SunCost`, not the Shop's real
   gem/coin price — I don't have that data. The roster (33 real "market"
   plants) is real; the specific numbers being swapped are not.
3. **Zombies and levels weren't part of what you uploaded**, so this mod
   doesn't touch zombie stats or per-level zombie waves at all — see the
   separate Auto Rebalance mod for that (still best-effort/estimated
   there).

## Installing the mod in-game

1. Back up your save (see above).
2. Copy this whole folder into your `gp-next/packs/` directory, e.g.
   `gp-next/packs/reverse-almanac-order/`.
3. Enable it from the in-game Patcher/GP-Next mod list.
4. Enable `worldMapJson` in the in-game **Experimental** settings page.
5. Restart the world map / seed chooser / shop screens so the reversed
   order, costs, and unlock locations take effect.

## Folder contents

```
pack.json                                 - GP-Next mod manifest
jsons/features/PlantFeatures.json         - reversed SEEDCHOOSERDEFAULTORDER (166 real plants)
jsons/features/almanac-order-changes.md   - full before/after table
jsons/objects/StoreCommodityFeatures.json - reversed Shop costs (real 33-plant roster)
jsons/objects/shop-order-changes.md       - before/after table
jsons/worldmap/gpn-worldmap.json          - reversed world-map plant rewards (15 real worlds + Epic Quest, 133 slots)
jsons/worldmap/worldmap-changes.md        - before/after table, per node
```

## Sources

- [PvZ2 Gardendless official site](https://pvzge.com/en/) (docs pages
  blocked from this environment; reached via GitHub mirrors instead)
- [pvzge_web — game source (GitHub)](https://github.com/Gzh0821/pvzge_web)
- [pvzg_site — docs source (GitHub)](https://github.com/Gzh0821/pvzg_site)
- [gp-next-worldmap.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-worldmap.md) — the confirmed `egypt`/`egypt1` example and save-backup warning
- [gpn-worldmap.schema.json (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/.vuepress/public/jsons/schema/gpn-worldmap.schema.json) — node types, `mainline`/`branches`/"replace"-mode structure
- [gp-next-datapack.md (raw, GitHub)](https://raw.githubusercontent.com/Gzh0821/pvzg_site/refs/heads/main/src/en/guide/mod/gp-next-datapack.md) — real `pack.json` template
- **Your uploaded `PlantFeatures.json` and `PlantProps.json`** — the real, extracted source of truth for everything plant-related in this mod as of this version
