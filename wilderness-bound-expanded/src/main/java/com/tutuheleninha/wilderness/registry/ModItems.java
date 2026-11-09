package com.tutuheleninha.wilderness.registry;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

import com.tutuheleninha.wilderness.WildernessMod;

import net.minecraft.core.HolderLookup;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.DoubleHighBlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.MapItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BannerPattern;
import net.minecraft.world.level.storage.loot.providers.number.ints.ContextIntProviders;

public final class ModItems {
	/** Block items, keyed by their block. Filled in {@link #init()}. */
	public static final Map<Block, Item> BLOCK_ITEMS = new HashMap<>();

	// --- Foods ------------------------------------------------------------------------------------------------------
	public static final Item CRANBERRIES = register("cranberries",
			properties -> new BlockItem(ModBlocks.CRANBERRY_BUSH, properties),
			new Item.Properties()
					.food(new FoodProperties(2, 0.4F, false))
					.compostable(ContextIntProviders.COMPOSTABLE_LOW)
					.useItemDescriptionPrefix());
	public static final Item FOREST_STEW = register("forest_stew", Item::new, stew(8, 9.6F));
	public static final Item HEARTY_STEW = register("hearty_stew", Item::new, stew(10, 12.0F));
	public static final Item PUMPKIN_SOUP = register("pumpkin_soup", Item::new, stew(7, 8.4F));
	public static final Item BERRY_COMPOTE = register("berry_compote", Item::new, stew(6, 7.2F));

	// --- Materials --------------------------------------------------------------------------------------------------
	public static final Item ACORN = register("acorn", Item::new, new Item.Properties()
			.compostable(ContextIntProviders.COMPOSTABLE_LOW));
	public static final Item ANTLER = register("antler", Item::new, new Item.Properties());

	// --- Tools ------------------------------------------------------------------------------------------------------
	/** Held in either hand, lets you walk up full blocks like a horse. */
	public static final Item WALKING_STICK = register("walking_stick", Item::new, new Item.Properties()
			.stacksTo(1)
			.attributes(ItemAttributeModifiers.builder()
					.add(Attributes.STEP_HEIGHT,
							new AttributeModifier(WildernessMod.id("walking_stick_step_height"), 0.5, AttributeModifier.Operation.ADD_VALUE),
							EquipmentSlotGroup.HAND)
					.build())
			.cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_ITEMS_SMALL));
	public static final Item RANGER_LOOKOUT_MAP = register("ranger_lookout_map", MapItem::new, new Item.Properties());
	public static final Item ANTLERS_BANNER_PATTERN = register("antlers_banner_pattern", Item::new, new Item.Properties()
			.stacksTo(1)
			.rarity(Rarity.UNCOMMON)
			.delayedComponent(DataComponents.PROVIDES_BANNER_PATTERNS, registries -> {
				HolderLookup.RegistryLookup<BannerPattern> patterns = registries.lookupOrThrow(Registries.BANNER_PATTERN);
				return patterns.getOrThrow(ModTags.PATTERN_ITEM_ANTLERS);
			}));

	private ModItems() {
	}

	private static Item.Properties stew(int nutrition, float saturation) {
		return new Item.Properties()
				.stacksTo(1)
				.food(new FoodProperties(nutrition, saturation, false))
				.usingConvertsTo(Items.BOWL);
	}

	public static void init() {
		for (Block block : ModBlocks.BLOCKS_WITH_ITEMS) {
			String name = BuiltInRegistries.BLOCK.getKey(block).getPath();
			Item.Properties properties = blockItemProperties(block);
			Function<Item.Properties, Item> factory = block == ModBlocks.CATTAIL || block == ModBlocks.GOLDENROD
					? itemProperties -> new DoubleHighBlockItem(block, itemProperties)
					: itemProperties -> new BlockItem(block, itemProperties);
			BLOCK_ITEMS.put(block, register(name, factory, properties.useBlockDescriptionPrefix()));
		}
	}

	private static Item.Properties blockItemProperties(Block block) {
		Item.Properties properties = new Item.Properties();

		for (WoodKind wood : WoodKind.values()) {
			if (wood.isNether()) {
				continue;
			}

			if (block == ModBlocks.HOLLOW_LOGS.get(wood) || block == ModBlocks.LOG_BENCHES.get(wood) || block == ModBlocks.PARQUETS.get(wood)) {
				return properties.cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_BLOCKS);
			}

			if (block == ModBlocks.PARQUET_SLABS.get(wood)) {
				return properties.cookingFuel(ContextIntProviders.COOKING_TIME_WOOD_SLABS);
			}
		}

		if (block == ModBlocks.PEAT) {
			return properties.cookingFuel(ModFuels.PEAT);
		}

		if (block == ModBlocks.THATCH) {
			return properties.compostable(ContextIntProviders.COMPOSTABLE_MEDIUM_HIGH);
		}

		if (block == ModBlocks.CATTAIL) {
			return properties.compostable(ContextIntProviders.COMPOSTABLE_LOW_MEDIUM);
		}

		if (block == ModBlocks.ASTER || block == ModBlocks.GOLDENROD) {
			return properties.compostable(ContextIntProviders.COMPOSTABLE_MEDIUM);
		}

		return properties;
	}

	static <I extends Item> I register(String name, Function<Item.Properties, I> factory, Item.Properties properties) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, WildernessMod.id(name));
		I item = factory.apply(properties.setId(key));

		if (item instanceof BlockItem blockItem) {
			// Same as vanilla's Items.registerItem: lets Block#asItem find this item.
			blockItem.registerBlocks(Item.BY_BLOCK, item);
		}

		return Registry.register(BuiltInRegistries.ITEM, key, item);
	}

	public static Item blockItem(Block block) {
		return BLOCK_ITEMS.get(block);
	}
}
