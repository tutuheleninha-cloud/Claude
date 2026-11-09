package com.tutuheleninha.wilderness.registry;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import com.tutuheleninha.wilderness.WildernessMod;
import com.tutuheleninha.wilderness.block.AntlerChandelierBlock;
import com.tutuheleninha.wilderness.block.CairnBlock;
import com.tutuheleninha.wilderness.block.CattailBlock;
import com.tutuheleninha.wilderness.block.CookingPotBlock;
import com.tutuheleninha.wilderness.block.CranberryBushBlock;
import com.tutuheleninha.wilderness.block.HollowLogBlock;
import com.tutuheleninha.wilderness.block.LogBenchBlock;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.FlowerPotBlock;
import net.minecraft.world.level.block.HayBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.TallFlowerBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

import net.fabricmc.fabric.api.registry.FlammableBlockRegistry;

public final class ModBlocks {
	/** Blocks that get a plain {@link net.minecraft.world.item.BlockItem}, in registration order. */
	static final List<Block> BLOCKS_WITH_ITEMS = new ArrayList<>();

	// --- Wood families -------------------------------------------------------------------------------------------
	public static final Map<WoodKind, Block> HOLLOW_LOGS = new EnumMap<>(WoodKind.class);
	public static final Map<WoodKind, Block> LOG_BENCHES = new EnumMap<>(WoodKind.class);
	public static final Map<WoodKind, Block> PARQUETS = new EnumMap<>(WoodKind.class);
	public static final Map<WoodKind, Block> PARQUET_SLABS = new EnumMap<>(WoodKind.class);
	/** Stripped log -> hollow log, used when an axe is used on a stripped log. */
	public static final Map<Block, Block> HOLLOW_LOG_BY_STRIPPED_LOG;

	static {
		Map<Block, Block> hollowByStripped = new HashMap<>();

		for (WoodKind wood : WoodKind.values()) {
			Block hollow = registerWithItem("hollow_" + wood.logName(), HollowLogBlock::new,
					BlockBehaviour.Properties.ofFullCopy(wood.log()).noOcclusion());
			HOLLOW_LOGS.put(wood, hollow);
			hollowByStripped.put(wood.strippedLog(), hollow);

			// The log's map colour function reads the vertical AXIS property, which benches don't have.
			LOG_BENCHES.put(wood, registerWithItem(wood.logName() + "_bench", LogBenchBlock::new,
					BlockBehaviour.Properties.ofFullCopy(wood.log()).mapColor(wood.planks().defaultMapColor()).noOcclusion()));

			PARQUETS.put(wood, registerWithItem(wood.woodName() + "_parquet", Block::new,
					BlockBehaviour.Properties.ofFullCopy(wood.planks())));
			PARQUET_SLABS.put(wood, registerWithItem(wood.woodName() + "_parquet_slab", SlabBlock::new,
					BlockBehaviour.Properties.ofFullCopy(wood.planks())));
		}

		HOLLOW_LOG_BY_STRIPPED_LOG = Collections.unmodifiableMap(hollowByStripped);
	}

	// --- Terracotta and concrete -----------------------------------------------------------------------------------
	public static final Block TERRACOTTA_STAIRS = registerWithItem("terracotta_stairs",
			properties -> new StairBlock(Blocks.TERRACOTTA.defaultBlockState(), properties),
			BlockBehaviour.Properties.ofFullCopy(Blocks.TERRACOTTA));
	public static final Block TERRACOTTA_SLAB = registerWithItem("terracotta_slab", SlabBlock::new,
			BlockBehaviour.Properties.ofFullCopy(Blocks.TERRACOTTA));
	public static final Block TERRACOTTA_WALL = registerWithItem("terracotta_wall", WallBlock::new,
			BlockBehaviour.Properties.ofFullCopy(Blocks.TERRACOTTA).forceSolidOn());

	public static final Map<DyeColor, Block> DYED_TERRACOTTA_STAIRS = new EnumMap<>(DyeColor.class);
	public static final Map<DyeColor, Block> DYED_TERRACOTTA_SLABS = new EnumMap<>(DyeColor.class);
	public static final Map<DyeColor, Block> DYED_TERRACOTTA_WALLS = new EnumMap<>(DyeColor.class);
	public static final Map<DyeColor, Block> CONCRETE_WALLS = new EnumMap<>(DyeColor.class);

	static {
		for (DyeColor color : DyeColor.values()) {
			Block terracotta = Blocks.DYED_TERRACOTTA.pick(color);
			String prefix = color.getSerializedName() + "_terracotta";
			DYED_TERRACOTTA_STAIRS.put(color, registerWithItem(prefix + "_stairs",
					properties -> new StairBlock(terracotta.defaultBlockState(), properties),
					BlockBehaviour.Properties.ofFullCopy(terracotta)));
			DYED_TERRACOTTA_SLABS.put(color, registerWithItem(prefix + "_slab", SlabBlock::new,
					BlockBehaviour.Properties.ofFullCopy(terracotta)));
			DYED_TERRACOTTA_WALLS.put(color, registerWithItem(prefix + "_wall", WallBlock::new,
					BlockBehaviour.Properties.ofFullCopy(terracotta).forceSolidOn()));
		}

		for (DyeColor color : DyeColor.values()) {
			Block concrete = Blocks.CONCRETE.pick(color);
			CONCRETE_WALLS.put(color, registerWithItem(color.getSerializedName() + "_concrete_wall", WallBlock::new,
					BlockBehaviour.Properties.ofFullCopy(concrete).forceSolidOn()));
		}
	}

