#!/usr/bin/env python3
"""
Generates the JSON assets and data of Wilderness Bound Expanded.

Run from anywhere:  python3 tools/gen_assets.py

Everything written here is derived from the tables below, so names always match the Java registry
(see registry/ModBlocks.java and registry/ModItems.java). Textures, sounds and structure files are made by
the other scripts in this folder and are never touched by this one.
"""
import json
import os
import shutil

NS = "wilderness"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", NS)
DATA_NS = os.path.join(RES, "data", NS)
DATA_MC = os.path.join(RES, "data", "minecraft")

# Folders that only contain generated files and are wiped before every run.
GENERATED = [
    os.path.join(ASSETS, "blockstates"),
    os.path.join(ASSETS, "models"),
    os.path.join(ASSETS, "items"),
    os.path.join(ASSETS, "lang"),
    os.path.join(DATA_NS, "loot_table"),
    os.path.join(DATA_NS, "recipe"),
    os.path.join(DATA_NS, "tags"),
    os.path.join(DATA_NS, "context_int_provider"),
    os.path.join(DATA_MC, "tags"),
]

EN = {}
PT = {}
TAGS = {}  # (registry folder, namespace, path) -> list of entries


def rl(path, ns=NS):
    return path if ":" in path else f"{ns}:{path}"


def mc(path):
    return f"minecraft:{path}"


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def lang(key, en, pt):
    EN[key] = en
    PT[key] = pt


def tag(registry, tag_id, *entries):
    ns, path = tag_id.split(":")
    TAGS.setdefault((registry, ns, path), [])
    for e in entries:
        if e not in TAGS[(registry, ns, path)]:
            TAGS[(registry, ns, path)].append(e)


def block_and_item_tag(tag_id, *entries):
    tag("block", tag_id, *entries)
    tag("item", tag_id, *entries)


# --------------------------------------------------------------------------------------------------------------
# Writers
# --------------------------------------------------------------------------------------------------------------

def blockstate(name, obj):
    write(os.path.join(ASSETS, "blockstates", f"{name}.json"), obj)


def block_model(name, obj):
    write(os.path.join(ASSETS, "models", "block", f"{name}.json"), obj)


def item_model(name, obj):
    write(os.path.join(ASSETS, "models", "item", f"{name}.json"), obj)


def item_def(name, model):
    """assets/<ns>/items/<name>.json pointing at a model."""
    write(os.path.join(ASSETS, "items", f"{name}.json"), {"model": {"type": "minecraft:model", "model": model}})


def generated_item(name, *layers):
    item_model(name, {"parent": "minecraft:item/generated", "textures": {f"layer{i}": l for i, l in enumerate(layers)}})
    item_def(name, rl(f"item/{name}"))


def block_item(name, model=None):
    item_def(name, model or rl(f"block/{name}"))


def loot(path, obj):
    write(os.path.join(DATA_NS, "loot_table", f"{path}.json"), obj)


def recipe(name, obj):
    write(os.path.join(DATA_NS, "recipe", f"{name}.json"), obj)


# --------------------------------------------------------------------------------------------------------------
# Common loot tables
# --------------------------------------------------------------------------------------------------------------

def loot_self(name, survives_explosion=True, item=None):
    pool = {"rolls": 1, "entries": [{"type": "minecraft:item", "name": rl(item or name)}]}
    if survives_explosion:
        pool["conditions"] = [{"condition": "minecraft:survives_explosion"}]
    loot(f"blocks/{name}", {"type": "minecraft:block", "pools": [pool], "random_sequence": rl(f"blocks/{name}")})


def loot_slab(name):
    loot(f"blocks/{name}", {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:item",
            "name": rl(name),
            "functions": [
                {"function": "minecraft:set_count", "count": 2, "add": False,
                 "conditions": [{"condition": "minecraft:block_state_property", "block": rl(name),
                                 "properties": {"type": "double"}}]},
                {"function": "minecraft:explosion_decay"},
            ],
        }]}],
        "random_sequence": rl(f"blocks/{name}"),
    })


def loot_double_plant(name):
    loot(f"blocks/{name}", {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1,
            "conditions": [{"condition": "minecraft:survives_explosion"}],
            "entries": [{"type": "minecraft:item", "name": rl(name),
                         "conditions": [{"condition": "minecraft:block_state_property", "block": rl(name),
                                         "properties": {"half": "lower"}}]}],
        }],
        "random_sequence": rl(f"blocks/{name}"),
    })


# --------------------------------------------------------------------------------------------------------------
# Common models
# --------------------------------------------------------------------------------------------------------------

def stairs_set(name, side, top=None, bottom=None):
    top = top or side
    bottom = bottom or side
    tex = {"bottom": bottom, "side": side, "top": top}
    block_model(name, {"parent": "minecraft:block/stairs", "textures": tex})
    block_model(f"{name}_inner", {"parent": "minecraft:block/inner_stairs", "textures": tex})
    block_model(f"{name}_outer", {"parent": "minecraft:block/outer_stairs", "textures": tex})
    variants = {}
    for facing, y in (("east", 0), ("south", 90), ("west", 180), ("north", 270)):
        for half in ("bottom", "top"):
            for shape in ("straight", "inner_left", "inner_right", "outer_left", "outer_right"):
                model = rl(f"block/{name}") if shape == "straight" else rl(f"block/{name}_{shape.split('_')[0]}")
                rot = y
                if half == "bottom":
                    if shape in ("inner_left", "outer_left"):
                        rot = (y + 270) % 360
                else:
                    if shape in ("inner_right", "outer_right"):
                        rot = (y + 90) % 360
                v = {"model": model}
                if half == "top":
                    v["x"] = 180
                if rot:
                    v["y"] = rot
                if rot or half == "top":
                    v["uvlock"] = True
                variants[f"facing={facing},half={half},shape={shape}"] = v
    blockstate(name, {"variants": variants})
    block_item(name)
    loot_self(name)


def slab_set(name, full_model, side, top=None, bottom=None):
    top = top or side
    bottom = bottom or side
    tex = {"bottom": bottom, "side": side, "top": top}
    block_model(name, {"parent": "minecraft:block/slab", "textures": tex})
    block_model(f"{name}_top", {"parent": "minecraft:block/slab_top", "textures": tex})
    blockstate(name, {"variants": {
        "type=bottom": {"model": rl(f"block/{name}")},
        "type=double": {"model": full_model},
        "type=top": {"model": rl(f"block/{name}_top")},
    }})
    block_item(name)
    loot_slab(name)


