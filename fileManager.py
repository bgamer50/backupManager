#This script is reposible for executing all actions related to managing a list of files (and directories).
import shutil
import os

#Records the path of the home directory, which includes the config file that says which directories to back up.
#Hopefully I'll have a nice web interface to handle creating that config file at some point.
homeDirectory = os.path.expanduser(os.path.join('~'))

directories = []
directoryFile = open(os.path.expanduser(os.path.join('~')) + "/.backupManager.config")

for line in directoryFile:
	directories.append(line.rstrip())

print(homeDirectory)
print(directories)
