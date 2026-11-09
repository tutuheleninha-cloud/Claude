package com.tutuheleninha.wilderness;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tutuheleninha.wilderness.registry.ModBlockEntities;
import com.tutuheleninha.wilderness.registry.ModBlocks;
import com.tutuheleninha.wilderness.registry.ModCreativeTabs;
import com.tutuheleninha.wilderness.registry.ModEntities;
import com.tutuheleninha.wilderness.registry.ModEntitySpawnEggs;
import com.tutuheleninha.wilderness.registry.ModEvents;
import com.tutuheleninha.wilderness.registry.ModItems;

import net.minecraft.resources.Identifier;

import net.fabricmc.api.ModInitializer;

public class WildernessMod implements ModInitializer {
	public static final String MOD_ID = "wilderness";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		ModBlocks.init();
		ModItems.init();
		ModBlockEntities.init();
		ModEntities.init();
		ModEntitySpawnEggs.init();
		ModCreativeTabs.init();
		ModEvents.init();
		LOGGER.info("Wilderness Bound Expanded loaded");
	}

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}
}
