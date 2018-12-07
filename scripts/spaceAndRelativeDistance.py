import json
import os

dirinputpath = "" # Add here the path to the folder with the files to be parsed
diroutputpath = "" # Add here the path to the output folder with a "Space" and "Time" folder in it

class Matrix:

    @staticmethod
    def getauthorcharacter(id):
        return chr(id + ord("a"))

    def __init__(self):
        self.lists = []
        self.names = {}
        self.currentauthorid = 0
        self.lists.append({"name": "anonymous", "distancelist": []})

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


class Territory:

    def __init__(self, startinglenght):
        self.s = Matrix.getauthorcharacter(0)*startinglenght
        self.time = 0

    def getclosestdistance(self, character, firstposition, secondposition):
        if self.s[firstposition-1:secondposition-1].find(character) != -1:
            return 0
        x = self.s[secondposition-1:].find(character)
        y = self.s[:firstposition-1][::-1].find(character)

        if x == -1 and y == -1:
            return -1
        elif x == -1:
            return y+1
        elif y == -1:
            return x+1
        else:
            return min(x, y) + 1

    def inscharacters(self, position, character, n):
        # print(self.s[:position-1] + "|" + character * n + "|" + self.s[position-1:])
        self.s = self.s[:position-1] + character * n + self.s[position-1:]

    def delcharacters(self, start, end):
        # print(self.s[:start-1] + "|" + self.s[end-1:])
        self.s = self.s[:start-1] + self.s[end-1:]

    def updcharacters(self, start, end, character):
        # print(self.s[:start - 1] + "|" + character * (end - start) + "|" + self.s[end - 1:])
        self.s = self.s[:start-1] + character*(end-start) + self.s[end-1:]

    def instime(self, character):
        self.time += 1
        self.inscharacters(self.time, character, 1)


def takesecond(elem):
    return elem['Timestamp']


def elaboratefile(filepath, spaceoutputpath, timeoutputpath):

    edits = []
    with open(filepath) as f:
        for line in f:
            if line != "\n":
                edits.append(json.loads(line.replace("\n", "")))

    edits.sort(key=takesecond)

    spaceterritory = 0
    spacematrix = Matrix()
    timeterritory = Territory(0)
    timematrix = Matrix()
    counter = 0

    for data in edits:

        if data != "\n":

            counter += 1

            if spaceterritory == 0:
                spaceterritory = Territory(data["preDocLength"])

            if "Author" in data:
                spacematrix.getauthorid(data["Author"])
                authorid = timematrix.getauthorid(data["Author"])
            else:
                authorid = 0

            start = data["preInterval"][0]
            end = data["preInterval"][1]

            for i in range(0, spacematrix.getauthorsnumber()):

                if i == authorid:
                    spacematrix.addistance(i, counter, 0)
                    timematrix.addistance(i, counter, 0)
                else:
                    spacematrix.addistance(i, counter, spaceterritory.getclosestdistance(spacematrix.getauthorcharacter(i), start, end))
                    timematrix.addistance(i, counter, timeterritory.getclosestdistance(timematrix.getauthorcharacter(i), counter, counter))

            timeterritory.instime(spacematrix.getauthorcharacter(authorid))

            if data["opCode"] == "INS":
                spaceterritory.inscharacters(start, spacematrix.getauthorcharacter(authorid), data["touchedCharsLength"])
            elif data["opCode"] == "DEL":
                spaceterritory.delcharacters(start, end)
            elif data["opCode"] == "UPD":
                spaceterritory.updcharacters(start, end, spacematrix.getauthorcharacter(authorid))

    timematrix.printtofile(timeoutputpath.replace(".txt", "##" + str(len(timeterritory.s)) + "##.csv"))
    spacematrix.printtofile(spaceoutputpath.replace(".txt", "##" + str(len(spaceterritory.s)) + "##.csv"))

for filename in os.listdir(dirinputpath):
    elaboratefile(os.path.join(dirinputpath, filename), os.path.join(diroutputpath, "Space", filename), os.path.join(diroutputpath, "Time", filename))
