import math

radius = 500
block = "stained_glass 0"
replace = ""
selector = "@a"

coords = []

for phi in range (0, 314):
    for theta in range (0, 628):
        x = radius * math.sin(phi / 100) * math.cos(theta / 100)
        y = radius * math.sin(phi / 100) * math.sin(theta / 100)
        z = radius * math.cos(phi / 100)
        coords.append("execute {5} ~ ~ ~ fill ~{0} ~{1} ~{2} ~{0} ~{1} ~{2} {3} replace {4}".format(round(x), round(y), round(z), block, replace,selector))

print("\n".join(list(set(coords))))
