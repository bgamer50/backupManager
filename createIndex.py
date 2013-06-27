#This script is reposibale for executing all actions related to managing a list of files (and directories).
#Should be complete now.
import os
from time import localtime
from sys import argv

def computeDirectory(dirPath, indexFile):
	fileTree = os.listdir(dirPath)
	fileOnlyTree = []
	for(dirpath, dirnames, filenames) in os.walk(dirPath):
		fileOnlyTree.extend(filenames)
		break
	directoryOnlyTree = list(set(fileTree) - set(fileOnlyTree))

	for f in fileOnlyTree:
		indexFile.write("f" + "\n") #File
		indexFile.write(f + "\n")
		indexFile.write(str(os.stat(dirPath + "/" + f).st_mtime) + "\n") #File modified time
		indexFile.write("ef" + "\n") #End File
	
	for d in directoryOnlyTree:
		indexFile.write("d" + "\n") #Directory
		indexFile.write(dirpath + "/" + d + "\n")
		computeDirectory(dirPath + "/" + d, indexFile)
		indexFile.write("ed" +  "\n") #End Directory

#Records the path of the home directory, which includes the config file that says which directories to back up.
#Then accesses the config file and makes a list of which directories will be backed up.
#Hopefully I'll have a nice web interface to handle creating that config file at some point.
homeDirectory = os.path.expanduser(os.path.join('~'))

directories = []
directoryFile = open(homeDirectory + "/.backupManager/directories.list")

for line in directoryFile:
	directories.append(line.rstrip())

#Build Index File
indexFilePath = homeDirectory + "/.backupManager/" + argv[1]
indexFile = open(indexFilePath, "w")
for dir in directories:
	indexFile.write("d" + "\n") #Directory
	indexFile.write(homeDirectory + "/" + dir + "\n")
	computeDirectory(homeDirectory + "/" + dir, indexFile)
	indexFile.write("ed" + "\n") #End Directory