	// --- Thatch and peat -------------------------------------------------------------------------------------------
	public static final Block THATCH = registerWithItem("thatch", HayBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.TERRACOTTA_YELLOW)
			.instrument(NoteBlockInstrument.BANJO)
			.strength(0.5F)
			.sound(SoundType.GRASS)
			.ignitedByLava());
	public static final Block THATCH_STAIRS = registerWithItem("thatch_stairs",
			properties -> new StairBlock(THATCH.defaultBlockState(), properties), BlockBehaviour.Properties.ofFullCopy(THATCH));
	public static final Block THATCH_SLAB = registerWithItem("thatch_slab", SlabBlock::new,
			BlockBehaviour.Properties.ofFullCopy(THATCH));

	public static final Block PEAT = registerWithItem("peat", Block::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.TERRACOTTA_BROWN)
			.strength(0.5F)
			.sound(SoundType.ROOTED_DIRT));
	public static final Block PEAT_BRICKS = registerWithItem("peat_bricks", Block::new,
			BlockBehaviour.Properties.ofFullCopy(Blocks.MUD_BRICKS).mapColor(MapColor.TERRACOTTA_BROWN));
	public static final Block PEAT_BRICK_STAIRS = registerWithItem("peat_brick_stairs",
			properties -> new StairBlock(PEAT_BRICKS.defaultBlockState(), properties), BlockBehaviour.Properties.ofFullCopy(PEAT_BRICKS));
	public static final Block PEAT_BRICK_SLAB = registerWithItem("peat_brick_slab", SlabBlock::new,
			BlockBehaviour.Properties.ofFullCopy(PEAT_BRICKS));
	public static final Block PEAT_BRICK_WALL = registerWithItem("peat_brick_wall", WallBlock::new,
			BlockBehaviour.Properties.ofFullCopy(PEAT_BRICKS).forceSolidOn());

	// --- Plants -----------------------------------------------------------------------------------------------------
	public static final Block CATTAIL = registerWithItem("cattail", CattailBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.PLANT)
			.noCollision()
			.instabreak()
			.sound(SoundType.GRASS)
			.offsetType(BlockBehaviour.OffsetType.XZ)
			.ignitedByLava()
			.pushReaction(PushReaction.POPPED));
	/** The item for this block is {@link ModItems#CRANBERRIES}, like sweet berries. */
	public static final Block CRANBERRY_BUSH = register("cranberry_bush", CranberryBushBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.PLANT)
			.randomTicks()
			.noCollision()
			.sound(SoundType.SWEET_BERRY_BUSH)
			.pushReaction(PushReaction.POPPED));
	public static final Block ASTER = registerWithItem("aster",
			properties -> new FlowerBlock(MobEffects.SPEED, 6.0F, properties), BlockBehaviour.Properties.of()
					.mapColor(MapColor.PLANT)
					.noCollision()
					.instabreak()
					.sound(SoundType.GRASS)
					.offsetType(BlockBehaviour.OffsetType.XZ)
					.pushReaction(PushReaction.POPPED));
	public static final Block POTTED_ASTER = register("potted_aster",
			properties -> new FlowerPotBlock(ASTER, properties), Blocks.flowerPotProperties());
	public static final Block GOLDENROD = registerWithItem("goldenrod", TallFlowerBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.PLANT)
			.noCollision()
			.instabreak()
			.sound(SoundType.GRASS)
			.offsetType(BlockBehaviour.OffsetType.XZ)
			.ignitedByLava()
			.pushReaction(PushReaction.POPPED));

	// --- Camping ----------------------------------------------------------------------------------------------------
	public static final Block CAIRN = registerWithItem("cairn", CairnBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.STONE)
			.strength(0.8F)
			.sound(SoundType.STONE)
			.noOcclusion()
			.pushReaction(PushReaction.POPPED));
	public static final Block ANTLER_CHANDELIER = registerWithItem("antler_chandelier", AntlerChandelierBlock::new,
			BlockBehaviour.Properties.of()
					.mapColor(MapColor.SAND)
					.strength(0.6F)
					.sound(SoundType.BONE_BLOCK)
					.lightLevel(state -> 14)
					.noOcclusion()
					.pushReaction(PushReaction.POPPED));
	public static final Block COOKING_POT = registerWithItem("cooking_pot", CookingPotBlock::new, BlockBehaviour.Properties.of()
			.mapColor(MapColor.METAL)
			.requiresCorrectToolForDrops()
			.strength(2.0F)
			.sound(SoundType.LANTERN)
			.noOcclusion());

	private ModBlocks() {
	}

	public static void init() {
		FlammableBlockRegistry flammable = FlammableBlockRegistry.getDefaultInstance();

		for (WoodKind wood : WoodKind.values()) {
			if (!wood.isNether()) {
				flammable.add(HOLLOW_LOGS.get(wood), 5, 5);
				flammable.add(LOG_BENCHES.get(wood), 5, 5);
				flammable.add(PARQUETS.get(wood), 5, 20);
				flammable.add(PARQUET_SLABS.get(wood), 5, 20);
			}
		}

		flammable.add(THATCH, 60, 20);
		flammable.add(THATCH_STAIRS, 60, 20);
		flammable.add(THATCH_SLAB, 60, 20);
		flammable.add(CATTAIL, 60, 100);
		flammable.add(ASTER, 60, 100);
		flammable.add(GOLDENROD, 60, 100);
	}

	private static <B extends Block> B registerWithItem(String name, Function<BlockBehaviour.Properties, B> factory,
			BlockBehaviour.Properties properties) {
		B block = register(name, factory, properties);
		BLOCKS_WITH_ITEMS.add(block);
		return block;
	}

	static <B extends Block> B register(String name, Function<BlockBehaviour.Properties, B> factory,
			BlockBehaviour.Properties properties) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, WildernessMod.id(name));
		B block = factory.apply(properties.setId(key));
		return Registry.register(BuiltInRegistries.BLOCK, key, block);
	}
}
