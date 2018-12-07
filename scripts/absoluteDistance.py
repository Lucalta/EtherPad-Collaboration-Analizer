import json
import os

dirinputpath = "" # Add here the path to the folder with the files to be parsed
diroutputpath = "" # Add here the path to the output folder with a "AbsTime" folder in it

class Matrix:

    @staticmethod
    def getauthorcharacter(id):
        return chr(id + ord("a"))

    def __init__(self):
        self.lists = []
        self.names = {}
        self.lastseen = {}
        self.currentauthorid = 0
        self.lists.append({"name": "anonymous", "distancelist": []})

    def setlastseen(self, authorcharacter, timestamp):
        self.lastseen[authorcharacter] = timestamp

    def getlastseen(self, authorcharacter):
        if authorcharacter in self.lastseen:
            return self.lastseen[authorcharacter]
        else:
            return -1

    def addauthor(self, authorname):
        self.currentauthorid += 1
        self.lists.append({"name": authorname, "distancelist": []})
        self.names[authorname] = self.currentauthorid
        return self.currentauthorid

    def getauthorsnumber(self):
        return len(self.lists)

    def addistance(self, authorname, line, distance):
        authorid = self.names[authorname]
        self.lists[authorid]["distancelist"].append((line, distance))

    def addistance(self, authorid, line, distance):
        self.lists[authorid]["distancelist"].append((line, distance))

    def getauthorid(self, name):
        if name in self.names:
            return self.names[name]
        else:
            return self.addauthor(name)

    def printtofile(self, outputpath):
        with open(outputpath, "w+") as f:
            for x in self.lists:
                line = x["distancelist"][0][0]
                if line > 1:
                    f.write("-1")
                if line > 2:
                    f.write(",-1" * (line-2))
                counter = 0
                while line <= x["distancelist"][-1][0]:
                    if line > 1:
                        f.write(",")
                    f.write(str(x["distancelist"][counter][1]))
                    line += 1
                    counter += 1
                f.write("\n")


def takesecond(elem):
    return elem['Timestamp']


def elaboratefile(filepath, outputpath):

    edits = []

    with open(filepath) as f:
        for line in f:
            if line != "\n":
                edits.append(json.loads(line.replace("\n", "")))

    edits.sort(key=takesecond)

    timematrix = Matrix()
    counter = 0

    for data in edits:

        if data != "\n":

            counter += 1

            if "Author" in data:
                authorid = timematrix.getauthorid(data["Author"])
            else:
                authorid = 0

            timestamp = round(int(data["Timestamp"])/1000)

            for i in range(0, timematrix.getauthorsnumber()):
                if i == authorid:
                    timematrix.addistance(i, counter, 0)
                else:
                    timestamp2 = timematrix.getlastseen(timematrix.getauthorcharacter(i))
                    if timestamp2 == -1:
                        distance = -1
                    else:
                        distance = timestamp - timestamp2
                    timematrix.addistance(i, counter, distance)

            timematrix.setlastseen(timematrix.getauthorcharacter(authorid), timestamp)

    timematrix.printtofile(outputpath.replace(".txt", ".csv"))


for filename in os.listdir(dirinputpath):
    elaboratefile(os.path.join(dirinputpath, filename), os.path.join(diroutputpath, "AbsTime", filename))
