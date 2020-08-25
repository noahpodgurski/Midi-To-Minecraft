import mido
from tkinter import *
import pyautogui
import time
import pdb

tracks = []
divider = 1
lowestNote = float('inf')
highestNote = float('-inf')

class Note:
	def __init__(self, note, noteLetter, duration):
		self.note = note
		self.noteLetter = noteLetter
		self.duration = duration
		self.on = 1

	def setDuration(self, value):
		self.duration = value

	def setOn(self, value):
		self.on = value

	def getOn(self):
		return self.on

	def getNote(self):
		return self.note


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

def toLetter(note):
	if note%12 == 0:
		return "C"
	elif note%12 == 1:
		return "C#"
	elif note%12 == 2:
		return "D"
	elif note%12 == 3:
		return "D#"
	elif note%12 == 4:
		return "E"
	elif note%12 == 5:
		return "F"
	elif note%12 == 6:
		return "F#"
	elif note%12 == 7:
		return "G"
	elif note%12 == 8:
		return "G#"
	elif note%12 == 9:
		return "A"
	elif note%12 == 10:
		return "A#"
	elif note%12 == 11:
		return "B"
	raise ValueError("Incorrect value passed to toLetter function")

def toMCClicks(note, octave=0):
	global lowestNote, highestNote
	note += (12*octave)
	return (note + 6)%24

def parse3():
	global lowestNote, highestNote
	lowestTick = float('inf')
	# for i in range(1): #need to corrently determine what tracks are and what they mean
	for track in mid.tracks:
		notes = []
		for msg in track:
			while msg.time >= 1:
				msg.time /= 2
			note = msg.bytes()[1]
			if msg.type == "note_on" and msg.velocity != 0:
				#NOTE ON
				#add current time to last note
				# print(f"starting time of next note is {round(msg.time*4)/4}")
				if len(notes) > 0:
					# print(f"NOTE OFF, ADDING {notes[-1].duration} to {(round(msg.time*4)/4)} on {notes[-1].noteLetter}")
					notes[-1].setDuration(notes[-1].duration+(round(msg.time*4)/4))
					# print(f"setting duration of {notes[-1].noteLetter} to {notes[-1].duration}")

			if (msg.type == "note_on" and msg.velocity == 0) or msg.type == "note_off":
				#note turned off, add new note object to list
				# print(round(msg.time*4)/4)
				noteLetter = toLetter(note)
				notes.append(Note(note, noteLetter, round(msg.time*4)/4))
				# print(f"NOTE OFF, NEW NOTE: {noteLetter} with a ENDING duration of : {msg.time}")
		tracks.append(notes)

	# avg = 0
	# c = 0
	# for track in tracks:
	# 	for note in track:
	# 		avg += note.duration
	# 		c += 1
	# if c != 0:
	# 	avg /= c
	# print(f"the avg tick was {avg}")

	# while lowestTick > 1:
	# 	for track in tracks:
	# 		for note in track:
	# 			note.logDuration(10)
	# 	lowestTick /= 10
	print(f"The lowest tick was {lowestTick}")

def adjustTimes(limit=1):
	global divider
	sumo = 0
	count = 0
	for track in mid.tracks:
		for msg in track:
			if msg.type == "note_on" or msg.type == "note_off":
				sumo += round(msg.time*4)/4
				count += 1
	avg = sumo/count
	print("AVERAGE:")
	print(avg)
	while avg >= limit:
		avg /= 10
		divider *= 10
	print(divider)

def parse4():
	global lowestNote, highestNote
	lowestTick = float('inf')
	# for i in range(1): #need to corrently determine what tracks are and what they mean
	for track in mid.tracks:
		notes = []
		for i in range(len(track)):
			msg = track[i]
			msg.time /= divider


			# print(msg)
			if msg.type == "note_on":
				if len(notes) > 0:
					notes[-1].setDuration(notes[-1].duration+(round(msg.time*4)/4))
					print(f"{notes[-1].noteLetter} played for {notes[-1].duration}?")
				
				note = msg.bytes()[1]
				noteLetter = toLetter(note)
				notes.append(Note(note, noteLetter, 0))
				#add current time to previous note
				
			if msg.type == "note_off":
				if len(notes) > 0:
					# print("here")
					for i in range(len(notes)-1, -1, -1):
						# print("notes[i].note")
						if notes[i].note == note and notes[i].getOn() == 1:
							notes[i].setOn(0)
							notes[i].setDuration(notes[i].duration+(round(msg.time*4)/4))
							# print(f"{notes[i].noteLetter} NOTE OFF {notes[i].duration}?")
		tracks.append(notes)