def wall_set(name, texture):
    block_model(f"{name}_post", {"parent": "minecraft:block/template_wall_post", "textures": {"wall": texture}})
    block_model(f"{name}_side", {"parent": "minecraft:block/template_wall_side", "textures": {"wall": texture}})
    block_model(f"{name}_side_tall", {"parent": "minecraft:block/template_wall_side_tall", "textures": {"wall": texture}})
    block_model(f"{name}_inventory", {"parent": "minecraft:block/wall_inventory", "textures": {"wall": texture}})
    parts = [{"apply": {"model": rl(f"block/{name}_post")}, "when": {"up": "true"}}]
    for height, suffix in (("low", "_side"), ("tall", "_side_tall")):
        for direction, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270)):
            apply = {"model": rl(f"block/{name}{suffix}"), "uvlock": True}
            if y:
                apply["y"] = y
            parts.append({"apply": apply, "when": {direction: height}})
    blockstate(name, {"multipart": parts})
    block_item(name, rl(f"block/{name}_inventory"))
    loot_self(name)


def stairs_recipe(name, ingredient, group=None):
    r = {"type": "minecraft:crafting_shaped", "category": "building", "key": {"#": ingredient},
         "pattern": ["#  ", "## ", "###"], "result": {"count": 4, "id": rl(name)}}
    if group:
        r["group"] = group
    recipe(name, r)


def slab_recipe(name, ingredient, group=None):
    r = {"type": "minecraft:crafting_shaped", "category": "building", "key": {"#": ingredient},
         "pattern": ["###"], "result": {"count": 6, "id": rl(name)}}
    if group:
        r["group"] = group
    recipe(name, r)


def wall_recipe(name, ingredient, group=None):
    r = {"type": "minecraft:crafting_shaped", "category": "misc", "key": {"#": ingredient},
         "pattern": ["###", "###"], "result": {"count": 6, "id": rl(name)}}
    if group:
        r["group"] = group
    recipe(name, r)


def stonecutting(name, ingredient, result, count=1):
    r = {"type": "minecraft:stonecutting", "ingredient": ingredient, "result": {"id": rl(result)}}
    if count != 1:
        r["result"]["count"] = count
    recipe(name, r)


# --------------------------------------------------------------------------------------------------------------
# Wood families: hollow logs, log benches, parquet
# --------------------------------------------------------------------------------------------------------------

WOODS = [
    # id, log name, english name, pt "de X" material for logs, pt material for planks (with article/agreement)
    ("oak", "oak_log", "Oak", "Tronco de Carvalho", "de Carvalho"),
    ("spruce", "spruce_log", "Spruce", "Tronco de Abeto", "de Abeto"),
    ("birch", "birch_log", "Birch", "Tronco de Bétula", "de Bétula"),
    ("jungle", "jungle_log", "Jungle", "Tronco da Selva", "da Selva"),
    ("acacia", "acacia_log", "Acacia", "Tronco de Acácia", "de Acácia"),
    ("dark_oak", "dark_oak_log", "Dark Oak", "Tronco de Carvalho Escuro", "de Carvalho Escuro"),
    ("mangrove", "mangrove_log", "Mangrove", "Tronco de Mangue", "de Mangue"),
    ("cherry", "cherry_log", "Cherry", "Tronco de Cerejeira", "de Cerejeira"),
    ("pale_oak", "pale_oak_log", "Pale Oak", "Tronco de Carvalho Pálido", "de Carvalho Pálido"),
    ("poplar", "poplar_log", "Poplar", "Tronco de Álamo", "de Álamo"),
    ("crimson", "crimson_stem", "Crimson", "Caule Carmesim", "Carmesim"),
    ("warped", "warped_stem", "Warped", "Caule Distorcido", "Distorcido"),
]


def wood_textures(wood, log):
    stem = log.endswith("_stem")
    stripped = f"stripped_{log}"
    return {
        "side": mc(f"block/{log}"),
        "end": mc(f"block/{log}_top"),
        "inside": mc(f"block/{stripped}"),
        "inside_end": mc(f"block/{stripped}_top"),
        "planks": mc(f"block/{wood}_planks"),
        "stem": stem,
    }


def face(texture, cull=None, uv=None, rotation=None):
    f = {"texture": texture}
    if uv is not None:
        f["uv"] = uv
    if cull:
        f["cullface"] = cull
    if rotation:
        f["rotation"] = rotation
    return f


def hollow_log_models(name, tex):
    """Vertical hollow log: four 2px walls around a 12x12 hole. Horizontal variants rotate this model."""
    walls = [
        # from, to, outer face, inner face
        ([0, 0, 0], [16, 16, 2], "north", "south"),
        ([0, 0, 14], [16, 16, 16], "south", "north"),
        ([0, 0, 2], [2, 16, 14], "west", "east"),
        ([14, 0, 2], [16, 16, 14], "east", "west"),
    ]
    elements = []
    for frm, to, outer, inner in walls:
        faces = {
            outer: face("#side", cull=outer),
            inner: face("#inside"),
            "up": face("#end", cull="up"),
            "down": face("#end", cull="down"),
        }
        # The short ends of the north/south walls are part of the outside of the log.
        if outer in ("north", "south"):
            faces["east"] = face("#side", cull="east")
            faces["west"] = face("#side", cull="west")
        elements.append({"from": frm, "to": to, "faces": faces})
    block_model(name, {
        "parent": "minecraft:block/block",
        "textures": {"particle": "#side", "side": tex["side"], "end": tex["end"], "inside": tex["inside"]},
        "elements": elements,
    })


