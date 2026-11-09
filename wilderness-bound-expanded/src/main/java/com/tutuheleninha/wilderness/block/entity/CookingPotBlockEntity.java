package com.tutuheleninha.wilderness.block.entity;

import java.util.Optional;

import com.tutuheleninha.wilderness.block.CookingPotBlock;
import com.tutuheleninha.wilderness.block.PotContents;
import com.tutuheleninha.wilderness.recipe.CookingPotRecipes;
import com.tutuheleninha.wilderness.registry.ModBlockEntities;

import net.minecraft.core.BlockPos;
import net.minecraft.core.NonNullList;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.Containers;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;

public class CookingPotBlockEntity extends BlockEntity {
	public static final int MAX_INGREDIENTS = 4;
	/** Ticks a pot needs over a fire to finish cooking. */
	public static final int COOK_TIME = 200;

	private final NonNullList<ItemStack> ingredients = NonNullList.withSize(MAX_INGREDIENTS, ItemStack.EMPTY);
	private ItemStack result = ItemStack.EMPTY;
	private int cookingProgress;

	public CookingPotBlockEntity(BlockPos pos, BlockState state) {
		super(ModBlockEntities.COOKING_POT, pos, state);
	}

	public static void serverTick(Level level, BlockPos pos, BlockState state, CookingPotBlockEntity pot) {
		if (state.getValue(CookingPotBlock.CONTENTS) != PotContents.WATER || pot.ingredientCount() == 0
				|| !CookingPotBlock.isHeated(level, pos)) {
			pot.resetProgress();
			return;
		}

		Optional<CookingPotRecipes.Recipe> recipe = CookingPotRecipes.find(pot.ingredients);

		if (recipe.isEmpty()) {
			pot.resetProgress();
			return;
		}

		pot.cookingProgress++;

		if (pot.cookingProgress >= COOK_TIME) {
			pot.result = recipe.get().createResult();

			for (int i = 0; i < MAX_INGREDIENTS; i++) {
				pot.ingredients.set(i, ItemStack.EMPTY);
			}

			pot.cookingProgress = 0;
			level.setBlock(pos, state
					.setValue(CookingPotBlock.CONTENTS, PotContents.STEW)
					.setValue(CookingPotBlock.SERVINGS, recipe.get().servings()), Block.UPDATE_ALL);
			level.playSound(null, pos, SoundEvents.BREWING_STAND_BREW, SoundSource.BLOCKS, 0.7F, 0.9F);
		}

		pot.setChanged();
	}

	private void resetProgress() {
		if (this.cookingProgress != 0) {
			this.cookingProgress = 0;
			this.setChanged();
		}
	}

	public int ingredientCount() {
		int count = 0;

		for (ItemStack stack : this.ingredients) {
			if (!stack.isEmpty()) {
				count++;
			}
		}

		return count;
	}

	public boolean canAddIngredient() {
		return this.ingredientCount() < MAX_INGREDIENTS;
	}

	public void addIngredient(ItemStack stack) {
		for (int i = 0; i < MAX_INGREDIENTS; i++) {
			if (this.ingredients.get(i).isEmpty()) {
				this.ingredients.set(i, stack);
				this.cookingProgress = 0;
				this.setChanged();
				return;
			}
		}
	}

	public ItemStack removeLastIngredient() {
		for (int i = MAX_INGREDIENTS - 1; i >= 0; i--) {
			ItemStack stack = this.ingredients.get(i);

			if (!stack.isEmpty()) {
				this.ingredients.set(i, ItemStack.EMPTY);
				this.cookingProgress = 0;
				this.setChanged();
				return stack;
			}
		}

		return ItemStack.EMPTY;
	}

	/** One bowl of whatever is cooked in the pot. */
	public ItemStack takeServing() {
		this.setChanged();
		return this.result.isEmpty() ? ItemStack.EMPTY : this.result.copyWithCount(1);
	}

	public void clearResult() {
		this.result = ItemStack.EMPTY;
		this.setChanged();
	}

	@Override
	protected void saveAdditional(ValueOutput output) {
		super.saveAdditional(output);
		ContainerHelper.saveAllItems(output, this.ingredients);

		if (!this.result.isEmpty()) {
			output.store("result", ItemStack.CODEC, this.result);
		}

		output.putInt("cooking_progress", this.cookingProgress);
	}

	@Override
	protected void loadAdditional(ValueInput input) {
		super.loadAdditional(input);

		for (int i = 0; i < MAX_INGREDIENTS; i++) {
			this.ingredients.set(i, ItemStack.EMPTY);
		}

		ContainerHelper.loadAllItems(input, this.ingredients);
		this.result = input.read("result", ItemStack.CODEC).orElse(ItemStack.EMPTY);
		this.cookingProgress = input.getIntOr("cooking_progress", 0);
	}

	@Override
	public void preRemoveSideEffects(BlockPos pos, BlockState state) {
		if (this.level != null) {
			Containers.dropContents(this.level, pos, this.ingredients);
		}
	}
}
