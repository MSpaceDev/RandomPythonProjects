coords = open("E:\\User\\Desktop\\coords.txt", "r").read().splitlines()

entity = "armor_stand"
nbt = "{ArmorItems:[{},{},{},{id:\"minecraft:diamond_helmet\",Count:1b}],NoBasePlate:1b,ShowArms:1b}"

y = 0

for string in coords:
    string = string.replace("~ ","")
    x,z = string.split(" ")
    print("summon " + entity + " " + x + " ~" + str(y) + " " + z + " " + nbt)
    y -= 1
