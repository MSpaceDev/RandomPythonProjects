components = ["piston", "sticky_piston", "dropper", "dispenser", "observer", "hopper"]

with open("wrench_rotation.txt", "w+") as f:
	for c in components:
		upper = c[0].upper() + c[1:]
		f.write("""# Rotates the {1}
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=north] run scoreboard players set @s wrench_stopLoop 1
execute as @s[scores={{wrench_stopLoop=..1}}] if block ~ ~ ~ {0}[facing=north] run setblock ~ ~ ~ {0}[facing=west]
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=east] run setblock ~ ~ ~ {0}[facing=north]
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=south] run setblock ~ ~ ~ {0}[facing=east]
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=up] run setblock ~ ~ ~ {0}[facing=south]
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=down] run setblock ~ ~ ~ {0}[facing=up]
execute as @s[scores={{wrench_stopLoop=..0}}] if block ~ ~ ~ {0}[facing=west] run setblock ~ ~ ~ {0}[facing=down]\n\n""".format(c, upper))