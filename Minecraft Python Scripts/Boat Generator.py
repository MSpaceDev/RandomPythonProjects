import pyperclip

#Set tags
firstBoatTag = "boat_first2"
boatTag = "boat_middle2"
lastBoatTag = "boat_last2"
armorStandTag = "boat_armorStand2"

# Amount
boatAmount = 2

start = "/summon boat ~ ~1 ~ {NoGravity:1b,Tags:[\"%s\",\"%s\"]" % (firstBoatTag, boatTag)

for i in range(boatAmount - 1):
	if i < boatAmount - 2:
		start += ("," + "Passengers:[{id:\"minecraft:armor_stand\",Tags:[\"%s\",\"%s\"]},{id:\"minecraft:boat\",NoGravity:1b,Tags:[\"%s\"]" % (armorStandTag, boatTag, boatTag))
	else:
		start += ("," + "Passengers:[{id:\"minecraft:armor_stand\",Tags:[\"%s\",\"%s\"]},{id:\"minecraft:boat\",NoGravity:1b,Tags:[\"%s\",\"%s\"]" % (armorStandTag, boatTag, lastBoatTag, boatTag))
start += "}"
for j in range(boatAmount - 1):
	start += "]}"

print("Command copied to clipboard!\n", start)
pyperclip.copy(start)