def log_bench_model(name, tex):
    """A half log lying along X, flat (stripped) side up, with a slightly raised seat."""
    block_model(name, {
        "parent": "minecraft:block/block",
        "textures": {"particle": "#side", "side": tex["side"], "end": tex["end"], "top": tex["inside"]},
        "elements": [
            {"from": [0, 0, 3], "to": [16, 7, 13], "faces": {
                "north": face("#side", uv=[0, 4, 16, 11]),
                "south": face("#side", uv=[0, 4, 16, 11]),
                "up": face("#top", uv=[0, 3, 16, 13], rotation=90),
                "down": face("#side", cull="down", uv=[0, 3, 16, 13]),
                "west": face("#end", cull="west", uv=[3, 9, 13, 16]),
                "east": face("#end", cull="east", uv=[3, 9, 13, 16]),
            }},
            {"from": [0, 7, 4], "to": [16, 8, 12], "faces": {
                "up": face("#top", uv=[0, 4, 16, 12], rotation=90),
                "north": face("#side", uv=[0, 3, 16, 4]),
                "south": face("#side", uv=[0, 3, 16, 4]),
                "west": face("#end", cull="west", uv=[4, 8, 12, 9]),
                "east": face("#end", cull="east", uv=[4, 8, 12, 9]),
            }},
        ],
    })


def parquet_elements(y_layers):
    """Octant cubes whose outer faces alternate plank direction, giving a basket-weave look on every side."""
    elements = []
    for j in y_layers:
        for i in (0, 1):
            for k in (0, 1):
                frm = [8 * i, 8 * j, 8 * k]
                to = [8 * i + 8, 8 * j + 8, 8 * k + 8]
                faces = {}
                if j == max(y_layers):
                    faces["up"] = face("#planks", cull="up" if j == 1 else None, rotation=90 if (i + k) % 2 else None)
                if j == min(y_layers):
                    faces["down"] = face("#planks", cull="down" if j == 0 else None, rotation=90 if (i + k) % 2 else None)
                if k == 0:
                    faces["north"] = face("#planks", cull="north", rotation=90 if (i + j) % 2 else None)
                if k == 1:
                    faces["south"] = face("#planks", cull="south", rotation=90 if (i + j) % 2 else None)
                if i == 0:
                    faces["west"] = face("#planks", cull="west", rotation=90 if (k + j) % 2 else None)
                if i == 1:
                    faces["east"] = face("#planks", cull="east", rotation=90 if (k + j) % 2 else None)
                elements.append({"from": frm, "to": to, "faces": faces})
    return elements


def gen_wood_families():
    for wood, log, en_name, pt_log, pt_mat in WOODS:
        tex = wood_textures(wood, log)
        stem = tex["stem"]
        en_log = f"{en_name} Stem" if stem else f"{en_name} Log"

        # Hollow log
        hollow = f"hollow_{log}"
        hollow_log_models(hollow, tex)
        blockstate(hollow, {"variants": {
            "axis=y": {"model": rl(f"block/{hollow}")},
            "axis=z": {"model": rl(f"block/{hollow}"), "x": 90},
            "axis=x": {"model": rl(f"block/{hollow}"), "x": 90, "y": 90},
        }})
        block_item(hollow)
        loot_self(hollow)
        lang(f"block.{NS}.{hollow}", f"Hollow {en_log}", (pt_log + " Oco") if stem else pt_log.replace("Tronco", "Tronco Oco", 1))
        block_and_item_tag(rl("hollow_logs"), rl(hollow))
        tag("block", "minecraft:mineable/axe", rl(hollow))
        if not stem:
            block_and_item_tag("minecraft:logs_that_burn", rl(hollow))
        recipe(f"{wood}_planks_from_{hollow}", {
            "type": "minecraft:crafting_shapeless", "category": "building", "group": "planks",
            "ingredients": [rl(hollow)], "result": {"count": 2, "id": mc(f"{wood}_planks")},
        })

        # Log bench
        bench = f"{log}_bench"
        log_bench_model(bench, tex)
        blockstate(bench, {"variants": {
            "axis=x": {"model": rl(f"block/{bench}")},
            "axis=z": {"model": rl(f"block/{bench}"), "y": 90},
        }})
        block_item(bench)
        loot_self(bench)
        lang(f"block.{NS}.{bench}", f"{en_log} Bench", f"Banco de {pt_log}")
        block_and_item_tag(rl("log_benches"), rl(bench))
        tag("block", "minecraft:mineable/axe", rl(bench))
        stripped = mc(f"stripped_{log}")
        recipe(bench, {
            "type": "minecraft:crafting_shaped", "category": "decorations", "group": "log_bench",
            "key": {"#": stripped, "|": "minecraft:stick"},
            "pattern": ["##", "||"], "result": {"count": 2, "id": rl(bench)},
        })

        # Parquet + parquet slab
        parquet = f"{wood}_parquet"
        pslab = f"{wood}_parquet_slab"
        ptex = {"particle": tex["planks"], "planks": tex["planks"]}
        block_model(parquet, {"parent": "minecraft:block/block", "textures": ptex, "elements": parquet_elements([0, 1])})
        block_model(pslab, {"parent": "minecraft:block/block", "textures": ptex, "elements": parquet_elements([0])})
        block_model(f"{pslab}_top", {"parent": "minecraft:block/block", "textures": ptex, "elements": parquet_elements([1])})
        blockstate(parquet, {"variants": {"": {"model": rl(f"block/{parquet}")}}})
        blockstate(pslab, {"variants": {
            "type=bottom": {"model": rl(f"block/{pslab}")},
            "type=double": {"model": rl(f"block/{parquet}")},
            "type=top": {"model": rl(f"block/{pslab}_top")},
        }})
        block_item(parquet)
        block_item(pslab)
        loot_self(parquet)
        loot_slab(pslab)
        pt_parquet = f"Parquê {pt_mat}" if pt_mat.startswith(("de", "da")) else f"Parquê {pt_mat}"
        lang(f"block.{NS}.{parquet}", f"{en_name} Parquet", pt_parquet)
        lang(f"block.{NS}.{pslab}", f"{en_name} Parquet Slab", f"Laje de {pt_parquet}")
        tag("block", "minecraft:mineable/axe", rl(parquet), rl(pslab))
        block_and_item_tag("minecraft:slabs", rl(pslab))
        block_and_item_tag("minecraft:wooden_slabs", rl(pslab))
        recipe(parquet, {
            "type": "minecraft:crafting_shaped", "category": "building", "group": "parquet",
            "key": {"#": mc(f"{wood}_slab")}, "pattern": ["#", "#"], "result": {"id": rl(parquet)},
        })
        slab_recipe(pslab, rl(parquet), group="parquet_slab")


