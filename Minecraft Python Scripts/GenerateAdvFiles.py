import re
import os
import codecs

# Plural Engine
import inflect
p = inflect.engine()

mobName = {
	"bat": {"count": 10, "item": "leather", "color": "dark_gray", "name": "Bat Mo' Sword"},
	"blaze": {"count": 1000, "item": "blaze_rod", "color": "gold", "name": "Blazing Heart"},
	"chicken": {"count": 200, "item": "feather", "color": "yellow", "name": "The Chef"},
	"cow": {"count": 200, "item": "beef", "color": "gold", "name": "Steak Stabber"},
	"creeper": {"count": 100, "item": "gunpowder", "color": "green", "name": "Sonic Boom"},
	"drowned": {"count": 100, "item": "trident", "color": "dark_aqua", "name": "Siren's Curse"},
	"dolphin": {"count": 10, "item": "cod", "color": "aqua", "name": "The Flipper"},
	"elderGuardian": {"count": 3, "item": "wet_sponge", "color": "blue", "name": "Old Man's Sword"},
	"enderDragon": {"count": 1, "item": "elytra", "color": "light_purple", "name": "Dragon Scythe"},
	"enderman": {"count": 5000, "item": "ender_pearl", "color": "dark_purple", "name": "The Ender Mincer"},
	"endermite": {"count": 25, "item": "obsidian", "color": "light_purple", "name": "The Ender Might"},
	"evoker": {"count": 1, "item": "totem_of_undying", "color": "gold", "name": "The Wololo"},
	"ghast": {"count": 20, "item": "ghast_tear", "color": "white", "name": "Ghastly Sharp"},
	"guardian": {"count": 50, "item": "prismarine_shard", "color": "aqua", "name": "Guardian Gutter"},
	"horse": {"count": 25, "item": "leather", "color": "gold", "name": "The Racing Blade"},
	"husk": {"count": 100, "item": "sand", "color": "yellow", "name": "Deadly Heat"},
	"llama": {"count": 25, "item": "lead", "color": "yellow", "name": "Spitter Splitter"},
	"magmaCube": {"count": 500, "item": "magma_cream", "color": "gold", "name": "Magma Musher"},
	"mooshroom": {"count": 50, "item": "red_mushroom", "color": "red", "name": "Mycelium Muncher"},
	"ocelot": {"count": 10, "item": "cod", "color": "gold", "name": "Kitty Killer"},
	"parrot": {"count": 10, "item": "feather", "color": "red", "name": "The Parrot Pecker"},
	"phantom": {"count": 20, "item": "phantom_membrane", "color": "green", "name": "Twinkle Twinkle"},
	"pig": {"count": 200, "item": "porkchop", "color": "light_purple", "name": "The Oinker"},
	"polarBear": {"count": 10, "item": "snowball", "color": "white", "name": "Bear Beater"},
	"rabbit": {"count": 25, "item": "rabbit_foot", "color": "white", "name": "Carrot Killer"},
	"slime": {"count": 2000, "item": "slime_ball", "color": "green", "name": "Slime Mace"},
	"shulker": {"count": 200, "item": "shulker_shell", "color": "light_purple", "name": "Shulker Shucker"},
	"silverfish": {"count": 200, "item": "stone", "color": "gray", "name": "Silverslicer"},
	"skeleton": {"count": 1000, "item": "bone", "color": "white", "name": "Bone Basher"},
	"snowGolem": {"count": 100, "item": "snow_block", "color": "aqua", "name": "Frozen Heart"},
	"spider": {"count": 1000, "item": "string", "color": "dark_red", "name": "Spidey Sense"},
	"stray": {"count": 100, "item": "tipped_arrow", "color": "dark_aqua", "name": "Paralyzing Stare"},
	"squid": {"count": 50, "item": "ink_sac", "color": "dark_blue", "name": "Squid Squisher"},
	"turtle": {"count": 10, "item": "turtle_egg", "color": "green", "name": "The Turtleman"},
	"vex": {"count": 25, "item": "iron_sword", "color": "aqua", "name": "The Vexinator"},
	"villager": {"count": 25, "item": "emerald", "color": "yellow", "name": "The Hmmmer"},
	"vindicator": {"count": 100, "item": "iron_axe", "color": "gray", "name": "The Vindicator"},
	"wolf": {"count": 25, "item": "bone", "color": "red", "name": "Doggy Dicer"},
	"witch": {"count": 100, "item": "potion", "color": "dark_purple", "name": "Bewitcher"},
	"witherSkeleton": {"count": 200, "item": "wither_skeleton_skull", "color": "dark_gray", "name": "Withering Soul"},
	"ironGolem": {"count": 25, "item": "iron_block", "color": "white", "name": "True Iron"},
	"zombie": {"count": 1000, "item": "rotten_flesh", "color": "green", "name": "Village Protector"},
	"zombieVillager": {"count": 100, "item": "rotten_flesh", "color": "dark_green", "name": "Village Betrayer"},
	"zombiePigman": {"count": 5000, "item": "golden_sword", "color": "light_purple", "name": "Pigman Slicer"},
	"cod": {"count": 50, "item": "cod_bucket", "color": "yellow", "name": "Cod Sword"},
	"salmon": {"count": 50, "item": "salmon_bucket", "color": "red", "name": "Salmon Sword"},
	"tropicalFish": {"count": 50, "item": "tropical_fish_bucket", "color": "yellow", "name": "Clown Sword"},
	"pufferfish": {"count": 50, "item": "pufferfish_bucket", "color": "yellow", "name": "Pokey Stick"},
	"wither": {"count": 1, "item": "nether_star", "color": "yellow", "name": "Wither Bane"}
}

