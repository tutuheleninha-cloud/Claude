package com.tutuheleninha.wilderness.client;

import com.tutuheleninha.wilderness.registry.ModEntities;

import net.minecraft.client.renderer.entity.NoopRenderer;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;

public class WildernessClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		EntityRendererRegistry.register(ModEntities.SEAT, NoopRenderer::new);
	}
}
