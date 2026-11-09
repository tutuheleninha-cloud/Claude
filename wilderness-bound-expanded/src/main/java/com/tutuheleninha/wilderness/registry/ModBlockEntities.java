package com.tutuheleninha.wilderness.registry;

import com.tutuheleninha.wilderness.WildernessMod;
import com.tutuheleninha.wilderness.block.entity.CookingPotBlockEntity;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.block.entity.BlockEntityType;

import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;

public final class ModBlockEntities {
	public static final BlockEntityType<CookingPotBlockEntity> COOKING_POT = Registry.register(BuiltInRegistries.BLOCK_ENTITY_TYPE,
			WildernessMod.id("cooking_pot"),
			FabricBlockEntityTypeBuilder.create(CookingPotBlockEntity::new, ModBlocks.COOKING_POT).build());

	private ModBlockEntities() {
	}

	public static void init() {
	}
}