def convertSnake(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convertSentence(name):
	name = re.sub("([a-z])([A-Z])","\g<1> \g<2>", name)
	name = name[0].upper() + name[1:]
	if (name == "Evoker"):
		return "Giant Evoker Boss"
	else:
		return name

def convertScore(name):
	if name == "witherSkeleton":
		name = "wSkeleton"
	elif name == "zombieVillager":
		name = "zVillager"
	elif name == "elderGuardian":
		name = "eGuardian"
	return name

def getColorCode(color):
	if color == "dark_red":
		return 4
	elif color == "red":
		return "c"
	elif color == "gold":
		return 6
	elif color == "yellow":
		return "e"
	elif color == "dark_green":
		return 2
	elif color == "green":
		return "a"
	elif color == "aqua":
		return "b"
	elif color == "dark_aqua":
		return 3
	elif color == "dark_blue":
		return 1
	elif color == "blue":
		return 9
	elif color == "light_purple":
		return "d"
	elif color == "dark_purple":
		return 5
	elif color == "white":
		return "f"
	elif color == "gray":
		return 7
	elif color == "dark_gray":
		return 8
	elif color == "black":
		return 0

def createPath(pathName):
	try:
		os.mkdir(pathName)
	except:
		pass

createPath("advancements")
createPath("advancements/functions")
createPath("advancements/functions/swords")
createPath("advancements/functions/swords/mobs")
createPath("advancements/advancements")
for i in range(3,10):
	createPath("advancements/advancements/row%s"%i)

# Initial values
i = 1
row = 3
last = "advancements:root"

# Create files from dictionary (Advancements, Functions and Test Function)
for k, v in mobName.items():
	snakeKey = convertSnake(k)
	sentenceKey = convertSentence(k)
	scoreName = convertScore(k)
	colorCode = getColorCode(v.get("color"))

	with codecs.open("advancements/functions/swords/mobs/kill_%s.mcfunction"%snakeKey, "w+", encoding='utf-8') as f:
		f.write("""# Desc: Checks if player has killed {0} {10} and gives sword
#
# Called by: advancements:advancements/row{9}/{4}_sword

give @s[scores={{adv_{6}={2}..}}] iron_sword{{Damage:{1}s,Unbreakable:1b,display:{{Name:"{{\\\"text\\\":\\\"§r§{7}{5}\\\"}}"}}}}
execute as @s[scores={{adv_{6}={2}..}}] run tellraw @a ["",{{"selector":"@s"}},{{"text":" has completed the challenge "}},{{"text":"[{5}]","color":"dark_purple","hoverEvent":{{"action":"show_text","value":{{"text":"","extra":[{{"text":"{5}","color":"dark_purple"}},{{"text":"\\nKill {0} {10}","color":"white"}}]}}}}}}]
advancement revoke @s[scores={{adv_{6}=..{3}}}] only advancements:row{9}/{4}_sword
		""".format(v.get("count"), i, v.get("count")-1, v.get("count")-2, snakeKey, v.get("name"), scoreName, colorCode, sentenceKey, row, p.plural(sentenceKey)))

	with open("advancements/advancements/row%s/%s_sword.json"%(row,snakeKey), "w+") as f:
		f.write("""{{
    "parent": "{4}",
    "display": {{
        "title": "{5}",
        "description": "Kill {1} {6}",
        "icon": {{
            "item": "minecraft:{2}"
        }},
        "frame": "challenge",
        "announce_to_chat": false
    }},
    "criteria": {{
        "killed_{3}": {{
            "trigger": "minecraft:player_killed_entity",
            "conditions": {{
                "entity": {{
                    "type": "minecraft:{3}"
                }}
            }}
        }}
    }},
    "rewards": {{
        "function": "advancements:swords/mobs/kill_{3}"
    }}
}}
	""".format(sentenceKey, v.get("count"), v.get("item"), snakeKey, last, v.get("name"), p.plural(sentenceKey, v.get("count"))))

	if(i%7 == 0):
		with open("advancements/advancements/row%s/end_row.json"%row, "w+") as f:
			f.write("""{{
    "parent": "advancements:row{0}/{1}_sword",
    "criteria": {{
        "impossible": {{
            "trigger": "minecraft:location"
        }}
    }}
}}
""".format(row, snakeKey))
		row += 1
		last = "advancements:root"
	else:
		last = "advancements:row%s/"%row + snakeKey + "_sword"
	i += 1


# Generates a function to test advancements and other functions
with open("advancements/functions/test_advancements.mcfunction", "w+") as f:
	i = 0
	x = 2
	for k, v in mobName.items():
		if (k == "enderDragon"):
			pass
		else:
			f.write("""summon %s ~%s ~ ~ {Air:1000000,NoAI:1b,Silent:1b,Invulnerable:1b,Health:1.0f}
scoreboard players set @a adv_%s %s\n"""%(convertSnake(k), x, convertScore(k), v.get("count") - 1))
			i += 1
			x += 2
