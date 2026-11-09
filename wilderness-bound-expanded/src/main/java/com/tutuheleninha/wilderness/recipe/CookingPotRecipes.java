package com.tutuheleninha.wilderness.recipe;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.function.Supplier;

import com.tutuheleninha.wilderness.registry.ModItems;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * The cooking pot's recipes. Ingredients are unordered; every ingredient in the pot must be used, and each
 * recipe slot takes exactly one item.
 */
public final class CookingPotRecipes {
	public record Recipe(String name, List<Set<Item>> slots, Supplier<Item> result, int servings) {
		public ItemStack createResult() {
			return new ItemStack(this.result.get());
		}
	}

	private static List<Recipe> recipes;

	private CookingPotRecipes() {
	}

	public static List<Recipe> all() {
		if (recipes == null) {
			recipes = build();
		}

		return recipes;
	}

	private static List<Recipe> build() {
		Set<Item> meat = Set.of(Items.BEEF, Items.COOKED_BEEF, Items.MUTTON, Items.COOKED_MUTTON, Items.PORKCHOP,
				Items.COOKED_PORKCHOP, Items.CHICKEN, Items.COOKED_CHICKEN);
		Set<Item> rabbit = Set.of(Items.RABBIT, Items.COOKED_RABBIT);
		Set<Item> mushroom = Set.of(Items.BROWN_MUSHROOM, Items.RED_MUSHROOM, Items.SHELF_MUSHROOM);
		Set<Item> potato = Set.of(Items.POTATO, Items.BAKED_POTATO);
		Set<Item> carrot = Set.of(Items.CARROT);
		Set<Item> beetroot = Set.of(Items.BEETROOT);
		Set<Item> berries = Set.of(Items.SWEET_BERRIES, Items.GLOW_BERRIES);

		List<Recipe> list = new ArrayList<>();
		list.add(new Recipe("forest_stew", List.of(Set.of(Items.SHELF_MUSHROOM), mushroom, carrot, potato), () -> ModItems.FOREST_STEW, 3));
		list.add(new Recipe("hearty_stew", List.of(meat, potato, carrot, beetroot), () -> ModItems.HEARTY_STEW, 3));
		list.add(new Recipe("pumpkin_soup", List.of(Set.of(Items.PUMPKIN), potato, carrot), () -> ModItems.PUMPKIN_SOUP, 3));
		list.add(new Recipe("berry_compote", List.of(Set.of(ModItems.CRANBERRIES), berries, Set.of(Items.SUGAR)), () -> ModItems.BERRY_COMPOTE, 3));
		list.add(new Recipe("rabbit_stew", List.of(rabbit, carrot, potato, mushroom), () -> Items.RABBIT_STEW, 3));
		list.add(new Recipe("mushroom_stew", List.of(Set.of(Items.BROWN_MUSHROOM), Set.of(Items.RED_MUSHROOM)), () -> Items.MUSHROOM_STEW, 3));
		list.add(new Recipe("beetroot_soup", List.of(beetroot, beetroot, beetroot, beetroot), () -> Items.BEETROOT_SOUP, 3));
		return List.copyOf(list);
	}

	public static boolean isIngredient(ItemStack stack) {
		if (stack.isEmpty()) {
			return false;
		}

		for (Recipe recipe : all()) {
			for (Set<Item> slot : recipe.slots()) {
				if (slot.contains(stack.getItem())) {
					return true;
				}
			}
		}

		return false;
	}

	public static Optional<Recipe> find(List<ItemStack> contents) {
		List<Item> items = new ArrayList<>();

		for (ItemStack stack : contents) {
			if (!stack.isEmpty()) {
				items.add(stack.getItem());
			}
		}

		for (Recipe recipe : all()) {
			if (recipe.slots().size() == items.size() && matches(recipe.slots(), items, 0, new boolean[items.size()])) {
				return Optional.of(recipe);
			}
		}

		return Optional.empty();
	}

	/** Backtracking match of recipe slots to items, so that every item fills exactly one slot. */
	private static boolean matches(List<Set<Item>> slots, List<Item> items, int slot, boolean[] used) {
		if (slot == slots.size()) {
			return true;
		}

		for (int i = 0; i < items.size(); i++) {
			if (!used[i] && slots.get(slot).contains(items.get(i))) {
				used[i] = true;

				if (matches(slots, items, slot + 1, used)) {
					return true;
				}

				used[i] = false;
			}
		}

		return false;
	}
}