def parse5():
	global lowestNote, highestNote
	lowestTick = float('inf')
	# for i in range(1): #need to corrently determine what tracks are and what they mean
	for track in mid.tracks:
		notes = []
		i = 0
		while i < len(track):
			track[i].time /= divider
			chord = []
			j = 1
			# pdb.set_trace()
			if j < len(track) and track[i].type == "note_on":
				# get ON chords
				while i+j < len(track) and track[i+j].type == "note_on" and track[i+j].time == 0:
					note = track[i+j].bytes()[1]
					noteLetter = toLetter(note)
					chord.append(Note(note, noteLetter, 0))
					chord[-1].setDuration(chord[-1].duration+(round(track[i].time*4)/4))
					# print(f"{noteLetter} is part of a chord!")
					# i += 1
					j += 1



			if len(chord) != 0: #we have a chord
				# chords.append(Chord(chord))
				#add first note
				note = track[i].bytes()[1]
				noteLetter = toLetter(note)
				chord.append(Note(note, noteLetter, 0))
				chord[-1].setDuration(chord[-1].duration+(round(track[i].time*4)/4))
				# print(f"{noteLetter} is part of a chord!")
				i += len(chord)-1
				notes.append(chord)
			elif len(chord) == 0 and track[i].type == "note_on": #no chord
				if len(notes) > 0 and type(notes[-1]) != list:
					notes[-1].setDuration(notes[-1].duration+(round(track[i].time*4)/4))
					print(f"{notes[-1].noteLetter} played for {notes[-1].duration}?")
				
				note = track[i].bytes()[1]
				noteLetter = toLetter(note)
				notes.append([Note(note, noteLetter, 0)])
				#add current time to previous note

			if track[i].type == "note_off":
				# if len(notes) > 0:
				if True:
					note = track[i].bytes()[1]
					noteLetter = toLetter(note)

					if len(notes) > 0:				
						for k in range(len(notes)-1, -1, -1):
							if type(notes[k]) == list:
								for n in notes[k]:
									if n.note == note and n.getOn() == 1:
										n.setOn(0)
										n.setDuration(n.duration+(round(track[i].time*4)/4))
										# break
							# elif type(notes[k]) == Note and notes[k].note == note and notes[k].getOn() == 1:
							# 	notes[k].setOn(0)
							# 	notes[k].setDuration(notes[k].duration+(round(track[i].time*4)/4))
							# 	break
			i += 1
		tracks.append(notes)
	
	# for chord in chords:
	# 	for note in chord.notes:
	# 		print(f"{note.noteLetter} is inside a chord!")

def printData():
	for track in tracks:
		for note in track:
			if type(note) == list:
				for n in note:
					print(f"{n.note} ({n.noteLetter}) played for a duration of {n.duration} seconds!")
			print("=========")
		# print(f"{notes[i].note} ({notes[i].noteLetter}) played from {(notes[i].start)} to {notes[i].end}")

	# print(f"the highest note was {highestNote} ({toLetter(highestNote)})")
	# print(f"the lowest note was {lowestNote} ({toLetter(lowestNote)})")

def toString():
	global lowestNote, highestNote

	if highestNote-lowestNote > 24:
		print("Extends beyond 2 octaves")
	mid = ""
	for track in tracks:
		for note in track:
			if type(note) == list:
				for n in note:
					clicks = toMCClicks(n.note, octave=-1)
					if clicks < 10:
						clicks = "0"+str(clicks)
					mid += f"|{clicks}|{'-'*int(n.duration*tempo)}"
					# bot += f"|{n.nLetter}|{'-'*int(n.duration*tempo)}"
			elif type(note) == Note:	
				clicks = toMCClicks(note.note, octave=-1)
				# rightClick(clicks)
				# print(f"Note: {note.noteLetter}")
				# time.sleep(1)
				if clicks < 10:
					clicks = "0"+str(clicks)
				# top += f"_{'_'*len(str(clicks))}_{' '*int(note.duration*tempo)}"
				mid += f"|{clicks}|{'-'*int(note.duration*tempo)}"
				# bot += f"|{note.noteLetter}|{'-'*int(note.duration*tempo)}"


		mid += "\n"

	# print(top)
	print(mid)
	# print(bot)

