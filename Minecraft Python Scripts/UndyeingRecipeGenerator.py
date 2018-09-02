import os
from json import dumps

blocks = ["stained_glass", "stained_glass_pane", "terracotta", "glazed_terracotta", "concrete_powder", "wool"]
colours = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
isOnetoOne = True


crafting_base = \
{
	"type": "crafting_shaped",
	"pattern": [
		"###",
		"#O#",
		"###"
	],
	"key": {
		"#": {
			"tag": ""
		},
		"O": {
			"item": ""
		}
	},
	"result": {
		"item": "",
		"count": 8
	},
	"group": ""
}

advancement_base = \
{
	"parent": "minecraft:recipes/root",
	"criteria": {
		"has_block": {
			"trigger": "minecraft:inventory_changed",
			"conditions": {
				"items": [
					{
						"tag": ""
					}
				]
			}
		},
		"has_dye": {
			"trigger": "minecraft:inventory_changed",
			"conditions": {
				"items": [
					{
						"tag": "universal_dyeing:dyes"
					}
				]
			}
		}
	},
	"requirements": [
		["has_block"],
		["has_dye"]
	],
	"rewards": {
		"recipes": []
	}
}

dyes = \
{
	"white": "bone_meal",
	"orange": "orange_dye",
	"magenta": "magenta_dye",
	"light_blue": "light_blue_dye",
	"yellow": "dandelion_yellow",
	"lime": "lime_dye",
	"pink": "pink_dye",
	"gray": "gray_dye",
	"light_gray": "light_gray_dye",
	"cyan": "cyan_dye",
	"purple": "purple_dye",
	"blue": "lapis_lazuli",
	"brown": "cocoa_beans",
	"green": "cactus_green",
	"red": "rose_red",
	"black": "ink_sac"
}

tags_base = { "values": [] }

try:
	os.mkdir("universal_dyeing")
	os.mkdir("universal_dyeing/recipes")
	os.mkdir("universal_dyeing/tags")
	os.mkdir("universal_dyeing/tags/items")
	os.mkdir("universal_dyeing/advancements")
	os.mkdir("universal_dyeing/advancements/recipes")
	os.mkdir("universal_dyeing/advancements/recipes/building_blocks")
	os.mkdir("universal_dyeing/advancements/recipes/building_blocks/universal_dyeing")
except:
	pass


terracotta = []
glazed_terracotta = []
concrete_powder = []
stained_glass = []
stained_glass_pane = []
wool = []
for b in blocks:
	for c in colours:
		if b == "terracotta":
			terracotta.append("universal_dyeing:" + c + "_" + b)
		elif b == "glazed_terracotta":
			glazed_terracotta.append("universal_dyeing:" + c + "_" + b)
		elif b == "concrete_powder":
			concrete_powder.append("universal_dyeing:" + c + "_" + b)
		elif b == "stained_glass":
			stained_glass.append("universal_dyeing:" + c + "_" + b)
		elif b == "stained_glass_pane":
			stained_glass_pane.append("universal_dyeing:" + c + "_" + b)
		elif b == "wool":
			wool.append("universal_dyeing:" + c + "_" + b)

# Generate all "block to clear" recipes
crafting_base["key"]["O"]["item"] = "minecraft:ice"
for i in range(3):
	block = blocks[i]
	crafting_base["key"]["#"]["tag"] = "universal_dyeing:%s" % block
	crafting_base["result"]["item"] = "minecraft:%s" % block

	# If stained_glass or stained_glass_pane
	if(i <= 1):
		glass = block[8:]
		crafting_base["result"]["item"] = "minecraft:%s" % glass

	with open("universal_dyeing/recipes/{0}_to_clear.json".format(block), "w+") as f:
		f.write(dumps(crafting_base, indent=4))

# Generate all "block_to_colour_block" recipes and Block Tags
for block in blocks:
	if (isOnetoOne and block == "wool"):
		crafting_base["type"] = "crafting_shapeless"
		crafting_base["result"]["count"] = 1
		crafting_base.pop("pattern")
		crafting_base.pop("key")
		ingredients = [{"tag": "wool"}, {"item": ""}]
		crafting_base["ingredients"] = ingredients
	else:
		crafting_base["key"]["#"]["tag"] = "universal_dyeing:%s" % block

	tags_base["values"].clear()
	for colour in colours:
		if (isOnetoOne and block == "wool"):
			# Recipes OnetoOne
			crafting_base["result"]["item"] = "minecraft:%s_%s" % (colour, block)
			crafting_base["ingredients"][1]["item"] = "minecraft:%s" % dyes.get(colour)
		else:
			# Recipes OnetoEight
			crafting_base["result"]["item"] = "minecraft:%s_%s" % (colour, block)
			crafting_base["key"]["O"]["item"] = "minecraft:%s" % dyes.get(colour)

		crafting_base["group"] = "universal_dyeing_" + block
		# Block Tags
		tags_base["values"].append("minecraft:%s_%s" % (colour, block))

		# Write to files
		with open("universal_dyeing/recipes/{1}_{0}.json".format(block, colour), "w+") as f:
			f.write(dumps(crafting_base, indent=4))
		with open("universal_dyeing/tags/items/{0}.json".format(block, colour), "w+") as f:
			f.write(dumps(tags_base, indent=4))

for b in blocks:
	with open("universal_dyeing/advancements/recipes/building_blocks/universal_dyeing/" + b + ".json", "w+") as f:
		if b == "terracotta":
			advancement_base["rewards"]["recipes"] = terracotta
		elif b == "glazed_terracotta":
			advancement_base["rewards"]["recipes"] = glazed_terracotta
		elif b == "concrete_powder":
			advancement_base["rewards"]["recipes"] = concrete_powder
		elif b == "stained_glass":
			advancement_base["rewards"]["recipes"] = stained_glass
		elif b == "stained_glass_pane":
			advancement_base["rewards"]["recipes"] = stained_glass_pane
		elif b == "wool":
			advancement_base["rewards"]["recipes"] = wool

		advancement_base["criteria"]["has_block"]["conditions"]["items"] = [{"tag": "universal_dyeing:" + b}]

		f.write(dumps(advancement_base, indent=4))