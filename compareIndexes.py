#Compares the current files to the list of the last backup.
#Unfinished, test only
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

#Retrieves info from index files.
def retrieveInfo(readIndex):
	dirList = {}

	dirpaths = [] #Used as a stack.
	index = 0
	while index < len(readIndex):
		line = readIndex[index].rstrip()
		if line == "d":
			index += 1
			dirpaths.append(readIndex[index].rstrip())
			if readIndex[index].rstrip() not in dirList:
				dirList[readIndex[index].rstrip()] = []
		elif line == "ed":
			dirpaths.pop()
		elif line == "f":
			index += 1
			newfile = file(readIndex[index].rstrip(), readIndex[index + 1].rstrip())
			index += 1
			dirList[dirpaths[len(dirpaths) - 1]].append(newfile)	
		index += 1
	return dirList

mainIndex = open(oldIndexPath).readlines()
prevIndex = open(newIndexPath).readlines()
currentDirList = retrieveInfo(mainIndex)
previousDirList = retrieveInfo(prevIndex)
#for d in currentDirList:
#       print(d + " {")
#       for f in currentDirList[d]:
#               print(f.name + " " + f.modified)
#       print("}")
