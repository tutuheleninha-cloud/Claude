#!/usr/bin/env node
/**
 * Regenerates this mod's jsons/ patch files from real, user-supplied
 * PvZ2 Gardendless data, by reversing plant unlock order.
 *
 * Usage:
 *   node scripts/reverse-unlocks.js \
 *     --plants=source/PlantFeatures.json \
 *     --worldmap=source/WorldMap.json \
 *     --out=jsons
 *
 * All arguments are optional; each defaults to the bundled *.example.json
 * placeholder so the script runs out of the box (producing a placeholder
 * patch, not a real one). See README.md for how to get the real source
 * files from your own game install.
 */
"use strict";
const fs = require("fs");
const path = require("path");

function arg(name, fallback) {
  const prefix = `--${name}=`;
  const hit = process.argv.find((a) => a.startsWith(prefix));
  return hit ? hit.slice(prefix.length) : fallback;
}

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function writeJson(p, data) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + "\n");
}

const root = path.resolve(__dirname, "..");
const plantsPath = path.resolve(root, arg("plants", "source/PlantFeatures.example.json"));
const worldmapPath = path.resolve(root, arg("worldmap", "source/WorldMap.example.json"));
const outDir = path.resolve(root, arg("out", "jsons"));

// --- 1. Reverse the base/default unlock order -----------------------------
// Confirmed by the mod docs: BASEUNLOCKLIST and SEEDCHOOSERDEFAULTORDER are
// plain string arrays that get overwritten wholesale on merge, so we only
// need to emit those two keys, reversed.
function reverseFeatures() {
  const src = readJson(plantsPath);
  const patch = {};
  if (Array.isArray(src.BASEUNLOCKLIST)) {
    patch.BASEUNLOCKLIST = [...src.BASEUNLOCKLIST].reverse();
  }
  if (Array.isArray(src.SEEDCHOOSERDEFAULTORDER)) {
    patch.SEEDCHOOSERDEFAULTORDER = [...src.SEEDCHOOSERDEFAULTORDER].reverse();
  }
  const outPath = path.join(outDir, "features", "PlantFeatures.json");
  writeJson(outPath, patch);
  console.log(`[features] wrote ${path.relative(root, outPath)}`);
  return patch;
}

// --- 2. Reverse which plant each level unlocks -----------------------------
// The exact field/key names for per-level plant rewards aren't publicly
// documented, so this walks the tree heuristically: any object with one of
// REWARD_KEYS holding a string value is treated as "this level/node unlocks
// plant X". Entries are collected in document order, the plant codenames are
// reversed, and reassigned to the same slots (so unlock ORDER reverses, but
// which level-slots exist does not change).
const REWARD_KEYS = [
  "RewardPlant", "REWARDPLANT", "UnlockPlant", "UNLOCKPLANT",
  "PlantReward", "PLANTREWARD", "NewPlant", "NEWPLANT",
];
const ID_KEYS = ["ID", "Id", "LevelName", "LEVELNAME", "Name", "CODENAME"];

function findId(ancestors) {
  for (let i = ancestors.length - 1; i >= 0; i--) {
    const node = ancestors[i];
    if (node && typeof node === "object") {
      for (const k of ID_KEYS) if (typeof node[k] === "string") return node[k];
    }
  }
  return null;
}

function collectRewards(node, ancestors, hits) {
  if (Array.isArray(node)) {
    node.forEach((child) => collectRewards(child, ancestors, hits));
    return;
  }
  if (node && typeof node === "object") {
    for (const key of REWARD_KEYS) {
      if (typeof node[key] === "string") {
        hits.push({ levelId: findId([...ancestors, node]), key, value: node[key], node });
      }
    }
    for (const value of Object.values(node)) {
      collectRewards(value, [...ancestors, node], hits);
    }
  }
}

function reverseWorldmap() {
  if (!fs.existsSync(worldmapPath)) {
    console.log("[worldmap] no worldmap source found, skipping");
    return;
  }
  const src = readJson(worldmapPath);
  const hits = [];
  collectRewards(src, [], hits);

  if (hits.length === 0) {
    console.log("[worldmap] no plant-unlock reward fields recognized — see README's");
    console.log("           'If the script finds nothing' section to add your field names.");
    return;
  }

  const originalValues = hits.map((h) => h.value);
  const reversedValues = [...originalValues].reverse();

  // Build a minimal patch: one entry per level id + the reward key/value,
  // which matches the documented CODENAME-based merge behavior for objects.
  const patchEntries = hits.map((h, i) => ({
    ID: h.levelId,
    [h.key]: reversedValues[i],
  }));

  const outPath = path.join(outDir, "worldmap", "WorldMap.json");
  writeJson(outPath, { Levels: patchEntries });
  console.log(`[worldmap] wrote ${path.relative(root, outPath)} (${hits.length} unlock(s) reversed)`);

  // Human-readable before/after table for manual verification in-game.
  const reportLines = [
    "# Unlock order changes",
    "",
    "| Level | Was unlocking | Now unlocks |",
    "|---|---|---|",
    ...hits.map((h, i) => `| ${h.levelId ?? "?"} | ${originalValues[i]} | ${reversedValues[i]} |`),
    "",
  ];
  const reportPath = path.join(outDir, "worldmap", "unlock-order-changes.md");
  fs.writeFileSync(reportPath, reportLines.join("\n"));
  console.log(`[worldmap] wrote ${path.relative(root, reportPath)}`);
}

reverseFeatures();
reverseWorldmap();
