import math
import pyperclip

radius = 20
blocks = ["air"]
width = 100
depth = 1

coords = []

for k in range(0, depth):
	for j in range (0, width):
		for i in range (0, 360):
			x = radius * math.cos(math.radians(i))
			y = radius * math.sin(math.radians(i))
			coords.append("execute at @s run fill ~%s ~-%s ~%s ~%s ~-%s ~%s %s replace red_concrete"%(round(x), depth - k, round(y), round(x), depth - k, round(y), blocks[i%len(blocks)]))
		radius += 1
	radius = 1

print("\n".join(list(set(coords))))
pyperclip.copy("\n".join(list(set(coords))))