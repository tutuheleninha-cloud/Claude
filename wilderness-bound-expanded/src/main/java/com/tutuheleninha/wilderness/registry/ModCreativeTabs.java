package com.tutuheleninha.wilderness.registry;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;

/**
 * Puts every new item next to its closest vanilla relative, the way a vanilla update would. There is no mod tab.
 */
public final class ModCreativeTabs {
	private ModCreativeTabs() {
	}

	public static void init() {
		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.BUILDING_BLOCKS).register(output -> {
			for (WoodKind wood : WoodKind.values()) {
				output.insertAfter(wood.strippedWood(), stacks(ModBlocks.HOLLOW_LOGS.get(wood)));
				output.insertAfter(wood.planks(), stacks(ModBlocks.PARQUETS.get(wood)));
				output.insertAfter(wood.slab(), stacks(ModBlocks.PARQUET_SLABS.get(wood)));
			}

			output.insertAfter(Blocks.MUD_BRICK_WALL, stacks(ModBlocks.PEAT_BRICKS, ModBlocks.PEAT_BRICK_STAIRS,
					ModBlocks.PEAT_BRICK_SLAB, ModBlocks.PEAT_BRICK_WALL, ModBlocks.THATCH, ModBlocks.THATCH_STAIRS, ModBlocks.THATCH_SLAB));
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COLORED_BLOCKS).register(output -> {
			output.insertAfter(Blocks.TERRACOTTA, stacks(ModBlocks.TERRACOTTA_STAIRS, ModBlocks.TERRACOTTA_SLAB, ModBlocks.TERRACOTTA_WALL));

			for (DyeColor color : DyeColor.values()) {
				output.insertAfter(Blocks.DYED_TERRACOTTA.pick(color), stacks(ModBlocks.DYED_TERRACOTTA_STAIRS.get(color),
						ModBlocks.DYED_TERRACOTTA_SLABS.get(color), ModBlocks.DYED_TERRACOTTA_WALLS.get(color)));
				output.insertAfter(Blocks.CONCRETE_SLAB.pick(color), stacks(ModBlocks.CONCRETE_WALLS.get(color)));
			}
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.NATURAL_BLOCKS).register(output -> {
			output.insertAfter(Blocks.MUD, stacks(ModBlocks.PEAT));
			output.insertAfter(Blocks.SUGAR_CANE, stacks(ModBlocks.CATTAIL));
			output.insertAfter(Blocks.CORNFLOWER, stacks(ModBlocks.ASTER));
			output.insertAfter(Blocks.PEONY, stacks(ModBlocks.GOLDENROD));
			output.insertAfter(Items.SWEET_BERRIES, stacks(ModItems.CRANBERRIES));
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(output -> {
			output.insertAfter(Blocks.SOUL_CAMPFIRE, stacks(ModBlocks.COOKING_POT));
			output.insertAfter(Blocks.SOUL_LANTERN, stacks(ModBlocks.ANTLER_CHANDELIER));
			output.insertAfter(Blocks.STRAW_BED, stacks(ModBlocks.LOG_BENCHES.values().toArray(new Block[0])));
			output.insertAfter(Blocks.LODESTONE, stacks(ModBlocks.CAIRN));
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(output -> {
			output.insertAfter(Items.ABANDONED_CAMP_MAP, stacks(ModItems.RANGER_LOOKOUT_MAP));
			output.insertAfter(Items.SPYGLASS, stacks(ModItems.WALKING_STICK));
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS).register(output -> {
			output.insertAfter(Items.RABBIT_STEW, stacks(ModItems.FOREST_STEW, ModItems.HEARTY_STEW, ModItems.PUMPKIN_SOUP,
					ModItems.BERRY_COMPOTE));
			output.insertAfter(Items.SWEET_BERRIES, stacks(ModItems.CRANBERRIES));
		});

		CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(output -> {
			output.insertAfter(Items.FEATHER, stacks(ModItems.ANTLER));
			output.insertAfter(Items.WHEAT, stacks(ModItems.ACORN));
			output.insertAfter(Items.FLOWER_BANNER_PATTERN, stacks(ModItems.ANTLERS_BANNER_PATTERN));
		});

		ModEntitySpawnEggs.addToCreativeTab();
	}

	/** Item stacks for blocks or items; blocks are turned into their registered block items. */
	static List<ItemStack> stacks(ItemLike... things) {
		List<ItemStack> list = new ArrayList<>();

		for (ItemLike thing : things) {
			if (thing instanceof Block block) {
				list.add(new ItemStack(ModItems.blockItem(block)));
			} else {
				list.add(new ItemStack(thing));
			}
		}

		return list;
	}
}
