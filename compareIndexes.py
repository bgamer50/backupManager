#Compares the current files to the list of the last backup.
#Unfinished
import os

homeDirectory = os.path.expanduser(os.path.join('~'))
oldIndexPath = homeDirectory + "/" + ".backupManager/main.index"
newIndexPath = homeDirectory + "/" + ".backupManager/main_old.index"

os.rename(oldIndexPath, newIndexPath)
os.system("python createIndex.py main.index")

#This is the part where I go through the xml files and create an array of file paths that need to be backed up.
#This begins with creating a file class that holds file info.
class file:
	name = ""
	modified = 0.0
	def __init__(self, n, m):
		self.name = n
		self.modified = m

mainIndex = open(oldIndexPath).readlines()
prevIndex = open(newIndexPath)

currentDirList = {}

dirpaths = [] #Used as a stack.
index = 0
while index < len(mainIndex):
	line = mainIndex[index].rstrip()
	if line == "d":
		index += 1
		dirpaths.append(mainIndex[index].rstrip())
		if mainIndex[index].rstrip() not in currentDirList:
			currentDirList[mainIndex[index].rstrip()] = []
	elif line == "ed":
		dirpaths.pop()
	elif line == "f":
		index += 1
		newfile = file(mainIndex[index].rstrip(), mainIndex[index + 1].rstrip())
		index += 1
		currentDirList[dirpaths[len(dirpaths) - 1]].append(newfile)	
	index += 1

for d in currentDirList:
	print(d + " {")
	for f in currentDirList[d]:
		print(f.name + " " + f.modified)
	print("}")
