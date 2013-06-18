#This script is reposible for executing all actions related to managing a list of files (and directories).
import shutil
import os
from bs4 import BeautifulSoup

#Records the path of the home directory, which includes the config file that says which directories to back up.
#Then accesses the config file and makes a list of which directories will be backed up.
#Hopefully I'll have a nice web interface to handle creating that config file at some point.
homeDirectory = os.path.expanduser(os.path.join('~'))

directories = []
directoryFile = open(homeDirectory + "/.backupManager/directories.list")

for line in directoryFile:
	directories.append(line.rstrip())
fileRecords = []

#Build XML
for dir in directories:
	fileRecord = BeautifulSoup('<directory>', 'xml')
	fileRecord.directory.attrs['path'] = homeDirectory + "/" + dir
	
	modifiedTag = fileRecord.new_tag('modified')	
	modifiedTag.string = "01-01-1970 0:00"
	fileRecord.directory.append(modifiedTag)
	
	#Add files and subdirs to XML
	fileTree = os.listdir(fileRecord.directory.attrs['path'])
	fileOnlyTree = []
	for (dirpath, dirnames, filenames) in os.walk(fileRecord.directory.attrs['path']):
		fileOnlyTree.extend(filenames)
		break
	directoryOnlyTree = list(set(fileTree) - set(fileOnlyTree))

	for f in fileOnlyTree:
		fileTag = fileRecord.new_tag('file')
		fileTag.string = f
		fileRecord.directory.append(fileTag)
		
	for d in directoryOnlyTree:
		dirTag = fileRecord.new_tag('directory')
		dirTag.attrs['path'] = fileRecord.directory.attrs['path'] + "/" + d
		fileRecord.directory.append(dirTag)

	fileRecords.append(fileRecord)

for f in fileRecords:
	print(f.prettify())
	print("\n")

