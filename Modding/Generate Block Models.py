import textwrap

arr = ["zombie", "skeleton", "creeper", "spider", "enderman", "witch", "silverfish", "slime", "blaze", "zombie_pigman", "ghast", "magma_cube"]

for i in range (0, 12):
    with open("models/block/{0}_infused_log.json".format(arr[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
            {{
                "parent": "block/cube_all",
                "textures": {{
                    "all": "monstertotems:blocks/infused_logs/{0}_infused_log"
                }}
            }}
        '''.format(arr[i]))))
        file.close()

    with open("models/item/{0}_infused_log.json".format(arr[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
            {{
                "parent": "monstertotems:block/{0}_infused_log"
            }}
        '''.format(arr[i]))))
        file.close()

    with open("blockstates/{0}_infused_log.json".format(arr[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
            {{
                "variants": {{
                    "normal": {{ "model": "monstertotems:{0}_infused_log"}}
                }}
            }}
        '''.format(arr[i]))))
        file.close()

    with open("textures/blocks/infused_logs/{0}_infused_log.png.mcmeta".format(arr[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
            {{
                "animation": {{
                    "interpolate": true,
                    "frametime": 10
                }},
                "texture": {{
                    "blur": true
                }}
            }}
        '''.format(arr[i]))))
        file.close()