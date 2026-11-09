package com.tutuheleninha.wilderness.test;

import java.util.HashSet;
import java.util.Set;

import com.tutuheleninha.wilderness.block.CookingPotBlock;
import com.tutuheleninha.wilderness.block.PotContents;
import com.tutuheleninha.wilderness.block.entity.CookingPotBlockEntity;
import com.tutuheleninha.wilderness.registry.ModBlocks;
import com.tutuheleninha.wilderness.worldgen.ModBiomes;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.MultiNoiseBiomeSourceParameterList;
import net.minecraft.world.level.biome.MultiNoiseBiomeSourceParameterLists;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CampfireBlock;

import net.fabricmc.fabric.api.gametest.v1.GameTest;

public class WildernessGameTests {
	@GameTest
	public void smoke(GameTestHelper helper) {
		helper.setBlock(0, 1, 0, Blocks.STONE);
		helper.succeedWhen(() ->
				helper.assertBlock(new BlockPos(0, 1, 0), block -> block == Blocks.STONE, block -> Component.literal("Expected stone"))
		);
	}

	/** The overworld climate map must contain both new biomes (checks the OverworldBiomeBuilder mixin). */
	@GameTest
	public void newBiomesAreInTheOverworld(GameTestHelper helper) {
		MultiNoiseBiomeSourceParameterList list = helper.getLevel().registryAccess()
				.lookupOrThrow(Registries.MULTI_NOISE_BIOME_SOURCE_PARAMETER_LIST)
				.getOrThrow(MultiNoiseBiomeSourceParameterLists.OVERWORLD)
				.value();
		Set<ResourceKey<Biome>> biomes = new HashSet<>();

		for (var entry : list.parameters().values()) {
			Holder<Biome> holder = entry.getSecond();
			holder.unwrapKey().ifPresent(biomes::add);
		}

		helper.assertTrue(biomes.contains(ModBiomes.OLD_GROWTH_DAPPLED_FOREST), "Old Growth Dappled Forest is not placed in the overworld");
		helper.assertTrue(biomes.contains(ModBiomes.BOG), "Bog is not placed in the overworld");
		helper.assertTrue(biomes.contains(net.minecraft.world.level.biome.Biomes.DAPPLED_FOREST), "Dappled Forest disappeared");
		helper.assertTrue(biomes.contains(net.minecraft.world.level.biome.Biomes.SWAMP), "Swamp disappeared");
		helper.succeed();
	}

	/** A pot of water over a lit campfire turns forest stew ingredients into three bowls of stew. */
	@GameTest(maxTicks = 400)
	public void cookingPotCooksForestStew(GameTestHelper helper) {
		BlockPos fire = new BlockPos(1, 1, 1);
		BlockPos potPos = fire.above();
		helper.setBlock(fire, Blocks.CAMPFIRE.defaultBlockState().setValue(CampfireBlock.LIT, true));
		helper.setBlock(potPos, ModBlocks.COOKING_POT.defaultBlockState()
				.setValue(CookingPotBlock.CONTENTS, PotContents.WATER)
				.setValue(CookingPotBlock.SERVINGS, 3));
		CookingPotBlockEntity pot = helper.getBlockEntity(potPos, CookingPotBlockEntity.class);
		pot.addIngredient(new ItemStack(Items.SHELF_MUSHROOM));
		pot.addIngredient(new ItemStack(Items.BROWN_MUSHROOM));
		pot.addIngredient(new ItemStack(Items.CARROT));
		pot.addIngredient(new ItemStack(Items.POTATO));

		helper.succeedWhen(() -> helper.assertBlockState(potPos,
				state -> state.is(ModBlocks.COOKING_POT) && state.getValue(CookingPotBlock.CONTENTS) == PotContents.STEW
						&& state.getValue(CookingPotBlock.SERVINGS) == 3,
				state -> Component.literal("Pot did not cook: " + state)));
	}
}
