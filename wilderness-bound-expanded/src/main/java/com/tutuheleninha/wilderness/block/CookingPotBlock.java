package com.tutuheleninha.wilderness.block;

import com.tutuheleninha.wilderness.block.entity.CookingPotBlockEntity;
import com.tutuheleninha.wilderness.recipe.CookingPotRecipes;
import com.tutuheleninha.wilderness.registry.ModBlockEntities;
import com.tutuheleninha.wilderness.registry.ModTags;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * An iron pot that cooks stews and soups in batches. Fill it with water, set it over a fire, add up to four
 * ingredients and wait. Each pot of stew fills three bowls.
 *
 * <p>Over a campfire it hangs from a small tripod whose legs reach down to the logs.
 */
public class CookingPotBlock extends BaseEntityBlock {
	public static final EnumProperty<Direction> FACING = BlockStateProperties.HORIZONTAL_FACING;
	public static final EnumProperty<PotContents> CONTENTS = EnumProperty.create("contents", PotContents.class);
	public static final IntegerProperty SERVINGS = IntegerProperty.create("servings", 0, 3);
	/** True when the pot sits above a campfire or fire, which shows the tripod. */
	public static final BooleanProperty HANGING = BlockStateProperties.HANGING;

	private static final VoxelShape SHAPE = Block.box(2, 0, 2, 14, 10, 14);

	public CookingPotBlock(Properties properties) {
		super(properties);
		this.registerDefaultState(this.stateDefinition.any()
				.setValue(FACING, Direction.NORTH)
				.setValue(CONTENTS, PotContents.EMPTY)
				.setValue(SERVINGS, 0)
				.setValue(HANGING, false));
	}

