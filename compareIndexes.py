#Compares the current files to the list of the last backup.
import os

homeDirectory = os.path.expanduser(os.path.join('~'))
os.rename(homeDirectory + "/" + ".backupManager/newIndex.xml", homeDirectory + "/" + ".backupManager/index.xml")

os.system("python fileManager.py")

