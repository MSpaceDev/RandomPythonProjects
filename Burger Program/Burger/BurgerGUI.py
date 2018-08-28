import subprocess as sp
import time, threading, os
from tkinter import *
from collections import Counter

class CreateMessage():
	def __init__(self, text, isError,stayTime=5):
		self.move = 0
		self.moveAmount = padY / 2 + 1
		self.stayTime = stayTime

		if (isError):
			color = "#9d1c1c"
		else:
			color = "#43b581"

		self.errorBG = background.create_rectangle(0, mainHeight - 1, mainWidth - 1, mainHeight + padY / 2, fill=color)
		self.errorText = background.create_text(mainWidth / 2, mainHeight + padY / 4 - 1, text=text, fill="white", font="SegoeUILight 11 bold")
		self.errorIn()

	def errorIn(self):
		if (self.move < self.moveAmount):
			background.after(4, self.errorIn)
			background.move(self.errorBG, 0, -1)
			background.move(self.errorText, 0, -1)
		else:
			self.move = 0
			threading._start_new_thread(self.timer, ())
			return
		self.move += 1

	def timer(self):
		time.sleep(self.stayTime)
		self.errorOut()
		return

	def errorOut(self):
		if (self.move < self.moveAmount):
			background.after(4, self.errorOut)
			background.move(self.errorBG, 0, 1)
			background.move(self.errorText, 0, 1)
		else:
			background.delete(self.errorBG)
			background.delete(self.errorText)
			return
		self.move += 1


# Useful classes to easily create Tkinter widgets on a canvas
class CreateCheckbox():
	def __init__(self, x, y, text, function, isChecked):
		self.isChecked = IntVar()
		self.checkbox = Checkbutton(background, text=text, bg="#36393e", activebackground="#36393e", bd=1,
									   font="Neoteric 15", fg="#9ababc", activeforeground="#9ababc",
									   selectcolor="#36393e", highlightbackground="#36393e", command=lambda: function(),
									   variable=self.isChecked, disabledforeground="#808387"
									)
		background.create_window(x, y, window=self.checkbox, anchor=NW)

		if (isChecked == True):
			self.checkbox.select()

	def setState(self, state):
		if(state == "disabled"):
			self.checkbox.config(state=DISABLED)
		elif (state == "normal"):
			self.checkbox.config(state=NORMAL)
		else:
			print("Improper state provided")


class CreateField():
	def __init__(self, x, y, name, state=True, defaultText="", charWidth=20, distance=130):
		self.name = name + ":"
		self.text = background.create_text(x, y - 3, text=self.name, font="Neoteric 15", fill="#9ababc", anchor=NW)

		self.entry = Entry(background, bg="#2f3136", fg="#9ababc", insertbackground="white", insertborderwidth=1,
						   disabledbackground="#25262b", disabledforeground="#808387", highlightthickness=0,
						   width=charWidth, font="SegoeUILight", textvariable=StringVar(root, defaultText)
						   )

		background.create_window(x + distance, y, window=self.entry, anchor=NW)

		if (state == False):
			self.setState("disabled")

	def getValue(self):
		return self.entry.get()

	def setState(self, state):
		if(state == "disabled"):
			self.entry.config(state=DISABLED, relief=FLAT)
			background.itemconfig(self.text, fill="#808387")
		elif(state == "normal"):
			self.entry.config(state=NORMAL, relief=SUNKEN)
			background.itemconfig(self.text, fill="#9ababc")
		else:
			print("Improper state provided")


class CreateButton():
	color = "#ffffff"

	def __init__(self, x, y, sizeX, sizeY, text, color, textColor, font, function):
		self.color = color

		# Create button graphic
		self.buttonBG = background.create_rectangle(x, y, x + sizeX, y + sizeY, fill=color)
		self.buttonText = background.create_text(x + sizeX/2, y + sizeY/2, text=text, fill=textColor, font=font)

		# Button Events
		background.tag_bind(self.buttonBG, "<Button-1>", self.buttonAnims)
		background.tag_bind(self.buttonText, "<Button-1>", self.buttonAnims)
		background.tag_bind(self.buttonBG, "<Enter>", self.buttonAnims)
		background.tag_bind(self.buttonText, "<Enter>", self.buttonAnims)
		background.tag_bind(self.buttonBG, "<Leave>", self.buttonAnims)
		background.tag_bind(self.buttonText, "<Leave>", self.buttonAnims)
		background.tag_bind(self.buttonBG, "<ButtonRelease-1>", self.buttonAnims)
		background.tag_bind(self.buttonText, "<ButtonRelease-1>", self.buttonAnims)

		background.tag_bind(self.buttonBG, "<Button-1>", lambda x: function())
		background.tag_bind(self.buttonText, "<Button-1>", lambda x: function())

	def buttonAnims(self, event):
		if (event.type == EventType.Enter):
			background.itemconfig(self.buttonBG, fill="#202225")
		elif (event.type == EventType.Leave):
			background.itemconfig(self.buttonBG, fill=self.color)
		elif (event.type == EventType.ButtonPress):
			background.itemconfig(self.buttonBG, fill=self.color)
		elif (event.type == EventType.ButtonRelease):
			background.itemconfig(self.buttonBG, fill="#202225")


