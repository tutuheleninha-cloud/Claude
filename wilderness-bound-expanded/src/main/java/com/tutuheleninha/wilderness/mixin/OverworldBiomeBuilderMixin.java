package com.tutuheleninha.wilderness.mixin;

import java.util.function.Consumer;

import com.mojang.datafixers.util.Pair;
import com.tutuheleninha.wilderness.worldgen.ModBiomes;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.biome.Climate;
import net.minecraft.world.level.biome.OverworldBiomeBuilder;

/**
 * Places the new biomes in the overworld climate map, next to their vanilla relatives:
 * <ul>
 * <li>Old Growth Dappled Forest takes the most "weird" part of the Dappled Forest's climate, like other old growth variants.</li>
 * <li>Bog takes the cold half of the swamp climate (swamps stay in temperate areas).</li>
 * </ul>
 */
@Mixin(OverworldBiomeBuilder.class)
public abstract class OverworldBiomeBuilderMixin {
	@Shadow
	@Final
	private Climate.Parameter[] temperatures;

	@Shadow
	private void addSurfaceBiome(Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> consumer, Climate.Parameter temperature,
			Climate.Parameter humidity, Climate.Parameter continentalness, Climate.Parameter erosion, Climate.Parameter weirdness,
			float offset, ResourceKey<Biome> biome) {
		throw new AssertionError();
	}

	@Inject(method = "pickMiddleBiome", at = @At("RETURN"), cancellable = true)
	private void wilderness$oldGrowthDappledForest(int temperature, int humidity, Climate.Parameter weirdness,
			CallbackInfoReturnable<ResourceKey<Biome>> cir) {
		if (cir.getReturnValue() == Biomes.DAPPLED_FOREST && weirdness.min() >= ModBiomes.OLD_GROWTH_MIN_WEIRDNESS) {
			cir.setReturnValue(ModBiomes.OLD_GROWTH_DAPPLED_FOREST);
		}
	}

	@Inject(method = "addSurfaceBiome", at = @At("HEAD"), cancellable = true)
	private void wilderness$coldSwampsBecomeBogs(Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> consumer,
			Climate.Parameter temperature, Climate.Parameter humidity, Climate.Parameter continentalness, Climate.Parameter erosion,
			Climate.Parameter weirdness, float offset, ResourceKey<Biome> biome, CallbackInfo ci) {
		if (biome != Biomes.SWAMP) {
			return;
		}

		Climate.Parameter cold = this.temperatures[1];

		if (temperature.min() > cold.min() || temperature.max() < cold.max()) {
			return;
		}

		this.addSurfaceBiome(consumer, cold, humidity, continentalness, erosion, weirdness, offset, ModBiomes.BOG);

		if (temperature.max() > cold.max()) {
			Climate.Parameter warmer = Climate.Parameter.span(this.temperatures[2], temperature);
			this.addSurfaceBiome(consumer, warmer, humidity, continentalness, erosion, weirdness, offset, Biomes.SWAMP);
		}

		ci.cancel();
	}
}
