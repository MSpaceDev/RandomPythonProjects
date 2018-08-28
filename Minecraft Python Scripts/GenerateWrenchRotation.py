colours = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]

with open("wrench_rotation.txt", "w+") as f:
	for c in colours:
		upper = c[0].upper() + c[1:]
		f.write("""# Rotates the {1} Glazed Terracotta
execute as @s[scores={{wrench_rotateUp=..0}}] if block ~ ~ ~ {0}_glazed_terracotta[facing=north] run scoreboard players set @s wrench_rotateUp 1
execute as @s[scores={{wrench_rotateUp=..1}}] if block ~ ~ ~ {0}_glazed_terracotta[facing=north] run setblock ~ ~ ~ {0}_glazed_terracotta[facing=west]
execute as @s[scores={{wrench_rotateUp=..0}}] if block ~ ~ ~ {0}_glazed_terracotta[facing=east] run setblock ~ ~ ~ {0}_glazed_terracotta[facing=north]
execute as @s[scores={{wrench_rotateUp=..0}}] if block ~ ~ ~ {0}_glazed_terracotta[facing=south] run setblock ~ ~ ~ {0}_glazed_terracotta[facing=east]
execute as @s[scores={{wrench_rotateUp=..0}}] if block ~ ~ ~ {0}_glazed_terracotta[facing=west] run setblock ~ ~ ~ {0}_glazed_terracotta[facing=south]\n\n""".format(c, upper))