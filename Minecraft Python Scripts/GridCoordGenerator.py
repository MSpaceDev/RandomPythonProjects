center = 0
diameter = 192
step = 32
y = 60

interval = diameter / step
corner = center + (diameter/2)
x = corner
z = corner

for i in range (0, int(interval) + 1):
    for j in range (0, int(interval) + 1):
        print("execute @a[tag=s] ~ ~ ~ setblock {0} {1} {2} structure_block 0 replace {{posX:-31,posY:0,posZ:-31,name:\"clear_map\",mode:\"LOAD\"}}".format(x,y,z))
        print("execute @a[tag=s] ~ ~ ~ setblock {0} {1} {2} redstone_block".format(x,y + 1,z))
        z -= step
    z = corner
    x -= step
