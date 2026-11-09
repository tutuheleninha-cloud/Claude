package com.tutuheleninha.wilderness.registry;

import com.tutuheleninha.wilderness.WildernessMod;
import com.tutuheleninha.wilderness.entity.Seat;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;

public final class ModEntities {
	public static final EntityType<Seat> SEAT = register("seat", EntityType.Builder.<Seat>of(Seat::new, MobCategory.MISC)
			.sized(0.0F, 0.0F)
			.noSave()
			.noSummon()
			.clientTrackingRange(10));

	private ModEntities() {
	}

	public static void init() {
	}

	private static <T extends Entity> EntityType<T> register(String name, EntityType.Builder<T> builder) {
		ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, WildernessMod.id(name));
		return Registry.register(BuiltInRegistries.ENTITY_TYPE, key, builder.build(key));
	}
}
