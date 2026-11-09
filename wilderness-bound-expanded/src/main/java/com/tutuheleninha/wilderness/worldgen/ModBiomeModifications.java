package com.tutuheleninha.wilderness.worldgen;

import com.tutuheleninha.wilderness.WildernessMod;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;

import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;

/**
 * Spreads some of the new plants and fallen hollow logs into vanilla biomes.
 *
 * <p>Additions are registered in alphabetical order of feature id, and the new biomes list these features in the same
 * order, so the feature order stays consistent across biomes (otherwise the game refuses to start).
 */
public final class ModBiomeModifications {
	private ModBiomeModifications() {
	}

	public static void init() {
		add("fallen_hollow_birch_tree", BiomeSelectors.includeByKey(Biomes.BIRCH_FOREST, Biomes.OLD_GROWTH_BIRCH_FOREST));
		add("fallen_hollow_oak_tree", BiomeSelectors.includeByKey(Biomes.FOREST));
		add("fallen_hollow_poplar_tree", BiomeSelectors.includeByKey(Biomes.DAPPLED_FOREST));
		add("fallen_hollow_spruce_tree", BiomeSelectors.includeByKey(Biomes.TAIGA, Biomes.OLD_GROWTH_PINE_TAIGA, Biomes.OLD_GROWTH_SPRUCE_TAIGA));
		add("patch_aster", BiomeSelectors.includeByKey(Biomes.DAPPLED_FOREST, Biomes.MEADOW, Biomes.FLOWER_FOREST));
		add("patch_cattail", BiomeSelectors.includeByKey(Biomes.SWAMP, Biomes.RIVER));
		add("patch_goldenrod", BiomeSelectors.includeByKey(Biomes.DAPPLED_FOREST, Biomes.MEADOW, Biomes.PLAINS));
	}

	private static void add(String name, java.util.function.Predicate<net.fabricmc.fabric.api.biome.v1.BiomeSelectionContext> selector) {
		ResourceKey<PlacedFeature> key = ResourceKey.create(Registries.PLACED_FEATURE, WildernessMod.id(name));
		BiomeModifications.addFeature(selector, GenerationStep.Decoration.VEGETAL_DECORATION, key);
	}
}
