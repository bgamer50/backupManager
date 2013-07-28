#This file will back up everything via FTP.
from ftplib import FTP
import os
import cPickle

def retrieveData(homeDirectory):
    dataFile = open(homeDirectory + "/.backupManager/info", "rb")
    return cPickle.load(dataFile)

def uploadFile(name, path, ftp):
    file = open(path, "rb")
    ftp.storbinary("STOR " + name)
    file.close()

homeDirectory = os.path.expanduser(os.path.join('~'))
configFile = open(homeDirectory + "/.backupManager/FTP.config")
url = configFile.readline().rstrip()
username = configFile.readline().rstrip()
password = configFile.readline().rstrip()
email = configFile.readline().rstrip()

ftp = FTP(url)
ftp.login(username, password)

data = retrieveData(homeDirectory)
for d in data:
    print(d + ":")
    ftp.cwd("~")
    try:
        ftp.cwd(d)
    except:
        ftp.mkd(d)
        ftp.cwd(d)
    for f in data[d]:
        print(f.name + "\n" + f.modified + "\n\n")
        uploadFile(f.name, homeDirectory + "/" + d, ftp)