# --------------------------------------------------------------------------------------------------------------
# Terracotta and concrete
# --------------------------------------------------------------------------------------------------------------

COLORS = [
    ("white", "White", "Branca", "Branco"), ("orange", "Orange", "Laranja", "Laranja"),
    ("magenta", "Magenta", "Magenta", "Magenta"), ("light_blue", "Light Blue", "Azul-Clara", "Azul-Claro"),
    ("yellow", "Yellow", "Amarela", "Amarelo"), ("lime", "Lime", "Verde-Limão", "Verde-Limão"),
    ("pink", "Pink", "Rosa", "Rosa"), ("gray", "Gray", "Cinza", "Cinza"),
    ("light_gray", "Light Gray", "Cinza-Clara", "Cinza-Claro"), ("cyan", "Cyan", "Ciano", "Ciano"),
    ("purple", "Purple", "Roxa", "Roxo"), ("blue", "Blue", "Azul", "Azul"),
    ("brown", "Brown", "Marrom", "Marrom"), ("green", "Green", "Verde", "Verde"),
    ("red", "Red", "Vermelha", "Vermelho"), ("black", "Black", "Preta", "Preto"),
]


def gen_terracotta_and_concrete():
    variants = [("terracotta", "Terracotta", "Terracota")]
    variants += [(f"{c}_terracotta", f"{en} Terracotta", f"Terracota {pt_f}") for c, en, pt_f, _ in COLORS]
    for base, en, pt in variants:
        texture = mc(f"block/{base}")
        stairs, slab, wall = f"{base}_stairs", f"{base}_slab", f"{base}_wall"
        stairs_set(stairs, texture)
        slab_set(slab, mc(f"block/{base}"), texture)
        wall_set(wall, texture)
        lang(f"block.{NS}.{stairs}", f"{en} Stairs", f"Escadas de {pt}")
        lang(f"block.{NS}.{slab}", f"{en} Slab", f"Laje de {pt}")
        lang(f"block.{NS}.{wall}", f"{en} Wall", f"Muro de {pt}")
        stairs_recipe(stairs, mc(base), group="terracotta_stairs")
        slab_recipe(slab, mc(base), group="terracotta_slab")
        wall_recipe(wall, mc(base), group="terracotta_wall")
        stonecutting(f"{stairs}_from_{base}_stonecutting", mc(base), stairs)
        stonecutting(f"{slab}_from_{base}_stonecutting", mc(base), slab, 2)
        stonecutting(f"{wall}_from_{base}_stonecutting", mc(base), wall)
        tag("block", "minecraft:mineable/pickaxe", rl(stairs), rl(slab), rl(wall))
        block_and_item_tag("minecraft:stairs", rl(stairs))
        block_and_item_tag("minecraft:slabs", rl(slab))
        block_and_item_tag("minecraft:walls", rl(wall))
        block_and_item_tag(rl("terracotta_stairs"), rl(stairs))
        block_and_item_tag(rl("terracotta_slabs"), rl(slab))
        block_and_item_tag(rl("terracotta_walls"), rl(wall))

    for c, en, _, pt_m in COLORS:
        base = f"{c}_concrete"
        wall = f"{base}_wall"
        wall_set(wall, mc(f"block/{base}"))
        lang(f"block.{NS}.{wall}", f"{en} Concrete Wall", f"Muro de Concreto {pt_m}")
        wall_recipe(wall, mc(base), group="concrete_wall")
        stonecutting(f"{wall}_from_{base}_stonecutting", mc(base), wall)
        tag("block", "minecraft:mineable/pickaxe", rl(wall))
        block_and_item_tag("minecraft:walls", rl(wall))
        block_and_item_tag(rl("concrete_walls"), rl(wall))


# --------------------------------------------------------------------------------------------------------------
# Thatch and peat
# --------------------------------------------------------------------------------------------------------------

