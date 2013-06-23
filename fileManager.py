#This script is reposibale for executing all actions related to managing a list of files (and directories).
import os
from bs4 import BeautifulSoup
from time import localtime

def computeDirectory(dir, homeDirectory, masterRecord):
	fileRecord = BeautifulSoup('<directory>', 'xml')
	fileRecord.directory.attrs['path'] = homeDirectory + "/" + dir
	masterRecord = fileRecord

	modifiedTag = fileRecord.new_tag('modified')	
	#modifiedTag.string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	modifiedTag.string = str(os.stat(homeDirectory + "/" + dir).st_mtime)
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
		fileTag.attrs['modified'] = str(os.stat(homeDirectory + "/" + dir).st_mtime)
		fileRecord.directory.append(fileTag)
		
	for d in directoryOnlyTree:
		#dirTag = fileRecord.new_tag('directory')
		#dirTag.attrs['path'] = fileRecord.directory.attrs['path'] + "/" + d
		#fileRecord.directory.append(dirTag)
		dirRecord = computeDirectory(d, homeDirectory + "/" + dir, masterRecord)
		fileRecord.directory.append(dirRecord)
	return fileRecord


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
	fileRecord = computeDirectory(dir, homeDirectory, None)
	fileRecords.append(fileRecord)

xmlFile = homeDirectory + "/.backupManager/newIndex.xml"
file = open(xmlFile, 'w')
for f in fileRecords:
	file.write(f.prettify())
	print("\n")
file.close()

file2 = open(xmlFile)
corrected = []
for line in file2:
	if "?xml" not in line:
		corrected.append(line)
file2.close()

file3 = open(xmlFile, 'w')
file3.write('<?xml version = "1.0" encoding = "utf-8"?>')
file3.write("\n")
for line in corrected:
	file3.write(line)
file3.write('<?/xml?>')
