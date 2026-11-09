package com.tutuheleninha.wilderness.registry;

import com.tutuheleninha.wilderness.WildernessMod;

import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BannerPattern;

public final class ModTags {
	/** Blocks (besides lit campfires) that heat a cooking pot placed above them. */
	public static final TagKey<Block> COOKING_POT_HEAT_SOURCES = TagKey.create(Registries.BLOCK, WildernessMod.id("cooking_pot_heat_sources"));
	public static final TagKey<Block> HOLLOW_LOGS = TagKey.create(Registries.BLOCK, WildernessMod.id("hollow_logs"));
	public static final TagKey<Block> LOG_BENCHES = TagKey.create(Registries.BLOCK, WildernessMod.id("log_benches"));

	public static final TagKey<Item> DEER_FOOD = TagKey.create(Registries.ITEM, WildernessMod.id("deer_food"));
	public static final TagKey<Item> OWL_FOOD = TagKey.create(Registries.ITEM, WildernessMod.id("owl_food"));
	public static final TagKey<Item> BROWN_BEAR_FOOD = TagKey.create(Registries.ITEM, WildernessMod.id("brown_bear_food"));
	public static final TagKey<Item> SQUIRREL_FOOD = TagKey.create(Registries.ITEM, WildernessMod.id("squirrel_food"));

	public static final TagKey<BannerPattern> PATTERN_ITEM_ANTLERS = TagKey.create(Registries.BANNER_PATTERN, WildernessMod.id("pattern_item/antlers"));

	private ModTags() {
	}
}
