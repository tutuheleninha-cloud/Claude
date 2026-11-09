"""
Biomes, world generation, mobs, structures and the other data-driven parts of the update.
Called by gen_assets.py, which provides the shared helpers through `g`.
"""
import copy
import json
import os

G = {}


def h(name):
    return G[name]


# ----------------------------------------------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------------------------------------------

def data_write(rel, obj, ns="wilderness"):
    base = os.path.join(h("RES"), "data", ns)
    h("write")(os.path.join(base, rel), obj)


def feature(name, obj):
    data_write(f"worldgen/feature/{name}.json", obj)


def placed(name, feat, placement):
    data_write(f"worldgen/placed_feature/{name}.json", {"feature": feat, "placement": placement})


def biome(name, obj):
    data_write(f"worldgen/biome/{name}.json", obj)


def trapezoid(r):
    return {"type": "minecraft:trapezoid", "max": r, "min": -r, "plateau": 0}


def spread(xz=7, y=3):
    return {"type": "minecraft:offset", "x": trapezoid(xz), "y": trapezoid(y), "z": trapezoid(xz)}


def survives(state):
    return {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:would_survive", "state": state}}


AIR = {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:matching_block_tag", "tag": "minecraft:air"}}


def leaf_litter_decorators():
    """Same leaf litter carpet the vanilla poplars drop around themselves."""
    entries = [{"data": "minecraft:leaf_litter", "weight": 1}]
    for amount in ("1", "2", "3"):
        for facing in ("north", "east", "south", "west"):
            if amount == "1" and facing == "north":
                continue
            entries.append({"data": {"id": "minecraft:leaf_litter", "properties": {"facing": facing, "segment_amount": amount}}, "weight": 1})
    deco = {"type": "minecraft:place_on_ground", "block_state_provider": {"type": "minecraft:weighted", "entries": entries},
            "height": 2, "radius": 5, "tries": 128}
    return [deco]


def poplar(color, giant):
    """Poplar tree definitions in the vanilla format. Giant ones are taller and wider with more shelf mushrooms."""
    if giant:
        trunk = {"type": "minecraft:poplar_trunk_placer", "base_height": 12, "branch_amount": {"type": "minecraft:uniform", "max_inclusive": 4, "min_inclusive": 2},
                 "height_rand_a": 6, "height_rand_b": 0, "trunk_height_above_branches": 5}
        foliage = {"type": "minecraft:poplar_foliage_placer", "height": {"type": "minecraft:uniform", "max_inclusive": 9, "min_inclusive": 7}, "offset": 0,
                   "radius": {"type": "minecraft:weighted_list", "distribution": [{"data": 7, "weight": 4}, {"data": 8, "weight": 4}, {"data": 9, "weight": 2}]},
                   "side_hole_chance": 0.2}
        decorators = [{"type": "minecraft:shelf_mushroom", "probability": 0.7}] + leaf_litter_decorators()
    else:
        raise ValueError
    return {
        "type": "minecraft:tree",
        "below_trunk_provider": "minecraft:soil_beneath_tree",
        "decorators": decorators,
        "foliage_placer": foliage,
        "foliage_provider": {"id": f"minecraft:{color}_poplar_leaves", "properties": {"distance": "7", "persistent": "false", "waterlogged": "false"}},
        "ignore_vines": True,
        "minimum_size": {"type": "minecraft:two_layers_feature_size", "upper_size": 2},
        "trunk_placer": trunk,
        "trunk_provider": {"id": "minecraft:poplar_log", "properties": {"axis": "y"}},
    }


def fallen_hollow(wood, length, decorators):
    return {
        "type": "minecraft:fallen_tree",
        "log_decorators": decorators,
        "log_length": {"type": "minecraft:uniform", "max_inclusive": length[1], "min_inclusive": length[0]},
        "stump_decorators": [],
        "trunk_provider": {"id": f"wilderness:hollow_{wood}_log", "properties": {"axis": "y", "waterlogged": "false"}},
    }


MUSHROOMS_ON_LOGS = {"type": "minecraft:attached_to_logs", "block_provider": {"type": "minecraft:weighted", "entries": [
    {"data": "minecraft:red_mushroom", "weight": 2}, {"data": "minecraft:brown_mushroom", "weight": 1}]}, "directions": ["up"], "probability": 0.1}


# ----------------------------------------------------------------------------------------------------------------
# World generation
# ----------------------------------------------------------------------------------------------------------------

def gen_worldgen():
    # Giant poplars for the old growth forest
    for color in ("red", "orange", "yellow"):
        feature(f"giant_{color}_poplar", poplar(color, giant=True))
        placed(f"giant_{color}_poplar", f"wilderness:giant_{color}_poplar", [survives("minecraft:poplar_sapling")])

    # Fallen hollow logs, for the new forest and as a rare sight in vanilla forests
    feature("fallen_hollow_poplar_tree", fallen_hollow("poplar", (5, 8), [
        {"type": "minecraft:attached_to_logs", "block_provider": {"id": "minecraft:brown_mushroom"}, "directions": ["up"], "probability": 0.1},
        {"type": "minecraft:shelf_mushroom", "probability": 0.8}]))
    feature("fallen_hollow_oak_tree", fallen_hollow("oak", (4, 7), [MUSHROOMS_ON_LOGS]))
    feature("fallen_hollow_birch_tree", fallen_hollow("birch", (5, 8), [MUSHROOMS_ON_LOGS]))
    feature("fallen_hollow_spruce_tree", fallen_hollow("spruce", (6, 10), [MUSHROOMS_ON_LOGS]))
    for wood in ("poplar", "oak", "birch", "spruce"):
        sapling = f"minecraft:{wood}_sapling"
        placed(f"fallen_hollow_{wood}_tree_checked", f"wilderness:fallen_hollow_{wood}_tree", [survives(sapling)])
        placed(f"fallen_hollow_{wood}_tree", f"wilderness:fallen_hollow_{wood}_tree", [
            {"type": "minecraft:rarity_filter", "chance": 7}, {"type": "minecraft:in_square"},
            {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
            {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"}, {"type": "minecraft:biome"}, survives(sapling)])

    # Old Growth Dappled Forest trees: mostly giant poplars, with normal poplars, spruce and fallen logs between them
    feature("trees_old_growth_dappled_forest", {"type": "minecraft:weighted_random_selector", "features": [
        {"data": "wilderness:giant_red_poplar", "weight": 110},
        {"data": "wilderness:giant_orange_poplar", "weight": 130},
        {"data": "wilderness:giant_yellow_poplar", "weight": 50},
        {"data": "minecraft:red_poplar_leaf_litter", "weight": 60},
        {"data": "minecraft:orange_poplar_leaf_litter", "weight": 70},
        {"data": "minecraft:spruce_checked", "weight": 30},
        {"data": "minecraft:fallen_poplar_tree", "weight": 40},
        {"data": "wilderness:fallen_hollow_poplar_tree_checked", "weight": 80},
    ]})
    placed("trees_old_growth_dappled_forest", "wilderness:trees_old_growth_dappled_forest", [
        {"type": "minecraft:count", "count": 7}, {"type": "minecraft:in_square"},
        {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"}, {"type": "minecraft:biome"}])

    # Flowers
    feature("aster", {"type": "minecraft:simple_block", "to_place": {"id": "wilderness:aster"}})
    feature("goldenrod", {"type": "minecraft:simple_block", "to_place": {"id": "wilderness:goldenrod", "properties": {"half": "lower"}}})
    placed("patch_aster", "wilderness:aster", [
        {"type": "minecraft:rarity_filter", "chance": 2}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"},
        {"type": "minecraft:count", "count": 24}, spread(7, 3), AIR])
    placed("patch_goldenrod", "wilderness:goldenrod", [
        {"type": "minecraft:rarity_filter", "chance": 3}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"},
        {"type": "minecraft:count", "count": 16}, spread(6, 3), AIR])

    # Bog
    feature("cattail", {"type": "minecraft:simple_block", "to_place": {"id": "wilderness:cattail", "properties": {"half": "lower", "waterlogged": "false"}}})
    placed("patch_cattail", "wilderness:cattail", [
        {"type": "minecraft:count", "count": 2}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR_WG"}, {"type": "minecraft:biome"},
        {"type": "minecraft:count", "count": 24}, spread(6, 2),
        {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:any_of", "predicates": [
            {"type": "minecraft:matching_block_tag", "tag": "minecraft:air"},
            {"type": "minecraft:matching_fluids", "fluids": "minecraft:water"}]}}])
    feature("cranberry_bush", {"type": "minecraft:simple_block", "to_place": {"id": "wilderness:cranberry_bush", "properties": {"age": "3"}}})
    placed("patch_cranberry_bush", "wilderness:cranberry_bush", [
        {"type": "minecraft:rarity_filter", "chance": 2}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"},
        {"type": "minecraft:count", "count": 20}, spread(6, 2), AIR])
    feature("disk_peat", {"type": "minecraft:disk", "half_height": 2,
                          "radius": {"type": "minecraft:uniform", "max_inclusive": 5, "min_inclusive": 2},
                          "state_provider": {"id": "wilderness:peat"},
                          "target": {"type": "minecraft:matching_blocks", "blocks": ["minecraft:dirt", "minecraft:grass_block", "minecraft:mud", "minecraft:clay"]}})
    placed("disk_peat", "wilderness:disk_peat", [
        {"type": "minecraft:count", "count": 3}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR_WG"}, {"type": "minecraft:biome"}])
    feature("bog_pool", {"type": "minecraft:waterlogged_vegetation_patch", "depth": 1, "extra_bottom_block_chance": 0.5,
                         "extra_edge_column_chance": 0.4, "ground_state": {"id": "wilderness:peat"},
                         "replaceable": "#wilderness:bog_pool_replaceable", "surface": "floor", "vegetation_chance": 0.25,
                         "vegetation_feature": {"feature": "wilderness:cattail", "placement": []}, "vertical_range": 4,
                         "xz_radius": {"type": "minecraft:uniform", "max_inclusive": 5, "min_inclusive": 2}})
    placed("bog_pool", "wilderness:bog_pool", [
        {"type": "minecraft:count", "count": 4}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}])
    h("tag")("block", "wilderness:bog_pool_replaceable", "minecraft:grass_block", "minecraft:dirt", "minecraft:mud",
             "minecraft:coarse_dirt", "minecraft:podzol", "minecraft:clay", "wilderness:peat", "#minecraft:replaceable_by_trees")
    feature("bog_spruce", {
        "type": "minecraft:tree", "below_trunk_provider": "minecraft:soil_beneath_tree", "decorators": [],
        "foliage_placer": {"type": "minecraft:pine_foliage_placer", "height": {"type": "minecraft:uniform", "max_inclusive": 3, "min_inclusive": 2}, "offset": 1, "radius": 1},
        "foliage_provider": {"id": "minecraft:spruce_leaves", "properties": {"distance": "7", "persistent": "false", "waterlogged": "false"}},
        "ignore_vines": True, "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1, "upper_size": 1},
        "trunk_placer": {"type": "minecraft:straight_trunk_placer", "base_height": 3, "height_rand_a": 2, "height_rand_b": 0},
        "trunk_provider": {"id": "minecraft:spruce_log", "properties": {"axis": "y"}}})
    placed("bog_spruce_checked", "wilderness:bog_spruce", [survives("minecraft:spruce_sapling")])
    feature("trees_bog", {"type": "minecraft:weighted_random_selector", "features": [
        {"data": "wilderness:bog_spruce_checked", "weight": 6},
        {"data": "minecraft:spruce_checked", "weight": 1},
        {"data": "minecraft:yellow_poplar_leaf_litter", "weight": 1},
        {"data": "wilderness:fallen_hollow_spruce_tree_checked", "weight": 1},
    ]})
    placed("trees_bog", "wilderness:trees_bog", [
        {"type": "minecraft:count", "count": {"type": "minecraft:weighted_list", "distribution": [{"data": 1, "weight": 6}, {"data": 2, "weight": 3}, {"data": 3, "weight": 1}]}},
        {"type": "minecraft:in_square"}, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 1},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"}, {"type": "minecraft:biome"}])

    gen_biomes()


SPAWNS_COMMON_MONSTERS = [
    {"type": "minecraft:spider", "count": 4, "weight": 100},
    {"type": "minecraft:zombie", "count": 4, "weight": 95},
    {"type": "minecraft:zombie_villager", "count": 1, "weight": 5},
    {"type": "minecraft:skeleton", "count": 4, "weight": 100},
    {"type": "minecraft:creeper", "count": 4, "weight": 100},
    {"type": "minecraft:slime", "count": 4, "weight": 100},
    {"type": "minecraft:enderman", "count": {"type": "minecraft:uniform", "max_inclusive": 4, "min_inclusive": 1}, "weight": 10},
    {"type": "minecraft:witch", "count": 1, "weight": 5},
]


def uniform(lo, hi):
    return {"type": "minecraft:uniform", "max_inclusive": hi, "min_inclusive": lo}


def spawns(creature, monster=None, ambient=True, water_ambient=False):
    by_cat = {
        "creature": creature,
        "monster": monster or SPAWNS_COMMON_MONSTERS,
        "underground_water_creature": [{"type": "minecraft:glow_squid", "count": uniform(4, 6), "weight": 10}],
    }
    if ambient:
        by_cat["ambient"] = [{"type": "minecraft:bat", "count": 8, "weight": 10}]
    return {"argument": {"spawn_costs": {}, "spawns_by_category": by_cat}, "modifier": "overlay"}


ORES = ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
        "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper", "minecraft:ore_andesite_lower",
        "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower", "minecraft:ore_iron_upper", "minecraft:ore_iron_middle",
        "minecraft:ore_iron_small", "minecraft:ore_gold", "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower",
        "minecraft:ore_diamond", "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
        "minecraft:ore_lapis", "minecraft:ore_lapis_buried", "minecraft:ore_copper", "minecraft:underwater_magma"]


def gen_biomes():
    extra_creatures = G.setdefault("EXTRA_SPAWNS", {})

    old_growth = {
        "attributes": {
            "minecraft:audio/background_music": {"default": {"max_delay": 24000, "min_delay": 12000, "sound": "minecraft:music.overworld.forest"}},
            "minecraft:gameplay/natural_mob_spawns": spawns([
                {"type": "minecraft:sheep", "count": 4, "weight": 10},
                {"type": "minecraft:pig", "count": 4, "weight": 8},
                {"type": "minecraft:chicken", "count": 4, "weight": 8},
                {"type": "minecraft:cow", "count": 4, "weight": 6},
                {"type": "minecraft:rabbit", "count": uniform(2, 4), "weight": 4},
                {"type": "minecraft:fox", "count": uniform(2, 4), "weight": 6},
                {"type": "minecraft:wolf", "count": uniform(2, 4), "weight": 5},
            ] + extra_creatures.get("old_growth_dappled_forest", [])),
            "minecraft:visual/fog_color": "#c8d4de",
            "minecraft:visual/sky_color": "#7ca3ff",
            "minecraft:visual/water_fog_color": "#375154",
        },
        "carvers": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"],
        "downfall": 0.7,
        "effects": {"dry_foliage_color": "#7a3104", "foliage_color": "#d8782a", "grass_color": "#c95e24", "water_color": "#375154"},
        "features": [
            [],
            ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
            ["minecraft:amethyst_geode", "minecraft:forest_rock"],
            ["minecraft:monster_room", "minecraft:monster_room_deep"],
            [],
            [],
            ORES + ["minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"],
            [],
            ["minecraft:spring_water", "minecraft:spring_lava"],
            ["minecraft:glow_lichen", "wilderness:trees_old_growth_dappled_forest", "minecraft:brown_mushroom_dappled_forest",
             "minecraft:patch_red_shrub", "minecraft:patch_grass_forest", "wilderness:patch_aster", "wilderness:patch_goldenrod"],
            ["minecraft:freeze_top_layer"],
        ],
        "has_precipitation": True,
        "temperature": 0.6,
    }
    biome("old_growth_dappled_forest", old_growth)

    bog = {
        "attributes": {
            "minecraft:audio/background_music": {"default": {"max_delay": 24000, "min_delay": 12000, "sound": "minecraft:music.overworld.swamp"}},
            "minecraft:gameplay/increased_fire_burnout": True,
            "minecraft:gameplay/natural_mob_spawns": spawns([
                {"type": "minecraft:sheep", "count": 4, "weight": 8},
                {"type": "minecraft:cow", "count": 4, "weight": 6},
                {"type": "minecraft:rabbit", "count": uniform(2, 3), "weight": 4},
                {"type": "minecraft:frog", "count": uniform(2, 5), "weight": 12},
                {"type": "minecraft:fox", "count": uniform(1, 2), "weight": 3},
            ] + extra_creatures.get("bog", []), monster=SPAWNS_COMMON_MONSTERS[:-2] + [
                {"type": "minecraft:enderman", "count": uniform(1, 4), "weight": 10},
                {"type": "minecraft:witch", "count": 1, "weight": 5},
                {"type": "minecraft:bogged", "count": 4, "weight": 30}]),
            "minecraft:visual/fog_color": "#b9c6c9",
            "minecraft:visual/sky_color": "#7aa3d8",
            "minecraft:visual/water_fog_color": "#2a2416",
            "minecraft:visual/water_fog_end_distance": {"argument": 0.8, "modifier": "multiply"},
        },
        "carvers": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"],
        "downfall": 0.9,
        "effects": {"dry_foliage_color": "#6e4b2a", "foliage_color": "#7b8a3a", "grass_color": "#8f8a46", "water_color": "#5a5a32"},
        "features": [
            [],
            ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
            ["minecraft:amethyst_geode", "wilderness:bog_pool"],
            ["minecraft:fossil_upper", "minecraft:fossil_lower", "minecraft:monster_room", "minecraft:monster_room_deep"],
            [],
            [],
            ORES + ["minecraft:disk_clay", "wilderness:disk_peat"],
            [],
            ["minecraft:spring_water", "minecraft:spring_lava"],
            ["minecraft:glow_lichen", "wilderness:trees_bog", "minecraft:flower_swamp", "minecraft:patch_grass_normal",
             "minecraft:patch_dead_bush", "minecraft:patch_waterlily", "minecraft:brown_mushroom_swamp", "minecraft:red_mushroom_swamp",
             "minecraft:brown_mushroom_normal", "minecraft:red_mushroom_normal", "minecraft:patch_sugar_cane_swamp", "minecraft:patch_pumpkin",
             "minecraft:patch_firefly_bush_swamp", "minecraft:patch_firefly_bush_near_water_swamp", "minecraft:seagrass_swamp",
             "wilderness:patch_cattail", "wilderness:patch_cranberry_bush"],
            ["minecraft:freeze_top_layer"],
        ],
        "has_precipitation": True,
        "temperature": 0.4,
    }
    biome("bog", bog)

    tag = h("tag")
    for b in ("wilderness:old_growth_dappled_forest", "wilderness:bog"):
        tag("worldgen/biome", "minecraft:is_overworld", b)
        tag("worldgen/biome", "minecraft:has_structure/trial_chambers", b)
        tag("worldgen/biome", "minecraft:spawns_cold_variant_farm_animals", b)
    tag("worldgen/biome", "minecraft:is_forest", "wilderness:old_growth_dappled_forest")
    tag("worldgen/biome", "minecraft:has_structure/abandoned_camp_dappled_forest", "wilderness:old_growth_dappled_forest")
    for t in ("has_structure/abandoned_camp_swamp", "has_structure/mineshaft", "has_structure/ruined_portal_swamp",
              "water_on_map_outlines", "spawns_cold_variant_frogs"):
        tag("worldgen/biome", f"minecraft:{t}", "wilderness:bog")

    lang = h("lang")
    lang("biome.wilderness.old_growth_dappled_forest", "Old Growth Dappled Forest", "Floresta salpicada antiga")
    lang("biome.wilderness.bog", "Bog", "Turfeira")


def generate(g):
    G.update(g)
    data_write("banner_pattern/antlers.json", {"asset_id": "wilderness:antlers", "translation_key": "block.wilderness.banner.antlers"})
    h("tag")("banner_pattern", "wilderness:pattern_item/antlers", "wilderness:antlers")
    colors = [("white", "White", "Branca"), ("orange", "Orange", "Laranja"), ("magenta", "Magenta", "Magenta"),
              ("light_blue", "Light Blue", "Azul-Clara"), ("yellow", "Yellow", "Amarela"), ("lime", "Lime", "Verde-Limão"),
              ("pink", "Pink", "Rosa"), ("gray", "Gray", "Cinza"), ("light_gray", "Light Gray", "Cinza-Clara"),
              ("cyan", "Cyan", "Ciano"), ("purple", "Purple", "Roxa"), ("blue", "Blue", "Azul"), ("brown", "Brown", "Marrom"),
              ("green", "Green", "Verde"), ("red", "Red", "Vermelha"), ("black", "Black", "Preta")]
    for c, en, pt in colors:
        h("lang")(f"block.wilderness.banner.antlers.{c}", f"{en} Antlers", f"Galhada {pt}")

    gen_worldgen()
