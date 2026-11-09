package com.tutuheleninha.wilderness.registry;

import com.tutuheleninha.wilderness.block.HollowLogBlock;

import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.gameevent.GameEvent;

import net.fabricmc.fabric.api.event.player.UseBlockCallback;

public final class ModEvents {
	private ModEvents() {
	}

	public static void init() {
		// Using an axe on a stripped log carves it into a hollow log, one step past stripping.
		UseBlockCallback.EVENT.register((player, level, hand, hitResult) -> {
			if (player.isSpectator()) {
				return InteractionResult.PASS;
			}

			ItemStack stack = player.getItemInHand(hand);

			if (!stack.is(ItemTags.AXES)) {
				return InteractionResult.PASS;
			}

			BlockPos pos = hitResult.getBlockPos();
			BlockState state = level.getBlockState(pos);
			Block hollow = ModBlocks.HOLLOW_LOG_BY_STRIPPED_LOG.get(state.getBlock());

			if (hollow == null || !state.hasProperty(RotatedPillarBlock.AXIS)) {
				return InteractionResult.PASS;
			}

			level.playSound(player, pos, SoundEvents.AXE_STRIP.value(), SoundSource.BLOCKS, 1.0F, 0.8F);

			if (!level.isClientSide()) {
				BlockState carved = hollow.defaultBlockState()
						.setValue(HollowLogBlock.AXIS, state.getValue(RotatedPillarBlock.AXIS))
						.setValue(HollowLogBlock.WATERLOGGED, false);
				level.setBlock(pos, carved, Block.UPDATE_ALL_IMMEDIATE);
				level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(player, carved));
				stack.hurtAndBreak(1, player, hand);
			}

			return InteractionResult.SUCCESS;
		});
	}
}
