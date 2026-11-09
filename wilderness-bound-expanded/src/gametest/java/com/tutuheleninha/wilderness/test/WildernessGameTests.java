package com.tutuheleninha.wilderness.test;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.Blocks;

import net.fabricmc.fabric.api.gametest.v1.GameTest;

public class WildernessGameTests {
	@GameTest
	public void smoke(GameTestHelper helper) {
		helper.setBlock(0, 1, 0, Blocks.STONE);
		helper.succeedWhen(() ->
				helper.assertBlock(new BlockPos(0, 1, 0), block -> block == Blocks.STONE, block -> Component.literal("Expected stone"))
		);
	}
}
