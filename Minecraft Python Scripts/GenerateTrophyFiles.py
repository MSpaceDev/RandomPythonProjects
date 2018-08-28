import os

damage = 1

#
# TRUE = Has GOLD ; SILVER ; BRONZE
# FALSE = Standalone Trophy
#
trophies = {
	"armour_stand": True,
    "boat_racing": True,
	"elytrapvp": True,
	"monument": False,
	"woodland": False,
	"bloxing": False,
	"notch_apple": False,
	"xp": False,
	"doth": True
}

places = ["gold", "silver", "bronze"]

try:
	os.mkdir("trophies")
	os.mkdir("trophies/get_trophy")
	os.mkdir("trophies/set_trophy")
except:
	pass

def convertSentence(name):
	if name == "elytrapvp":
		return "ElytraPvP"
	elif name == "xp":
		return "XP"
	elif name == "doth":
		return "DotH"

	name = name.replace("_", " ")
	return name.title()

# Set trophy
for k, v in trophies.items():
	if (v == True):
		try:
			os.mkdir("trophies/get_trophy/" + k)
			os.mkdir("trophies/set_trophy/" + k)
		except:
			pass
		for p in places:
			with open("trophies/set_trophy/" + k + "/" + p + ".mcfunction", "w+") as f:
				# If IS NOT direction dependant
				if (k == "doth"):
					f.write('''setblock ~ ~ ~ spawner
data merge block ~ ~ ~ {RequiredPlayerRange:0s}
data merge block ~ ~ ~ {SpawnData:{id:"minecraft:armor_stand",Invisible:1,Marker:1}}

data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}''' % (damage))
					damage += 1
				# Else, block IS direction dependant
				else:
					f.write('''setblock ~ ~ ~ spawner
data merge block ~ ~ ~ {RequiredPlayerRange:0s}
data merge block ~ ~ ~ {SpawnData:{id:"minecraft:armor_stand",Invisible:1,Marker:1}}

execute as @a[tag=north] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=south] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=east] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=west] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}''' % (damage + 1, damage, damage + 3, damage + 2))
					damage += 4

			# get_all.mcfunction
			with open("trophies/get_trophy/" + k + "/" + p + ".mcfunction", "w+") as f:
				f.write('''give @s player_head{SkullOwner:{Id:"a2ecd9b8-fb6f-4426-b740-028de21455b9",Properties:{textures:[{Value:"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMTYyMzRhZTdkNTU5MDNlYThiYzM0NDEzY2Q1MmRlZDNiMzdjOTJlZWU1YWU1MzNmYzUxMjZhNjU0NjFmMTFmIn19fQ=="}]},Name:"%s %s Trophy"},display:{Name:"{\\\"text\\\":\\\"%s %s Trophy\\\",\\\"color\\\":\\\"yellow\\\",\\\"italic\\\":\\\"false\\\"}"}}
''' % (convertSentence(p), convertSentence(k), convertSentence(p), convertSentence(k)))
	else:
		with open("trophies/set_trophy/" + k + ".mcfunction", "w+") as f:
			f.write('''setblock ~ ~ ~ spawner
data merge block ~ ~ ~ {RequiredPlayerRange:0s}
data merge block ~ ~ ~ {SpawnData:{id:"minecraft:armor_stand",Invisible:1,Marker:1}}

execute as @a[tag=north] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=south] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=east] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}
execute as @a[tag=west] run data merge block ~ ~ ~ {SpawnData:{ArmorItems:[{},{},{},{id:"minecraft:diamond_hoe",Count:1b,tag:{Unbreakable:1,Damage:%ss}}]}}''' % (damage + 1, damage, damage + 3, damage + 2))
			damage += 4
		with open("trophies/get_trophy/" + k + ".mcfunction", "w+") as f:
			f.write('''give @s player_head{SkullOwner:{Id:"a2ecd9b8-fb6f-4426-b740-028de21455b9",Properties:{textures:[{Value:"eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMTYyMzRhZTdkNTU5MDNlYThiYzM0NDEzY2Q1MmRlZDNiMzdjOTJlZWU1YWU1MzNmYzUxMjZhNjU0NjFmMTFmIn19fQ=="}]},Name:"%s Trophy"},display:{Name:"{\\\"text\\\":\\\"%s Trophy\\\",\\\"color\\\":\\\"yellow\\\",\\\"italic\\\":\\\"false\\\"}"}}
		''' % (convertSentence(k), convertSentence(k)))

with open("trophies/get_all.mcfunction", "w+") as f:
	for k, v in trophies.items():
		if (v == True):
			for p in places:
				f.write("\nfunction spawner_blocks:get_trophy/" + k + "/" + p)
		else:
			f.write("\nfunction spawner_blocks:get_trophy/" + k)