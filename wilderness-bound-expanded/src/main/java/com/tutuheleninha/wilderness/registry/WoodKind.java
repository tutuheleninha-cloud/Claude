package com.tutuheleninha.wilderness.registry;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

/**
 * Every wood type that gets hollow logs, log benches and parquet. Order matches the vanilla creative tab.
 */
public enum WoodKind {
	OAK("oak", "oak_log", Blocks.OAK_LOG, Blocks.STRIPPED_OAK_LOG, Blocks.OAK_PLANKS, Blocks.OAK_SLAB, Blocks.STRIPPED_OAK_WOOD),
	SPRUCE("spruce", "spruce_log", Blocks.SPRUCE_LOG, Blocks.STRIPPED_SPRUCE_LOG, Blocks.SPRUCE_PLANKS, Blocks.SPRUCE_SLAB, Blocks.STRIPPED_SPRUCE_WOOD),
	BIRCH("birch", "birch_log", Blocks.BIRCH_LOG, Blocks.STRIPPED_BIRCH_LOG, Blocks.BIRCH_PLANKS, Blocks.BIRCH_SLAB, Blocks.STRIPPED_BIRCH_WOOD),
	JUNGLE("jungle", "jungle_log", Blocks.JUNGLE_LOG, Blocks.STRIPPED_JUNGLE_LOG, Blocks.JUNGLE_PLANKS, Blocks.JUNGLE_SLAB, Blocks.STRIPPED_JUNGLE_WOOD),
	ACACIA("acacia", "acacia_log", Blocks.ACACIA_LOG, Blocks.STRIPPED_ACACIA_LOG, Blocks.ACACIA_PLANKS, Blocks.ACACIA_SLAB, Blocks.STRIPPED_ACACIA_WOOD),
	DARK_OAK("dark_oak", "dark_oak_log", Blocks.DARK_OAK_LOG, Blocks.STRIPPED_DARK_OAK_LOG, Blocks.DARK_OAK_PLANKS, Blocks.DARK_OAK_SLAB, Blocks.STRIPPED_DARK_OAK_WOOD),
	MANGROVE("mangrove", "mangrove_log", Blocks.MANGROVE_LOG, Blocks.STRIPPED_MANGROVE_LOG, Blocks.MANGROVE_PLANKS, Blocks.MANGROVE_SLAB, Blocks.STRIPPED_MANGROVE_WOOD),
	CHERRY("cherry", "cherry_log", Blocks.CHERRY_LOG, Blocks.STRIPPED_CHERRY_LOG, Blocks.CHERRY_PLANKS, Blocks.CHERRY_SLAB, Blocks.STRIPPED_CHERRY_WOOD),
	PALE_OAK("pale_oak", "pale_oak_log", Blocks.PALE_OAK_LOG, Blocks.STRIPPED_PALE_OAK_LOG, Blocks.PALE_OAK_PLANKS, Blocks.PALE_OAK_SLAB, Blocks.STRIPPED_PALE_OAK_WOOD),
	POPLAR("poplar", "poplar_log", Blocks.POPLAR_LOG, Blocks.STRIPPED_POPLAR_LOG, Blocks.POPLAR_PLANKS, Blocks.POPLAR_SLAB, Blocks.STRIPPED_POPLAR_WOOD),
	CRIMSON("crimson", "crimson_stem", Blocks.CRIMSON_STEM, Blocks.STRIPPED_CRIMSON_STEM, Blocks.CRIMSON_PLANKS, Blocks.CRIMSON_SLAB, Blocks.STRIPPED_CRIMSON_HYPHAE),
	WARPED("warped", "warped_stem", Blocks.WARPED_STEM, Blocks.STRIPPED_WARPED_STEM, Blocks.WARPED_PLANKS, Blocks.WARPED_SLAB, Blocks.STRIPPED_WARPED_HYPHAE);

	private final String name;
	private final String logName;
	private final Block log;
	private final Block strippedLog;
	private final Block planks;
	private final Block slab;
	private final Block strippedWood;

	WoodKind(String name, String logName, Block log, Block strippedLog, Block planks, Block slab, Block strippedWood) {
		this.name = name;
		this.logName = logName;
		this.log = log;
		this.strippedLog = strippedLog;
		this.planks = planks;
		this.slab = slab;
		this.strippedWood = strippedWood;
	}

	public String woodName() {
		return this.name;
	}

	/** "oak_log", or "crimson_stem" for nether woods. */
	public String logName() {
		return this.logName;
	}

	public boolean isNether() {
		return this == CRIMSON || this == WARPED;
	}

	public Block log() {
		return this.log;
	}

	public Block strippedLog() {
		return this.strippedLog;
	}

	public Block planks() {
		return this.planks;
	}

	public Block slab() {
		return this.slab;
	}

	/** The last vanilla log-family block in the creative tab, used to place our blocks after it. */
	public Block strippedWood() {
		return this.strippedWood;
	}
}
