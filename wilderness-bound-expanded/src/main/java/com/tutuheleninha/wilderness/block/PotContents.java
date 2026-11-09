package com.tutuheleninha.wilderness.block;

import net.minecraft.util.StringRepresentable;

public enum PotContents implements StringRepresentable {
	EMPTY("empty"),
	WATER("water"),
	STEW("stew");

	private final String name;

	PotContents(String name) {
		this.name = name;
	}

	@Override
	public String getSerializedName() {
		return this.name;
	}
}
