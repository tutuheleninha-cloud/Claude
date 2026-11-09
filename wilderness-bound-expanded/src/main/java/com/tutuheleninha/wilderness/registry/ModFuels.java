package com.tutuheleninha.wilderness.registry;

import com.tutuheleninha.wilderness.WildernessMod;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProvider;

/**
 * Burn times are data-driven since 26.3; the values live in {@code data/wilderness/context_int_provider/cooking}.
 */
public final class ModFuels {
	public static final ResourceKey<ContextIntProvider> PEAT =
			ResourceKey.create(Registries.CONTEXT_INT_PROVIDER, WildernessMod.id("cooking/time_peat"));

	private ModFuels() {
	}
}
