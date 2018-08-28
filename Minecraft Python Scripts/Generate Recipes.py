import textwrap

wood = ["oak", "spruce", "birch", "jungle", "dark_oak", "acacia"]
stone = ["mossy", "cracked", "chiseled"]
quartz = ["quartz_block", "chiseled_quartz_block", "quartz_pillar"]
sandstone = ["sandstone", "chiseled_sandstone", "cut_sandstone"]
redsandstone = ["red_sandstone", "chiseled_red_sandstone", "cut_red_sandstone"]
blocks = ["cobblestone", "brick", "nether_brick", "purpur"]

for i in range(0, len(blocks)):
    with open("recipes/stairs_{0}.json".format(blocks[i]), "w+") as file:
        file.write(str(textwrap.dedent('''
{{
    "type": "crafting_shaped",
    "pattern": [
        "#  ",
        "## ",
        "###"
    ],
    "key": {{
        "#": {{
            "item": "minecraft:{0}"
        }}
    }},
    "result": {{
        "item": "minecraft:{0}_stairs",
        "count": 8
    }}
}}
        '''.format(blocks[i]))))
        file.close()