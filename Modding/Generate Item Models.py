import textwrap
import pathlib

generateMCMETA = False
generateItemBlock = True
texturePath = "textures/items"
arr = ["resistance_totem", "strength_totem", "haste_totem", "regeneration_totem", "jumpboost_totem", "swiftness_totem"]

pathlib.Path('models/item').mkdir(parents=True, exist_ok=True)
if (generateMCMETA):
    pathlib.Path(texturePath).mkdir(parents=True, exist_ok=True)

if (generateItemBlock == False):
    for i in range (0, len(arr)):
        with open("models/item/{0}_totem.json".format(arr[i]), "w+") as file:
            file.write(str(textwrap.dedent('''
                {{
                    "parent": "item/generated",
                    "textures": {{
                        "layer0": "monstertotems:blocks/potion_totems/{0}"
                    }}
                }}
            '''.format(arr[i]))))
            file.close()

if(generateItemBlock):
    for i in range(0, len(arr)):
        with open("models/item/{0}.json".format(arr[i]), "w+") as file:
            file.write(str(textwrap.dedent('''
                {{
                    "parent": "monstertotems:block/{0}",
                }}
            '''.format(arr[i]))))
            file.close()

if(generateMCMETA):
    with open("{0}/{1}.png.mcmeta".format(texturePath, arr[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
            {{
                "animation": {{
                    "interpolate": true,
                    "frametime": 1
                }}
            }}
        '''.format(arr[i]))))
        file.close()