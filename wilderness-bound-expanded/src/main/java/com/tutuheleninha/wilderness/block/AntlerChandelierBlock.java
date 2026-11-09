package com.tutuheleninha.wilderness.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.pathfinder.PathComputationType;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A rustic hanging light made of shed antlers and candles. Must hang from a ceiling.
 */
public class AntlerChandelierBlock extends Block {
	private static final VoxelShape SHAPE = Block.box(1, 3, 1, 15, 16, 15);
	/** Candle wick positions, relative to the block, in pixels. */
	private static final double[][] CANDLES = {{3.5, 9.0, 8.0}, {12.5, 9.0, 8.0}, {8.0, 9.0, 3.5}, {8.0, 9.0, 12.5}};

	public AntlerChandelierBlock(Properties properties) {
		super(properties);
	}

	@Override
	protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
		return SHAPE;
	}

	@Override
	protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
		return Block.canSupportCenter(level, pos.above(), Direction.DOWN);
	}

	@Override
	protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks, BlockPos pos, Direction direction,
			BlockPos neighborPos, BlockState neighborState, RandomSource random) {
		if (direction == Direction.UP && !state.canSurvive(level, pos)) {
			return Blocks.AIR.defaultBlockState();
		}

		return super.updateShape(state, level, ticks, pos, direction, neighborPos, neighborState, random);
	}

	@Override
	public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
		for (double[] candle : CANDLES) {
			double x = pos.getX() + candle[0] / 16.0;
			double y = pos.getY() + candle[1] / 16.0 + 0.06;
			double z = pos.getZ() + candle[2] / 16.0;

			if (random.nextFloat() < 0.3F) {
				level.addParticle(ParticleTypes.SMOKE, x, y, z, 0.0, 0.0, 0.0);
			}

			level.addParticle(ParticleTypes.SMALL_FLAME, x, y, z, 0.0, 0.0, 0.0);
		}
	}

	@Override
	protected boolean isPathfindable(BlockState state, PathComputationType type) {
		return false;
	}
}