def toCheckBoxes():
	root = Tk()
	x = []
	for track in tracks:
		y = []
		for note in track:
			y.append(toMCClicks(note.note, -1))
		x.append(y)
	for y in x:
		lng = Checkbar(root, y)
		lng.pack(side=TOP,  fill=X)
		lng.config(relief=GROOVE, bd=2)

	def allstates(): 
		print(list(lng.state()))
	Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
	Button(root, text='Peek', command=allstates).pack(side=RIGHT)
	root.mainloop()

def clearExcessiveTracks():
	for i in range(len(tracks)-1):
		different = 0
		for j in range(i+1, len(tracks)):
			if len(tracks[i]) == len(tracks[j]):
				for x in range(len(tracks[i])):
					if tracks[i][x].note != tracks[j][x].note:
						different = 1
						break
			if different == 0:
				tracks[i] = []
				print("clearing a track")

def rightClick(note):
	for i in range(note):
		pyautogui.click(button="right")
		# pyautogui.press('enter')
		# pyautogui.write("hello")
		# pyautogui.press('enter')

	# pyautogui.mouseDown(button="right")
	# pyautogui.mouseUp(button="right")

def goUp(direction="-Z", octave=0, LIMIT=20):
	global x, y, z
	if direction == "-Z":
		pyautogui.write(f"fill {x-2} {y} {z} {x-2} {y} {z} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+1} {z+1} {x-2} {y} {z+1} minecraft:black_concrete")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-2} {y+1} {z+1} {x-2} {y+1} {z+1} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+2} {z+1} {x-1} {y+2} {z+1} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+2} {z-LIMIT*3} {x-2} {y+2} {z} minecraft:black_concrete")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+3} {z} {x-2} {y+3} {z} minecraft:redstone_wire")
		pyautogui.press('enter')
		z -= 2
	elif direction[-1] == "Z": #or --Z
		pyautogui.write(f"fill {x-2} {y} {z+1} {x-2} {y} {z+1} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+1} {z} {x-2} {y} {z} minecraft:black_concrete")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-2} {y+1} {z} {x-2} {y+1} {z} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+2} {z} {x-1} {y+2} {z} minecraft:redstone_wire")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+2} {z+1+LIMIT*3} {x-2} {y+2} {z+1} minecraft:black_concrete")
		pyautogui.press('enter')
		pyautogui.write(f"fill {x-1} {y+3} {z+1} {x-2} {y+3} {z+1} minecraft:redstone_wire")
		pyautogui.press('enter')
		z += 2

	y += 3
	return direction

