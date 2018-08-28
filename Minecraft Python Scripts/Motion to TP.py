values = open("E:\\User\\Desktop\\selector.txt", "r").read().splitlines()

i = -180

for string in values:
    sel, tp = str.split(string, " ", 1)
    print("execute {0} ~ ~ ~ summon armor_stand ~ ~ ~ {{Tags:[\"ice_path{1}\",\"ice_path\"],NoGravity:1b}}".format(sel, i))
    i += 1