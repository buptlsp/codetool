import os

def file_get_content(file):
    fd = open(file, "r")
    string = fd.read()
    fd.close()
    return string
def file_put_content(file, string, createDir=True):
    dirPath = os.path.dirname(file)
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)
    fd = open(file, "w")
    fd.write(string)
    fd.close()