	@Override
	protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
		builder.add(FACING, CONTENTS, SERVINGS, HANGING);
	}

	@Override
	public BlockState getStateForPlacement(BlockPlaceContext context) {
		BlockPos below = context.getClickedPos().below();
		return this.defaultBlockState()
				.setValue(FACING, context.getHorizontalDirection().getOpposite())
				.setValue(HANGING, isFireBelow(context.getLevel().getBlockState(below)));
	}

	@Override
	protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction direction,
			BlockPos neighborPos, BlockState neighborState, RandomSource random) {
		if (direction == Direction.DOWN) {
			state = state.setValue(HANGING, isFireBelow(neighborState));
		}

		return super.updateShape(state, level, ticks, pos, direction, neighborPos, neighborState, random);
	}

	private static boolean isFireBelow(BlockState below) {
		return below.is(BlockTags.CAMPFIRES) || below.is(BlockTags.FIRE);
	}

	/** Whether something below the pot is hot enough to cook with. */
	public static boolean isHeated(BlockGetter level, BlockPos pos) {
		BlockState below = level.getBlockState(pos.below());

		if (below.is(BlockTags.CAMPFIRES)) {
			return below.getValue(CampfireBlock.LIT);
		}

		return below.is(ModTags.COOKING_POT_HEAT_SOURCES);
	}

	@Override
	protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
		return SHAPE;
	}

	@Override
	protected RenderShape getRenderShape(BlockState state) {
		return RenderShape.MODEL;
	}

	@Override
	public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
		return new CookingPotBlockEntity(pos, state);
	}

	@Override
	public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
		return level.isClientSide() ? null : createTickerHelper(type, ModBlockEntities.COOKING_POT, CookingPotBlockEntity::serverTick);
	}

	@Override
	protected InteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
			InteractionHand hand, BlockHitResult hitResult) {
		if (!(level.getBlockEntity(pos) instanceof CookingPotBlockEntity pot)) {
			return InteractionResult.TRY_WITH_EMPTY_HAND;
		}

		PotContents contents = state.getValue(CONTENTS);

		if (contents == PotContents.EMPTY && stack.is(Items.WATER_BUCKET)) {
			if (!level.isClientSide()) {
				player.setItemInHand(hand, ItemUtils.createFilledResult(stack, player, new ItemStack(Items.BUCKET)));
				setContents(level, pos, state, PotContents.WATER, 3, player);
			}

			level.playSound(player, pos, SoundEvents.BUCKET_EMPTY, SoundSource.BLOCKS, 1.0F, 1.0F);
			return InteractionResult.SUCCESS;
		}

		if (contents == PotContents.WATER && stack.is(Items.BUCKET) && pot.ingredientCount() == 0) {
			if (!level.isClientSide()) {
				player.setItemInHand(hand, ItemUtils.createFilledResult(stack, player, new ItemStack(Items.WATER_BUCKET)));
				setContents(level, pos, state, PotContents.EMPTY, 0, player);
			}

			level.playSound(player, pos, SoundEvents.BUCKET_FILL, SoundSource.BLOCKS, 1.0F, 1.0F);
			return InteractionResult.SUCCESS;
		}

		if (contents == PotContents.WATER && CookingPotRecipes.isIngredient(stack) && pot.canAddIngredient()) {
			if (!level.isClientSide()) {
				pot.addIngredient(stack.copyWithCount(1));
				stack.consume(1, player);
				level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, state));
			}

			level.playSound(player, pos, SoundEvents.GENERIC_SPLASH, SoundSource.BLOCKS, 0.4F, 1.4F);
			return InteractionResult.SUCCESS;
		}

		if (contents == PotContents.STEW && stack.is(Items.BOWL)) {
			if (!level.isClientSide()) {
				ItemStack serving = pot.takeServing();
				player.setItemInHand(hand, ItemUtils.createFilledResult(stack, player, serving));
				int left = state.getValue(SERVINGS) - 1;

				if (left <= 0) {
					pot.clearResult();
					setContents(level, pos, state, PotContents.EMPTY, 0, player);
				} else {
					setContents(level, pos, state, PotContents.STEW, left, player);
				}
			}

			level.playSound(player, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, 1.0F, 0.8F);
			return InteractionResult.SUCCESS;
		}

		return InteractionResult.TRY_WITH_EMPTY_HAND;
	}

	@Override
	protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
		// Sneak-use with an empty hand fishes the last ingredient back out.
		if (player.isSecondaryUseActive() && state.getValue(CONTENTS) == PotContents.WATER
				&& level.getBlockEntity(pos) instanceof CookingPotBlockEntity pot && pot.ingredientCount() > 0) {
			if (!level.isClientSide()) {
				ItemStack taken = pot.removeLastIngredient();

				if (!player.getInventory().add(taken)) {
					player.drop(taken, false);
				}
			}

			level.playSound(player, pos, SoundEvents.GENERIC_SPLASH, SoundSource.BLOCKS, 0.3F, 1.6F);
			return InteractionResult.SUCCESS;
		}

		return InteractionResult.PASS;
	}

	private static void setContents(Level level, BlockPos pos, BlockState state, PotContents contents, int servings, Player player) {
		BlockState updated = state.setValue(CONTENTS, contents).setValue(SERVINGS, servings);
		level.setBlock(pos, updated, Block.UPDATE_ALL);
		level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, updated));
	}

	@Override
	public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
		if (state.getValue(CONTENTS) == PotContents.EMPTY || !isHeated(level, pos)) {
			return;
		}

		double surface = pos.getY() + 0.5 + state.getValue(SERVINGS) * 0.06;

		for (int i = 0; i < 2; i++) {
			double x = pos.getX() + 0.3 + random.nextDouble() * 0.4;
			double z = pos.getZ() + 0.3 + random.nextDouble() * 0.4;
			level.addParticle(ParticleTypes.BUBBLE_POP, x, surface, z, 0.0, 0.02, 0.0);
		}

		if (random.nextInt(4) == 0) {
			level.addParticle(ParticleTypes.WHITE_SMOKE, pos.getX() + 0.5, surface + 0.1, pos.getZ() + 0.5, 0.0, 0.03, 0.0);
		}

		if (random.nextInt(10) == 0) {
			level.playLocalSound(pos.getX() + 0.5, surface, pos.getZ() + 0.5, SoundEvents.BUBBLE_COLUMN_BUBBLE_POP,
					SoundSource.BLOCKS, 0.3F, 0.8F + random.nextFloat() * 0.3F, false);
		}
	}

	@Override
	protected boolean isPathfindable(BlockState state, PathComputationType type) {
		return false;
	}
}