def gen_thatch_and_peat():
    side, top = rl("block/thatch_side"), rl("block/thatch_top")
    block_model("thatch", {"parent": "minecraft:block/cube_column", "textures": {"end": top, "side": side}})
    block_model("thatch_horizontal", {"parent": "minecraft:block/cube_column_horizontal", "textures": {"end": top, "side": side}})
    blockstate("thatch", {"variants": {
        "axis=x": {"model": rl("block/thatch_horizontal"), "x": 90, "y": 90},
        "axis=y": {"model": rl("block/thatch")},
        "axis=z": {"model": rl("block/thatch_horizontal"), "x": 90},
    }})
    block_item("thatch")
    loot_self("thatch")
    stairs_set("thatch_stairs", side, top, top)
    slab_set("thatch_slab", rl("block/thatch"), side, top, top)
    lang(f"block.{NS}.thatch", "Thatch", "Sapê")
    lang(f"block.{NS}.thatch_stairs", "Thatch Stairs", "Escadas de Sapê")
    lang(f"block.{NS}.thatch_slab", "Thatch Slab", "Laje de Sapê")
    recipe("thatch", {"type": "minecraft:crafting_shaped", "category": "building", "group": "thatch",
                      "key": {"#": mc("wheat")}, "pattern": ["##", "##"], "result": {"id": rl("thatch")}})
    recipe("thatch_from_cattail", {"type": "minecraft:crafting_shaped", "category": "building", "group": "thatch",
                                   "key": {"#": rl("cattail")}, "pattern": ["##", "##"], "result": {"count": 2, "id": rl("thatch")}})
    stairs_recipe("thatch_stairs", rl("thatch"))
    slab_recipe("thatch_slab", rl("thatch"))
    tag("block", "minecraft:mineable/hoe", rl("thatch"), rl("thatch_stairs"), rl("thatch_slab"))
    block_and_item_tag("minecraft:stairs", rl("thatch_stairs"))
    block_and_item_tag("minecraft:slabs", rl("thatch_slab"))

    block_model("peat", {"parent": "minecraft:block/cube_all", "textures": {"all": rl("block/peat")}})
    blockstate("peat", {"variants": {"": {"model": rl("block/peat")}}})
    block_item("peat")
    loot_self("peat")
    lang(f"block.{NS}.peat", "Peat", "Turfa")
    tag("block", "minecraft:mineable/shovel", rl("peat"))
    tag("block", "minecraft:dirt", rl("peat"))
    tag("block", "minecraft:supports_vegetation", rl("peat"))
    tag("block", "minecraft:sniffer_diggable_block", rl("peat"))
    # Burn time: 1200 ticks (6 items), between a log and coal.
    write(os.path.join(DATA_NS, "context_int_provider", "cooking", "time_peat.json"), {
        "type": "minecraft:div",
        "left": 1200,
        "right": {
            "type": "minecraft:conditional",
            "condition": "minecraft:block/fast_cooking",
            "on_false": "minecraft:cooking/normal_burn_time_reduction_factor",
            "on_true": "minecraft:cooking/fast_burn_time_reduction_factor",
        },
    })

    bricks = rl("block/peat_bricks")
    block_model("peat_bricks", {"parent": "minecraft:block/cube_all", "textures": {"all": bricks}})
    blockstate("peat_bricks", {"variants": {"": {"model": rl("block/peat_bricks")}}})
    block_item("peat_bricks")
    loot_self("peat_bricks")
    stairs_set("peat_brick_stairs", bricks)
    slab_set("peat_brick_slab", rl("block/peat_bricks"), bricks)
    wall_set("peat_brick_wall", bricks)
    lang(f"block.{NS}.peat_bricks", "Peat Bricks", "Tijolos de Turfa")
    lang(f"block.{NS}.peat_brick_stairs", "Peat Brick Stairs", "Escadas de Tijolos de Turfa")
    lang(f"block.{NS}.peat_brick_slab", "Peat Brick Slab", "Laje de Tijolos de Turfa")
    lang(f"block.{NS}.peat_brick_wall", "Peat Brick Wall", "Muro de Tijolos de Turfa")
    recipe("peat_bricks", {"type": "minecraft:crafting_shaped", "category": "building",
                           "key": {"#": rl("peat")}, "pattern": ["##", "##"], "result": {"count": 4, "id": rl("peat_bricks")}})
    stairs_recipe("peat_brick_stairs", rl("peat_bricks"))
    slab_recipe("peat_brick_slab", rl("peat_bricks"))
    wall_recipe("peat_brick_wall", rl("peat_bricks"))
    for result, count in (("peat_brick_stairs", 1), ("peat_brick_slab", 2), ("peat_brick_wall", 1)):
        stonecutting(f"{result}_from_peat_bricks_stonecutting", rl("peat_bricks"), result, count)
    tag("block", "minecraft:mineable/pickaxe", rl("peat_bricks"), rl("peat_brick_stairs"), rl("peat_brick_slab"), rl("peat_brick_wall"))
    block_and_item_tag("minecraft:stairs", rl("peat_brick_stairs"))
    block_and_item_tag("minecraft:slabs", rl("peat_brick_slab"))
    block_and_item_tag("minecraft:walls", rl("peat_brick_wall"))


# --------------------------------------------------------------------------------------------------------------
# Plants
# --------------------------------------------------------------------------------------------------------------

def cross(name, texture):
    block_model(name, {"parent": "minecraft:block/cross", "textures": {"cross": texture}})


def gen_plants():
    # Cattail: two-block plant, lower half may be waterlogged.
    cross("cattail_bottom", rl("block/cattail_bottom"))
    cross("cattail_top", rl("block/cattail_top"))
    blockstate("cattail", {"variants": {
        "half=lower": {"model": rl("block/cattail_bottom")},
        "half=upper": {"model": rl("block/cattail_top")},
    }})
    generated_item("cattail", rl("item/cattail"))
    loot_double_plant("cattail")
    lang(f"block.{NS}.cattail", "Cattail", "Taboa")

    # Cranberry bush, item is "cranberries" (like sweet berries).
    for age in range(4):
        cross(f"cranberry_bush_stage{age}", rl(f"block/cranberry_bush_stage{age}"))
    blockstate("cranberry_bush", {"variants": {f"age={a}": {"model": rl(f"block/cranberry_bush_stage{a}")} for a in range(4)}})
    generated_item("cranberries", rl("item/cranberries"))
    loot("blocks/cranberry_bush", {
        "type": "minecraft:block",
        "functions": [{"function": "minecraft:explosion_decay"}],
        "pools": [
            {"rolls": 1,
             "conditions": [{"condition": "minecraft:block_state_property", "block": rl("cranberry_bush"), "properties": {"age": "3"}}],
             "entries": [{"type": "minecraft:item", "name": rl("cranberries")}],
             "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 2, "max": 3}},
                           {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune",
                            "formula": "minecraft:uniform_bonus_count", "parameters": {"bonusMultiplier": 1}}]},
            {"rolls": 1,
             "conditions": [{"condition": "minecraft:block_state_property", "block": rl("cranberry_bush"), "properties": {"age": "2"}}],
             "entries": [{"type": "minecraft:item", "name": rl("cranberries")}],
             "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 2}},
                           {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune",
                            "formula": "minecraft:uniform_bonus_count", "parameters": {"bonusMultiplier": 1}}]},
            {"rolls": 1,
             "conditions": [{"condition": "minecraft:block_state_property", "block": rl("cranberry_bush"), "properties": {"age": "0"}}],
             "entries": [{"type": "minecraft:item", "name": rl("cranberries")}]},
            {"rolls": 1,
             "conditions": [{"condition": "minecraft:block_state_property", "block": rl("cranberry_bush"), "properties": {"age": "1"}}],
             "entries": [{"type": "minecraft:item", "name": rl("cranberries")}]},
        ],
        "random_sequence": rl("blocks/cranberry_bush"),
    })
    lang(f"block.{NS}.cranberry_bush", "Cranberry Bush", "Arbusto de Cranberry")
    lang(f"item.{NS}.cranberries", "Cranberries", "Cranberries")
    tag("item", "minecraft:fox_food", rl("cranberries"))

    # Aster + potted aster
    cross("aster", rl("block/aster"))
    blockstate("aster", {"variants": {"": {"model": rl("block/aster")}}})
    generated_item("aster", rl("block/aster"))
    loot_self("aster")
    block_model("potted_aster", {"parent": "minecraft:block/flower_pot_cross", "textures": {"plant": rl("block/aster")}})
    blockstate("potted_aster", {"variants": {"": {"model": rl("block/potted_aster")}}})
    loot("blocks/potted_aster", {
        "type": "minecraft:block",
        "pools": [
            {"rolls": 1, "conditions": [{"condition": "minecraft:survives_explosion"}],
             "entries": [{"type": "minecraft:item", "name": "minecraft:flower_pot"}]},
            {"rolls": 1, "conditions": [{"condition": "minecraft:survives_explosion"}],
             "entries": [{"type": "minecraft:item", "name": rl("aster")}]},
        ],
        "random_sequence": rl("blocks/potted_aster"),
    })
    lang(f"block.{NS}.aster", "Aster", "Áster")
    lang(f"block.{NS}.potted_aster", "Potted Aster", "Áster Envasado")
    recipe("purple_dye_from_aster", {"type": "minecraft:crafting_shapeless", "category": "misc", "group": "purple_dye",
                                     "ingredients": [rl("aster")], "result": {"id": "minecraft:purple_dye"}})
    block_and_item_tag("minecraft:small_flowers", rl("aster"))
    tag("block", "minecraft:flower_pots", rl("potted_aster"))
    tag("item", "minecraft:bee_food", rl("aster"))

    # Goldenrod: tall flower
    cross("goldenrod_bottom", rl("block/goldenrod_bottom"))
    cross("goldenrod_top", rl("block/goldenrod_top"))
    blockstate("goldenrod", {"variants": {
        "half=lower": {"model": rl("block/goldenrod_bottom")},
        "half=upper": {"model": rl("block/goldenrod_top")},
    }})
    generated_item("goldenrod", rl("block/goldenrod_top"))
    loot_double_plant("goldenrod")
    lang(f"block.{NS}.goldenrod", "Goldenrod", "Vara-Dourada")
    recipe("yellow_dye_from_goldenrod", {"type": "minecraft:crafting_shapeless", "category": "misc", "group": "yellow_dye",
                                         "ingredients": [rl("goldenrod")], "result": {"count": 2, "id": "minecraft:yellow_dye"}})
    block_and_item_tag("minecraft:flowers", rl("goldenrod"))
    tag("block", "minecraft:tall_flowers", rl("goldenrod"))
    tag("item", "minecraft:bee_food", rl("goldenrod"))
    tag("block", "minecraft:bee_attractive", rl("aster"), rl("goldenrod"))
    tag("block", "minecraft:replaceable_by_trees", rl("cattail"), rl("goldenrod"), rl("aster"))
    tag("block", "minecraft:sword_efficient", rl("cattail"), rl("goldenrod"), rl("cranberry_bush"))
    tag("block", "minecraft:enchantment_power_transmitter", rl("cattail"), rl("goldenrod"), rl("aster"), rl("cranberry_bush"))


