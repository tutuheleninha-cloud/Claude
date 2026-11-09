package com.tutuheleninha.wilderness.worldgen;

import com.tutuheleninha.wilderness.WildernessMod;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;

/**
 * The biomes themselves are data (data/wilderness/worldgen/biome). Placement in the overworld is done the same way
 * vanilla places its variants, see {@code OverworldBiomeBuilderMixin}.
 */
public final class ModBiomes {
	public static final ResourceKey<Biome> OLD_GROWTH_DAPPLED_FOREST = key("old_growth_dappled_forest");
	public static final ResourceKey<Biome> BOG = key("bog");

	/**
	 * Dappled Forests only appear where weirdness is positive. The two outermost weirdness slices become the old growth
	 * variant, so roughly a quarter of all dappled forests are old growth.
	 */
	public static final long OLD_GROWTH_MIN_WEIRDNESS = Climate.quantizeCoord(0.76F);

	private ModBiomes() {
	}

	private static ResourceKey<Biome> key(String name) {
		return ResourceKey.create(Registries.BIOME, WildernessMod.id(name));
	}
}