class Program():
	def __init__(self, root):
		self.lastLocation = ""

		### Seperators and borders ###
		background.create_rectangle(padX, padY, padX + length, padY + height, fill="#36393e", width=1)
		background.create_line(padX + 10, padY + 30, padX + length - 10, padY + 30)
		background.create_line(padX + 330, padY + 30, padX + 330, padY + height - 10)

		### Text ###
		blkgen = background.create_text(mainWidth / 2, padY + 15, text="OPTIONS", font="Neoteric 20", fill="#808387",anchor=CENTER)

		### Fields ###
		self.version1 = CreateField(padX + 350, padY + 40, "Version One", True, "1.13.jar")
		self.version2 = CreateField(padX + 350, padY + 65, "Version Two", True, "1.13.1.jar")
		self.output = CreateField(padX + 350, padY + 90, "Output", True, "output.json")

		### Checkboxes ###
		self.biomes = CreateCheckbox(padX + 25, padY + 35, "Biomes", self.passFunc, False)
		self.blocks = CreateCheckbox(padX + 25, padY + 60, "Blocks", self.passFunc, False)
		self.blockstates = CreateCheckbox(padX + 25, padY + 85, "Blockstates", self.passFunc, False)
		self.entities = CreateCheckbox(padX + 25, padY + 110, "Entities", self.passFunc, False)
		self.items = CreateCheckbox(padX + 25, padY + 135, "Items", self.passFunc, False)
		self.language = CreateCheckbox(padX + 25, padY + 160, "Language", self.passFunc, False)

		self.packets = CreateCheckbox(padX + 190, padY + 35, "Packets", self.passFunc, False)
		self.recipes = CreateCheckbox(padX + 190, padY + 60, "Recipes", self.passFunc, False)
		self.sounds = CreateCheckbox(padX + 190, padY + 85, "Sounds", self.passFunc, False)
		self.stats = CreateCheckbox(padX + 190, padY + 110, "Stats", self.passFunc, False)
		self.tags = CreateCheckbox(padX + 190, padY + 135, "Tags", self.passFunc, False)
		self.tileentities = CreateCheckbox(padX + 190, padY + 160, "Tile Entities", self.passFunc, False)

		self.compare = CreateCheckbox(padX + 350, padY + 110, "Compare?", self.passFunc, True)

		### Buttons ###
		self.button = CreateButton(padX + 410, padY + height - 95, 200, 75, "GENERATE!", "#3d4046", "#9ababc","Neoteric 30", self.generate)

	def passFunc(self):
		pass

	# Checks for errors in input and returns true if so
	def errorHandling(self):
		if re.search("^\s+", self.version1.getValue()) or self.version1.getValue() == "":
			CreateMessage("Version cannot be empty or start with a space", True)
			return True
		elif not re.search("^[^/:*?\"<>|\\\]([\w]*\.?)+\.jar", self.version1.getValue()):
			CreateMessage("Version must be proper file name [\"my_file.jar\"] and cannot contain \\ / : * ? \" < > |", True)
			return True
		elif not re.search("^[^/:*?\"<>|\\\]([\w]*\.?)+\.json", self.output.getValue()):
			CreateMessage("Output must be proper file name [\"my_file.json\"] and cannot contain \\ / : * ? \" < > |", True)
			return True
		elif self.compare.isChecked.get() == 1:
			if re.search("^\s+", self.version2.getValue()) or self.version2.getValue() == "":
				CreateMessage("Version cannot be empty or start with a space", True)
				return True
			elif not re.search("^[^/:*?\"<>|\\\]([\w]*\.?)+\.jar", self.version2.getValue()):
				CreateMessage("Version must be proper file name [\"my_file.jar\"] and cannot contain \\ / : * ? \" < > |", True)
				return True

	def formatOutput(self, lines):
		linesF = []
		for s in lines:
			s = re.sub("(\s{4})*", "", s)
			s = re.sub(" *$", "", s)
			s = re.sub("[,{}\[\]]*", "", s)
			if s.find('"max_state_id"') != -1:
				continue
			elif s.find('"min_state_id"') != -1:
				continue
			elif s.find('"class"') != -1:
				continue
			elif s.find('"field"') != -1:
				continue
			elif s.find('"declared_in"') != -1:
				continue
			elif s.find('"value"') != -1:
				continue
			elif s.find('"method"') != -1:
				continue
			elif s.find('"other"') != -1:
				continue
			elif s.find('"size"') != -1:
				continue
			elif s.find('"target"') != -1:
				continue
			elif s.find('"enum_class"') != -1:
				continue
			elif s.find('"field_name"') != -1:
				continue
			elif s.find('"numeric_id"') != -1:
				continue
			elif s.find('"classes"') != -1:
				continue
			linesF.append(s)
		return linesF

	# Generates file based on input
	def generate(self):
		if(self.errorHandling()):
			return

		# Assign values
		output = self.output.getValue()
		versions = [self.version1.getValue()]
		if self.compare.isChecked.get() == 1:
			versions.append(self.version2.getValue())

		# Clear output file if it exists
		try:
			with open(output, "r+") as f:
				f.truncate(0)
		except:
			pass

		# Produce command based on selections
		try:
			os.mkdir("output")
		except:
			pass

		command = []
		topping = self.getToppings()
		if self.compare.isChecked.get() == 1:
			for i in range(2):
				try:
					with open("output/output" + str(i) + ".json", "r+") as f:
						f.truncate(0)
				except:
					pass

				command = ["python munch.py", versions[i], "--output .\\output\\output" + str(i) + ".json"]
				if topping != "":
					command.extend(["--toppings", topping])
				command = " ".join(command)
				print(command)
				sp.Popen(command)

			# Halt program to make sure files are generated
			while not os.path.isfile("output/output0.json"):
				continue
			while not os.path.isfile("output/output1.json"):
				continue
			fileSize = 0
			while fileSize <= 0:
				fileSize = os.stat("output/output0.json").st_size
				continue
			fileSize = 0
			while fileSize <= 0:
				fileSize = os.stat("output/output1.json").st_size
				continue
			time.sleep(5)
			r0F = []
			r1F = []

			with open("output/output0.json", "r+") as f:
				r = f.readlines()
				r0F = self.formatOutput(r)

			with open("output/output1.json", "r+") as f:
				r = f.readlines()
				r1F = self.formatOutput(r)

			with open(output, "w+") as f:
				out = r0F
				out.extend(r1F)
				freq = dict(Counter(out))
				outList = [keys for keys, values in freq.items() if values < 2]

				for s in outList:
					f.write(s)
		else:
			command = ["python munch.py", versions[0], "--output", output]
			if topping != "":
				command.extend(["--toppings", topping])
			command = " ".join(command)
			sp.Popen(command)

		# Run command in console
		CreateMessage("File generated successfully!", False)

	def getToppings(self):
		toppings = []
		if self.biomes.isChecked.get() == 1:
			toppings.append("biomes")
		if self.blocks.isChecked.get() == 1:
			toppings.append("blocks")
		if self.blockstates.isChecked.get() == 1:
			toppings.append("blockstates")
		if self.entities.isChecked.get() == 1:
			toppings.append("entities")
		if self.items.isChecked.get() == 1:
			toppings.append("items")
		if self.language.isChecked.get() == 1:
			toppings.append("language")
		if self.packets.isChecked.get() == 1:
			toppings.append("packets")
		if self.recipes.isChecked.get() == 1:
			toppings.append("recipes")
		if self.sounds.isChecked.get() == 1:
			toppings.append("sounds")
		if self.stats.isChecked.get() == 1:
			toppings.append("stats")
		if self.tags.isChecked.get() == 1:
			toppings.append("tags")
		if self.tileentities.isChecked.get() == 1:
			toppings.append("tileentities")
		topping = ",".join(toppings)
		return topping

# Main Program
root = Tk()

height = 250
padX = 50
padY = 50
sizeY = str(padY*2 + height)
size = str(790)+"x"+sizeY

root.title("Burger")
root.geometry(size)
root.resizable(False, False)
root.update()

# Setup global static variables
mainWidth = root.winfo_width()
mainHeight = root.winfo_height()
length = mainWidth - padX*2

# Create background
background = Canvas(root, width=mainWidth, height=mainHeight, highlightthickness=0, bg="#2f3136")
background.pack()
background.create_text(mainWidth / 2, padY / 2, text="BURGER", font="Neoteric 30", fill="#9ababc", anchor=CENTER)

# Load GUI
Program(root)

root.mainloop()