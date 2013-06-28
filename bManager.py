from Tkinter import *
import compareIndexes
import os

#This script handles the GUI.  The user can choose which directories to back up and then start the indexing process.
#At the moment, the actual backup is not handled yet by this program.

homeDirectory = os.path.expanduser(os.path.join('~'))

class mainWindow(Frame):
	varList = {}
	def callback(self):
		listFile = open(homeDirectory + "/" + ".backupManager/directories.list", "w")
		for v in self.varList:
			if self.varList[v].get() == 1:
				listFile.write(v + "\n")
		compareIndexes
		exit()

	def __init__(self, parent, directories):
		Frame.__init__(self, parent, background = "gray")
		self.parent = parent

		self.parent.title("Backup Manager")
		self.pack(fill = BOTH, expand = 1)
		#self.varList = {}
		self.buttonVar = IntVar()		

		indexY = 0
		indexX = 0
		for d in directories:
			self.varList[d] = IntVar()
			cb = Checkbutton(self, text = d, variable = self.varList[d])
			cb.select()
			cb.place(x = 50 + 200 * indexX, y = 50 + 30 * indexY)
			if 50 + 30 * indexY > 400:
				indexY = -1
				indexX += 1
			indexY += 1
		button = Button(parent, text = "Start Backup", command = self.callback)
		button.place(x = 520, y = 400)

fileTree = os.listdir(homeDirectory)
fileOnlyTree = []
for(dirpath, dirnames, filenames) in os.walk(homeDirectory):
	fileOnlyTree.extend(filenames)
	break
directoryOnlyTree = list(set(fileTree) - set(fileOnlyTree))
for d in directoryOnlyTree:
	if d[0] == ".":
		directoryOnlyTree.remove(d)
directoryOnlyTree.remove(".backupManager")

root = Tk()
root.geometry("640x480+300+300")
app = mainWindow(root, directoryOnlyTree)
root.mainloop()
