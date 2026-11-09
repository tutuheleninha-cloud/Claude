package com.tutuheleninha.wilderness.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.SimpleWaterloggedBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.material.FluidState;
import net.minecraft.world.level.material.Fluids;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A log with its heartwood carved out. The opening is wide enough for small mobs, and for players who crawl.
 * Made by using an axe on a stripped log.
 */
public class HollowLogBlock extends Block implements SimpleWaterloggedBlock {
	public static final EnumProperty<Direction.Axis> AXIS = BlockStateProperties.AXIS;
	public static final BooleanProperty WATERLOGGED = BlockStateProperties.WATERLOGGED;

	private static final VoxelShape SHAPE_Y = Shapes.or(
			Block.box(0, 0, 0, 16, 16, 2),
			Block.box(0, 0, 14, 16, 16, 16),
			Block.box(0, 0, 2, 2, 16, 14),
			Block.box(14, 0, 2, 16, 16, 14));
	private static final VoxelShape SHAPE_X = Shapes.or(
			Block.box(0, 0, 0, 16, 2, 16),
			Block.box(0, 14, 0, 16, 16, 16),
			Block.box(0, 2, 0, 16, 14, 2),
			Block.box(0, 2, 14, 16, 14, 16));
	private static final VoxelShape SHAPE_Z = Shapes.or(
			Block.box(0, 0, 0, 16, 2, 16),
			Block.box(0, 14, 0, 16, 16, 16),
			Block.box(0, 2, 0, 2, 14, 16),
			Block.box(14, 2, 0, 16, 14, 16));

	public HollowLogBlock(Properties properties) {
		super(properties);
		this.registerDefaultState(this.stateDefinition.any().setValue(AXIS, Direction.Axis.Y).setValue(WATERLOGGED, false));
	}

	@Override
	protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
		builder.add(AXIS, WATERLOGGED);
	}

	@Override
	protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
		return switch (state.getValue(AXIS)) {
			case X -> SHAPE_X;
			case Z -> SHAPE_Z;
			default -> SHAPE_Y;
		};
	}

	@Override
	public BlockState getStateForPlacement(BlockPlaceContext context) {
		FluidState fluid = context.getLevel().getFluidState(context.getClickedPos());
		return this.defaultBlockState()
				.setValue(AXIS, context.getClickedFace().getAxis())
				.setValue(WATERLOGGED, fluid.getType() == Fluids.WATER);
	}

	@Override
	protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction direction,
			BlockPos neighborPos, BlockState neighborState, RandomSource random) {
		if (state.getValue(WATERLOGGED)) {
			ticks.scheduleTick(pos, Fluids.WATER, Fluids.WATER.getTickDelay(level));
		}

		return super.updateShape(state, level, ticks, pos, direction, neighborPos, neighborState, random);
	}

	@Override
	protected FluidState getFluidState(BlockState state) {
		return state.getValue(WATERLOGGED) ? Fluids.WATER.getSource(false) : super.getFluidState(state);
	}

	@Override
	protected BlockState rotate(BlockState state, Rotation rotation) {
		return RotatedPillarBlock.rotatePillar(state, rotation);
	}

	@Override
	protected boolean useShapeForLightOcclusion(BlockState state) {
		return true;
	}

	@Override
	protected boolean isPathfindable(BlockState state, PathComputationType type) {
		return false;
	}
}
