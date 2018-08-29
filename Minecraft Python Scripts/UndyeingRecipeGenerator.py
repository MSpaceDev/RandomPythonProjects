import os
from json import dumps

blocks = ["stained_glass", "stained_glass_pane", "terracotta", "glazed_terracotta", "concrete_powder", "concrete", "carpet", "wool"]
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
except:
	pass

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

		# Block Tags
		tags_base["values"].append("minecraft:%s_%s" % (colour, block))

		# Write to files
		with open("universal_dyeing/recipes/{1}_{0}.json".format(block, colour), "w+") as f:
			f.write(dumps(crafting_base, indent=4))
		with open("universal_dyeing/tags/items/{0}.json".format(block, colour), "w+") as f:
			f.write(dumps(tags_base, indent=4))