# --------------------------------------------------------------------------------------------------------------
# Camping: cairn, antler chandelier, cooking pot
# --------------------------------------------------------------------------------------------------------------

def stone(frm, to, tex="#stone"):
    return {"from": frm, "to": to, "faces": {d: face(tex) for d in ("north", "south", "east", "west", "up", "down")}}


def gen_camping_blocks():
    # Cairn: 1-4 stacked stones
    sizes = [
        [stone([5, 0, 5], [11, 3, 11], "#base")],
        [stone([4, 0, 4], [12, 3, 12], "#base"), stone([5, 3, 5.5], [11, 6, 10.5])],
        [stone([4, 0, 4], [12, 3, 12], "#base"), stone([5, 3, 5], [11, 6, 11]), stone([6, 6, 6], [10.5, 9, 10])],
        [stone([3, 0, 3], [13, 3, 13], "#base"), stone([4.5, 3, 4.5], [11.5, 6, 11.5]), stone([5.5, 6, 6], [10.5, 9, 10.5]),
         stone([6.5, 9, 6.5], [9.5, 11, 9.5])],
    ]
    for n, elements in enumerate(sizes, start=1):
        block_model(f"cairn_{n}", {
            "parent": "minecraft:block/block",
            "textures": {"particle": "minecraft:block/cobblestone", "base": "minecraft:block/mossy_cobblestone",
                         "stone": "minecraft:block/cobblestone"},
            "elements": elements,
        })
    blockstate("cairn", {"variants": {f"stones={n}": [
        {"model": rl(f"block/cairn_{n}")}, {"model": rl(f"block/cairn_{n}"), "y": 90},
        {"model": rl(f"block/cairn_{n}"), "y": 180}, {"model": rl(f"block/cairn_{n}"), "y": 270},
    ] for n in range(1, 5)}})
    block_item("cairn", rl("block/cairn_3"))
    loot("blocks/cairn", {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:item", "name": rl("cairn"),
            "functions": [
                {"function": "minecraft:set_count", "count": n, "add": False,
                 "conditions": [{"condition": "minecraft:block_state_property", "block": rl("cairn"), "properties": {"stones": str(n)}}]}
                for n in (2, 3, 4)
            ] + [{"function": "minecraft:explosion_decay"}],
        }]}],
        "random_sequence": rl("blocks/cairn"),
    })
    lang(f"block.{NS}.cairn", "Cairn", "Marco de Pedras")
    recipe("cairn", {"type": "minecraft:crafting_shapeless", "category": "decorations",
                     "ingredients": ["#minecraft:stone_crafting_materials"], "result": {"count": 2, "id": rl("cairn")}})
    tag("block", "minecraft:mineable/pickaxe", rl("cairn"))

    # Antler chandelier
    candle = "#candle"
    elements = [
        # chain
        {"from": [7.5, 12, 7.5], "to": [8.5, 16, 8.5], "shade": False, "faces": {
            "north": face("#chain", uv=[6, 0, 9, 16]), "south": face("#chain", uv=[6, 0, 9, 16]),
            "east": face("#chain", uv=[6, 0, 9, 16]), "west": face("#chain", uv=[6, 0, 9, 16])}},
        # central knot of antlers
        {"from": [6, 9, 6], "to": [10, 12, 10], "faces": {d: face("#antler", uv=[0, 0, 4, 3]) for d in ("north", "south", "east", "west", "up", "down")}},
    ]
    # four antler arms with tines
    arms = [([2, 7, 7], [6, 9, 9]), ([10, 7, 7], [14, 9, 9]), ([7, 7, 2], [9, 9, 6]), ([7, 7, 10], [9, 9, 14])]
    for frm, to in arms:
        elements.append({"from": frm, "to": to, "faces": {d: face("#antler", uv=[4, 0, 8, 2]) for d in ("north", "south", "east", "west", "up", "down")}})
    tines = [([2, 9, 7.5], [3, 12, 8.5]), ([13, 9, 7.5], [14, 12, 8.5]), ([7.5, 9, 2], [8.5, 12, 3]), ([7.5, 9, 13], [8.5, 12, 14]),
             ([4.5, 9, 7.5], [5.5, 11, 8.5]), ([10.5, 9, 7.5], [11.5, 11, 8.5])]
    for frm, to in tines:
        elements.append({"from": frm, "to": to, "faces": {d: face("#antler", uv=[8, 0, 9, 3]) for d in ("north", "south", "east", "west", "up")}})
    # candles on the four arm ends
    for cx, cz in ((3.5, 8), (12.5, 8), (8, 3.5), (8, 12.5)):
        elements.append({"from": [cx - 1, 9, cz - 1], "to": [cx + 1, 9 + 0.01 + 3, cz + 1], "faces": {
            "north": face(candle, uv=[0, 8, 2, 11]), "south": face(candle, uv=[0, 8, 2, 11]),
            "east": face(candle, uv=[0, 8, 2, 11]), "west": face(candle, uv=[0, 8, 2, 11]),
            "up": face(candle, uv=[0, 6, 2, 8])}})
        elements.append({"from": [cx - 0.5, 12, cz], "to": [cx + 0.5, 13, cz], "shade": False, "faces": {
            "north": face(candle, uv=[0, 5, 1, 6]), "south": face(candle, uv=[0, 5, 1, 6])}})
        elements.append({"from": [cx, 12, cz - 0.5], "to": [cx, 13, cz + 0.5], "shade": False, "faces": {
            "east": face(candle, uv=[0, 5, 1, 6]), "west": face(candle, uv=[0, 5, 1, 6])}})
    block_model("antler_chandelier", {
        "parent": "minecraft:block/block",
        "ambientocclusion": False,
        "textures": {"particle": rl("block/antler_chandelier"), "antler": rl("block/antler_chandelier"),
                     "candle": "minecraft:block/candle_lit", "chain": "minecraft:block/iron_chain"},
        "elements": elements,
    })
    blockstate("antler_chandelier", {"variants": {"": {"model": rl("block/antler_chandelier")}}})
    block_item("antler_chandelier")
    loot_self("antler_chandelier")
    lang(f"block.{NS}.antler_chandelier", "Antler Chandelier", "Lustre de Galhadas")
    recipe("antler_chandelier", {"type": "minecraft:crafting_shaped", "category": "decorations",
                                 "key": {"A": rl("antler"), "C": "minecraft:candle", "I": "minecraft:iron_chain"},
                                 "pattern": [" I ", "CAC", "A A"], "result": {"id": rl("antler_chandelier")}})
    tag("block", "minecraft:mineable/pickaxe", rl("antler_chandelier"))

    gen_cooking_pot()


