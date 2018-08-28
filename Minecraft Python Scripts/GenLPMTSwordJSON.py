import re

damage = 251

mobName = [
	"bat",
	"blaze",
	"chicken",
	"cow",
	"creeper",
	"drowned",
	"dolphin",
	"elderGuardian",
	"enderDragon",
	"enderman",
	"endermite",
	"evoker",
	"ghast",
	"guardian",
	"horse",
	"husk",
	"llama",
	"magmaCube",
	"mooshroom",
	"ocelot",
	"parrot",
	"phantom",
	"pig",
	"polarBear",
	"rabbit",
	"slime",
	"shulker",
	"silverfish",
	"skeleton",
	"snowman",
	"spider",
	"stray",
	"squid",
	"turtle",
	"vex",
	"villager",
	"vindicator",
	"wolf",
	"witch",
	"witherSkeleton",
	"villagerGolem",
	"zombie",
	"zombieVillager",
	"zombiePigman",
	"cod",
	"salmon",
	"tropicalFish",
	"pufferfish",
	"wither"
]

def convertSnake(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

overrides = []

mobNo = -1
for i in range(0, damage):
	percent = 1 /  damage * i
	if (mobNo == -1):
		overrides.append({"predicate": {"damaged": 0, "damage": percent}, "model": "item/iron_sword"})
		mobNo += 1
	elif(i < len(mobName) + 1):
		overrides.append({ "predicate": {"damaged": 0, "damage": percent}, "model": "item/custom/swords/mobs/%s"%(convertSnake(mobName[mobNo]))})
		mobNo += 1
	else:
		overrides.append({ "predicate": {"damaged": 0, "damage": percent}, "model": "item/custom/update_pack"})

for d in overrides:
	predicate = str(d) + ","
	predicate = predicate.replace("\'", "\"")
	predicate = predicate.replace("{", "{ ", 1)
	print("\t   ",predicate)