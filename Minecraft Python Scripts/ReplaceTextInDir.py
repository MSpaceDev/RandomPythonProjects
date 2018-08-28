import os

find = """,
                    "functions": [
                        {
                            "function": "minecraft:set_data",
                            "data": 15
                        }
                    ]"""

replacement = """"""

# for dname, dirs, files in os.walk("C:/Users/user/AppData/Roaming/.minecraft/.latestsnapshot/saves/Update LPMT Functions/datapacks/1.13/data/mobs/loot_tables"):
#     for fname in files:
#         fpath = os.path.join(dname, fname)
#         with open(fpath) as f:
#             s = f.read()
#             s = s.replace(find, replacement)
#         print(s)
#         with open(fpath, "w") as f:
#             f.write(s)

for dname, dirs, files in os.walk("C:/Users/user/AppData/Roaming/.minecraft/.latestsnapshot/saves/Update LPMT Functions/datapacks/1.13/data/minecraft/loot_tables/entities"):
    k = 0
    cmd = []
    for i in files:
        if(dname == "C:/Users/user/AppData/Roaming/.minecraft/.latestsnapshot/saves/Update LPMT Functions/datapacks/1.13/data/minecraft/loot_tables/entities\sheep"):
            continue
        j = i.replace(".json", "")
        print("summon %s ~ ~ ~%s {NoAI:1b,Silent:1b}"%(j, k))
        k = k + 2