def toMinecraft(direction="Z", octave=0):
	global x, y, z
	LIMIT = 20
	for track in tracks:
		count = 0
		# if direction == "Z":
		for notes in track:
			#keep from going in a complete straight line
			# count += 1
			# if count % LIMIT == 0:
			# 	#go up, and switch direction
			# 	direction = goUp("-"+direction, tempo, octave, LIMIT)
			# 	input(f"Hit enter to continue ({count/len(track)}% complete)")
			# 	time.sleep(1.5)
			xOffset = 4
			for index, note in enumerate(notes):
			
				#convert to clicks
				duration = int(note.duration*tempo)
				clicks = toMCClicks(note.note, octave)
				# if duration != 0:
				if True:
					
					#add noteblock
					pyautogui.write(f"fill {x-xOffset} {y} {z+2} {x-xOffset} {y} {z+2} minecraft:note_block[instrument=flute, note={clicks}]")
					pyautogui.press('enter')
					#add redstone leading to noteblock and main circuit
					pyautogui.write(f"fill {x-xOffset} {y} {z+1} {x-xOffset} {y} {z+1} minecraft:redstone_wire") #redstone
					pyautogui.press('enter')
					xOffset += 2

			#add connecting redstone
			pyautogui.write(f"fill {x-2} {y} {z} {x-2-len(notes)*2} {y} {z} minecraft:redstone_wire")
			pyautogui.press('enter')

			#add repeater with delay
			pyautogui.write(f"fill {x-2} {y} {z+1} {x-2} {y} {z+1} minecraft:repeater[facing=north, delay={duration}]") #repeater
			pyautogui.press('enter')
			z += 2	
			#add repeaters with extra delay
			if duration > 4:		
				while duration > 4:
					pyautogui.write(f"fill {x-2} {y} {z-1} {x-2} {y} {z-1} minecraft:repeater[facing=north, delay=4]")
					pyautogui.press('enter')
					duration -= 4
					z += 1
				pyautogui.write(f"fill {x-2} {y} {z-1} {x-2} {y} {z-1} minecraft:repeater[facing=north, delay={duration}]")
				pyautogui.press('enter')
			# at the end of chord, add 2 to z and 2 redstone dust to give room for chord
			# if index+1 < len(notes) and len(notes[index+1]) > 1: #if next note is a chord
			if True: #is chord
				pyautogui.write(f"fill {x-2} {y} {z} {x-2} {y} {z+1} minecraft:redstone_wire")
				pyautogui.press('enter')
				z += 2

			# elif direction == "-Z":
			# 	#add noteblock
			# 	pyautogui.write(f"fill {x} {y} {z} {x} {y} {z} minecraft:note_block[instrument=flute, note={clicks}]")
			# 	pyautogui.press('enter')
			# 	#add redstone leading to noteblock and main circuit
			# 	pyautogui.write(f"fill {x-1} {y} {z} {x-2} {y} {z} minecraft:redstone_wire") #redstone
			# 	pyautogui.press('enter')
			# 	#add repeater with delay
			# 	pyautogui.write(f"fill {x-2} {y} {z+1} {x-2} {y} {z+1} minecraft:repeater[facing=south, delay={duration}]") #repeater
			# 	pyautogui.press('enter')
			# 	z -= 2	
			# 	#add repeaters with extra delay
			# 	if duration > 4:		
			# 		while duration > 4:
			# 			pyautogui.write(f"fill {x-2} {y} {z-1} {x-2} {y} {z-1} minecraft:repeater[facing=south, delay=4]")
			# 			pyautogui.press('enter')
			# 			duration -= 4
			# 			z -= 1
			# 		pyautogui.write(f"fill {x-2} {y} {z-1} {x-2} {y} {z-1} minecraft:repeater[facing=south, delay={duration}]")
			# 		pyautogui.press('enter')

def restart():
	global x, y, z
	for i in range(0, 601, 100):
		pyautogui.write(f"fill {x} {y} {z+i} {x-12} {y+10} {z+i+100} minecraft:air")
		pyautogui.press('enter')


mid = mido.MidiFile("russia.mid")
# mid = mido.MidiFile("kirbymelody.mid")
print(mid)
print(f"{mid.tracks[0]} midi tracks detected")

for track in mid.tracks:
	print("NEW TRACK")
	for event in track:
		print(event)



x = -246
y = 4
z = -32
tempo = 4
if __name__ == '__main__':

	time.sleep(2)
	adjustTimes(1)
	# parse4()
	parse5()
	printData()
	toString()
	
	#####WILL WRITE######
	restart()
	toMinecraft("Z", octave=0)
	#####WILL WRITE######

	print("DONE")

"""
TYPES:
type 0 (single track): all messages are saved in one track
type 1 (synchronous): all tracks start at the same time
type 2 (asynchronous): each track is independent of the others

DAY 4, Captain's Log,
i think that the length of the note is not being properly determined by the time,
it seems like the note before gets the duration of the note after it



melee.mid
<midi file 'melee.mid' type 1, 2 tracks, 191 messages>
<meta message set_tempo tempo=461538 time=0>
<meta message time_signature numerator=4 denominator=4 clocks_per_click=24 notated_32nd_notes_per_beat=8 time=0>
<meta message end_of_track time=0>

MARY2.MID
<midi file 'mary2.mid' type 1, 4 tracks, 168 messages>
<meta message set_tempo tempo=461538 time=0>
<meta message time_signature numerator=4 denominator=4 clocks_per_click=24 notated_32nd_notes_per_beat=8 time=0>
<meta message end_of_track time=0>



"""