def box(frm, to, tex, faces=("north", "south", "east", "west", "up", "down"), **extra):
    e = {"from": frm, "to": to, "faces": {d: face(tex) for d in faces}}
    e.update(extra)
    return e


def gen_cooking_pot():
    tex = {"particle": rl("block/cooking_pot_side"), "side": rl("block/cooking_pot_side"),
           "top": rl("block/cooking_pot_top"), "bottom": rl("block/cooking_pot_bottom"),
           "inner": rl("block/cooking_pot_inner"), "handle": rl("block/cooking_pot_handle")}
    body = [
        # floor
        {"from": [3, 1, 3], "to": [13, 2, 13], "faces": {"up": face("#inner"), "down": face("#bottom")}},
        # walls (outer faces use side texture, inner faces inner texture)
        {"from": [2, 1, 2], "to": [14, 10, 3], "faces": {"north": face("#side"), "south": face("#inner"), "up": face("#top"), "down": face("#bottom"), "east": face("#side"), "west": face("#side")}},
        {"from": [2, 1, 13], "to": [14, 10, 14], "faces": {"south": face("#side"), "north": face("#inner"), "up": face("#top"), "down": face("#bottom"), "east": face("#side"), "west": face("#side")}},
        {"from": [2, 1, 3], "to": [3, 10, 13], "faces": {"west": face("#side"), "east": face("#inner"), "up": face("#top"), "down": face("#bottom")}},
        {"from": [13, 1, 3], "to": [14, 10, 13], "faces": {"east": face("#side"), "west": face("#inner"), "up": face("#top"), "down": face("#bottom")}},
        # little feet
        box([3, 0, 3], [5, 1, 5], "#bottom"), box([11, 0, 3], [13, 1, 5], "#bottom"),
        box([3, 0, 11], [5, 1, 13], "#bottom"), box([11, 0, 11], [13, 1, 13], "#bottom"),
        # handle lugs and bail (handle runs east-west when facing north)
        box([1, 8, 7], [2, 9, 9], "#handle"), box([14, 8, 7], [15, 9, 9], "#handle"),
        box([1, 9, 7.5], [2, 14, 8.5], "#handle"), box([14, 9, 7.5], [15, 14, 8.5], "#handle"),
        box([1, 14, 7.5], [15, 15, 8.5], "#handle"),
    ]
    block_model("cooking_pot", {"parent": "minecraft:block/block", "textures": tex, "elements": body})
    # Hanger over a campfire: two posts reaching down to the fire and a crossbar the bail hangs from.
    hanger_tex = {"particle": "minecraft:block/spruce_log", "post": "minecraft:block/spruce_log"}
    block_model("cooking_pot_hanger", {
        "parent": "minecraft:block/block", "textures": hanger_tex,
        "elements": [
            box([-0.5, -9, 7], [1.5, 16, 9], "#post"),
            box([14.5, -9, 7], [16.5, 16, 9], "#post"),
            box([1.5, 15, 7.5], [14.5, 16.5, 8.5], "#post"),
        ],
    })
    for contents in ("water", "stew"):
        for servings in (1, 2, 3):
            height = 3 + servings * 2
            block_model(f"cooking_pot_{contents}_{servings}", {
                "parent": "minecraft:block/block",
                "textures": {"particle": rl(f"block/cooking_pot_{contents}"), "liquid": rl(f"block/cooking_pot_{contents}")},
                "elements": [{"from": [3, height, 3], "to": [13, height, 13], "faces": {"up": face("#liquid", uv=[3, 3, 13, 13])}}],
            })
    parts = []
    for facing, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270)):
        a = {"model": rl("block/cooking_pot")}
        h = {"model": rl("block/cooking_pot_hanger")}
        if y:
            a["y"] = y
            h["y"] = y
        parts.append({"apply": a, "when": {"facing": facing}})
        parts.append({"apply": h, "when": {"facing": facing, "hanging": "true"}})
    for contents in ("water", "stew"):
        for servings in (1, 2, 3):
            parts.append({"apply": {"model": rl(f"block/cooking_pot_{contents}_{servings}")},
                          "when": {"contents": contents, "servings": str(servings)}})
    blockstate("cooking_pot", {"multipart": parts})
    block_item("cooking_pot")
    loot_self("cooking_pot")
    lang(f"block.{NS}.cooking_pot", "Cooking Pot", "Panela")
    recipe("cooking_pot", {"type": "minecraft:crafting_shaped", "category": "misc",
                           "key": {"#": "minecraft:iron_ingot"}, "pattern": ["# #", "###"], "result": {"id": rl("cooking_pot")}})
    tag("block", "minecraft:mineable/pickaxe", rl("cooking_pot"))
    tag("block", rl("cooking_pot_heat_sources"), "#minecraft:fire", "minecraft:magma_block", "minecraft:lava")


