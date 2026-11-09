package com.tutuheleninha.wilderness.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A small stack of stones that marks a trail. Up to four stones can be stacked, like sea pickles.
 */
public class CairnBlock extends Block {
	public static final int MAX_STONES = 4;
	public static final IntegerProperty STONES = IntegerProperty.create("stones", 1, MAX_STONES);

	private static final VoxelShape[] SHAPES = new VoxelShape[] {
			Block.box(5, 0, 5, 11, 3, 11),
			Block.box(4, 0, 4, 12, 6, 12),
			Block.box(4, 0, 4, 12, 9, 12),
			Block.box(3, 0, 3, 13, 11, 13)
	};

	public CairnBlock(Properties properties) {
		super(properties);
		this.registerDefaultState(this.stateDefinition.any().setValue(STONES, 1));
	}

	@Override
	protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
		builder.add(STONES);
	}

	@Override
	protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
		return SHAPES[state.getValue(STONES) - 1];
	}

	@Override
	public BlockState getStateForPlacement(BlockPlaceContext context) {
		BlockState existing = context.getLevel().getBlockState(context.getClickedPos());

		if (existing.is(this)) {
			return existing.setValue(STONES, Math.min(MAX_STONES, existing.getValue(STONES) + 1));
		}

		return super.getStateForPlacement(context);
	}

	@Override
	protected boolean canBeReplaced(BlockState state, BlockPlaceContext context) {
		if (!context.isSecondaryUseActive() && context.getItemInHand().is(this.asItem()) && state.getValue(STONES) < MAX_STONES) {
			return true;
		}

		return super.canBeReplaced(state, context);
	}

	@Override
	protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
		BlockPos below = pos.below();
		return level.getBlockState(below).isFaceSturdy(level, below, Direction.UP);
	}

	@Override
	protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction direction,
			BlockPos neighborPos, BlockState neighborState, RandomSource random) {
		if (direction == Direction.DOWN && !state.canSurvive(level, pos)) {
			return Blocks.AIR.defaultBlockState();
		}

		return super.updateShape(state, level, ticks, pos, direction, neighborPos, neighborState, random);
	}

	@Override
	protected boolean isPathfindable(BlockState state, PathComputationType type) {
		return false;
	}
}
