from pick import pick
from colorama import Fore, Style
import textwrap
import re
import os

def Continue():
	tryagain = input(f"{Fore.LIGHTCYAN_EX}\nContinue? [Y/N]: {Style.RESET_ALL}")
	if(tryagain == "Y" or tryagain == "y"):
		return True
	else:
		return False

def calcLengthToTicks(length):
	time = re.findall("\d+", length)
	seconds = int(time[0]) * 60
	seconds += int(time[1])
	seconds += (int(time[2]) / 1000)
	ticks = seconds * 20
	return int(ticks - 1)

while True:
	sound_type, index = pick(
			title="Select the sound you want generated: [Use UP & DOWN arrows]",
			options = ["Loopable", "Random Event", "Single Fire"]
		)

	os.system('cls')

	print(f"{Fore.LIGHTGREEN_EX}Enter the appropriate properties:\n")
	print(f"{Fore.LIGHTCYAN_EX}SOUNDID - The ID given to the AEC. Used as the sound's source location [{Fore.LIGHTYELLOW_EX}eg. 1{Fore.LIGHTCYAN_EX}]")
	print(f"CONDITION - Checks an entity before playing the sound to the player [{Fore.LIGHTYELLOW_EX}eg. @a[tag=hasItem,scores={{item=1}}]{Fore.LIGHTCYAN_EX}]")
	print(f"SOUND PATH - The path from sounds/.. [{Fore.LIGHTYELLOW_EX}eg. custom/loop{Fore.LIGHTCYAN_EX}]")
	print(f"RADIUS - The distance the sound can be heard [{Fore.LIGHTYELLOW_EX}eg. 16{Fore.LIGHTCYAN_EX}] (0 = GLOBAL SOUND)")

	if (sound_type == "Loopable"):
		print(f"LENGTH - The duration of the sound [{Fore.LIGHTYELLOW_EX}eg. 1m 25s 525ms{Fore.LIGHTCYAN_EX}] (Whitespace doesn't matter)")
		print(f"IMPORTANT - Determines whether all players will be tp'd to the sound and back to their old location. Will make the sound hearable in that radius to all players who weren't there initailly [{Fore.LIGHTYELLOW_EX}Y/N{Fore.LIGHTCYAN_EX}]{Style.RESET_ALL}\n")

	id = input(f"{Fore.LIGHTYELLOW_EX}Sound ID: ")
	condition = input("Condition (Leave empty for just a radius): ")
	sound_name = input("Sound Path: ")
	radius = input("Radius: ")

	if(sound_type == "Loopable"):
		length = input("Length: ")
		important = input("Important? (Y/N): ")

	print(f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}")
	if(id == ""):
		os.system('cls')
		print("ERROR:\nSound ID not specified!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif(sound_name == ""):
		os.system('cls')
		print("ERROR:\nSound Name not specified!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif(radius == ""):
		os.system('cls')
		print("ERROR:\nRadius was not specified!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif(length == ""):
		os.system('cls')
		print("ERROR:\nLength not specified!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif (re.match("^[\d]+$", id) is None):
		os.system('cls')
		print("ERROR:\nSound ID only accepts integers!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif (re.search("[:*?\"<>|\\\]", sound_name)):
		os.system('cls')
		print("ERROR:\nSound Name cannot contain the following characters \\ : * ? \" < > |!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif(re.match("^[\d]+\.?[\d]*$", radius) is None):
		os.system('cls')
		print("ERROR:\nRadius only accepts integers or doubles!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif(re.match("^\d+m\s*\d+s\s*\d+ms$", length) is None):
		os.system('cls')
		print(f"ERROR:\nLength must be entered in the format {Fore.LIGHTYELLOW_EX}1m 1s 1ms!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break
	elif (sound_type == "Loopable" and float(radius) < 16 and float(radius) > 0):
		os.system('cls')
		print("ERROR:\nLOOPABLE SOUND TYPE: The radius has to be 16 blocks or more!")
		if (Continue()):
			continue
		else:
			os.system('cls')
			break

	if (float(radius).is_integer()):
		radius = int(radius)
	else:
		radius = float(radius)

	volume = 0
	if radius == 0:
		volume = 1000000.0
		radius = 1000000.0
	else:
		volume = float(radius / 16)

	ticks = calcLengthToTicks(length)

	with open("sound_" + sound_name + ".mcfunction", 'w+') as f:
		if (sound_type == "Loopable"):
			f.write(str(textwrap.dedent(
				'''# [LOOPABLE] sound_{0} Function

# Loop sound when standing in radius
scoreboard players add @a[distance=0..{1}] loop 1
execute if entity @a[distance=0..{1},scores={{loop=1}}] run playsound minecraft:loop voice @a[distance=0..{1}] ~ ~ ~ {2}
scoreboard players set @a[distance=0..{1},scores={{loop={3}..}}] loop 0
				'''
			)).format(sound_name, radius, volume, ticks, id))

			if(radius != 1000000.0):
				f.write(str(textwrap.dedent(
					'''
	# Stop sound and reset values upon leaving radius
	execute as @a[distance={1}..,scores={{loop=1..}}] run stopsound @s voice minecraft:{0}
	execute as @a[distance={1}..,scores={{loop=1..}}] run scoreboard players set @s loop 0
					'''
				)).format(sound_name, radius + 0.001))

			if(condition == ""):
				f.write(str(textwrap.dedent(
					'''
		# MOVE THIS COMMAND TO -> LOOP.MCFUNCTION
		execute as @s[type=area_effect_cloud,scores={{soundID={1}}}] at @s run function soundengine:loopable/sound_{0}	
					'''
				)).format(sound_name, id))
			else:
				f.write(str(textwrap.dedent(
					'''
		# MOVE THIS COMMAND TO -> LOOP.MCFUNCTION
		execute as @s[type=area_effect_cloud,scores={{soundID={1}}}] at @s if entity {2} run function soundengine:loopable/sound_{0}	
					'''
				)).format(sound_name, id, condition))

	print(f"{Fore.LIGHTGREEN_EX}MCFunction file generated successfully!{Style.RESET_ALL}")
	break
