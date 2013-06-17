#This class is reposible for executing all actions related to managing a list of files (and directories).
import shutil
import os
homeDirectory = os.path.expanduser(os.path.join('~'))
directories = []
directories.add("Documents")
print(homeDirectory)