# --------------------------------------------------------------------------------------------------------------
# Items
# --------------------------------------------------------------------------------------------------------------

def gen_items():
    stews = [
        ("forest_stew", "Forest Stew", "Ensopado da Floresta"),
        ("hearty_stew", "Hearty Stew", "Ensopado Reforçado"),
        ("pumpkin_soup", "Pumpkin Soup", "Sopa de Abóbora"),
        ("berry_compote", "Berry Compote", "Compota de Frutas Vermelhas"),
    ]
    for name, en, pt in stews:
        # The bowl is the vanilla bowl texture; only the contents are new art.
        generated_item(name, "minecraft:item/bowl", rl(f"item/{name}_contents"))
        lang(f"item.{NS}.{name}", en, pt)

    generated_item("acorn", rl("item/acorn"))
    lang(f"item.{NS}.acorn", "Acorn", "Bolota")
    generated_item("antler", rl("item/antler"))
    lang(f"item.{NS}.antler", "Antler", "Galhada")

    item_model("walking_stick", {"parent": "minecraft:item/handheld", "textures": {"layer0": rl("item/walking_stick")}})
    item_def("walking_stick", rl("item/walking_stick"))
    lang(f"item.{NS}.walking_stick", "Walking Stick", "Cajado de Caminhada")
    recipe("walking_stick", {"type": "minecraft:crafting_shaped", "category": "equipment",
                             "key": {"/": "minecraft:stick", "S": "minecraft:string", "L": "minecraft:leather"},
                             "pattern": ["  /", " S ", "/  "], "result": {"id": rl("walking_stick")}})
    recipe("walking_stick_from_antler", {"type": "minecraft:crafting_shaped", "category": "equipment",
                                         "key": {"/": "minecraft:stick", "A": rl("antler")},
                                         "pattern": ["  A", " / ", "/  "], "result": {"id": rl("walking_stick")}})

    generated_item("ranger_lookout_map", rl("item/ranger_lookout_map"))
    lang(f"item.{NS}.ranger_lookout_map", "Ranger Lookout Map", "Mapa de Mirante")

    generated_item("antlers_banner_pattern", rl("item/antlers_banner_pattern"))
    lang(f"item.{NS}.antlers_banner_pattern", "Banner Pattern", "Figura para Estandarte")
    lang(f"item.{NS}.antlers_banner_pattern.desc", "Antlers", "Galhada")
    recipe("antlers_banner_pattern", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                      "ingredients": ["minecraft:paper", rl("antler")], "result": {"id": rl("antlers_banner_pattern")}})



# --------------------------------------------------------------------------------------------------------------
# Tags that don't belong to one block
# --------------------------------------------------------------------------------------------------------------

def gen_misc_tags():
    tag("item", rl("deer_food"), "minecraft:apple", "minecraft:golden_apple", "minecraft:wheat", rl("acorn"))
    tag("item", rl("owl_food"), "minecraft:rabbit", "minecraft:chicken", "minecraft:cod", "minecraft:salmon")
    tag("item", rl("brown_bear_food"), "minecraft:sweet_berries", rl("cranberries"), "minecraft:honeycomb", "minecraft:salmon")
    tag("item", rl("squirrel_food"), rl("acorn"), "minecraft:sweet_berries", "minecraft:glow_berries")


# --------------------------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------------------------

def write_tags():
    for (registry, ns, path), entries in sorted(TAGS.items()):
        base = DATA_NS if ns == NS else os.path.join(RES, "data", ns)
        write(os.path.join(base, "tags", registry, f"{path}.json"), {"replace": False, "values": entries})


def write_lang():
    write(os.path.join(ASSETS, "lang", "en_us.json"), dict(sorted(EN.items())))
    missing = sorted(set(EN) - set(PT))
    if missing:
        raise SystemExit(f"Missing pt_br translations: {missing}")
    write(os.path.join(ASSETS, "lang", "pt_br.json"), dict(sorted(PT.items())))


def main():
    for d in GENERATED:
        if os.path.isdir(d):
            shutil.rmtree(d)

    gen_wood_families()
    gen_terracotta_and_concrete()
    gen_thatch_and_peat()
    gen_plants()
    gen_camping_blocks()
    gen_items()
    gen_misc_tags()

    import gen_content  # noqa: E402  (biomes, mobs, structures, data-driven extras)
    gen_content.generate(globals())

    write_tags()
    write_lang()
    print(f"Wrote {len(EN)} translations and {len(TAGS)} tags.")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
