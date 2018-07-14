import json

filepath = ""  # Add here the path to the file to be parsed

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


class Territory:

    def __init__(self, startinglenght):
        self.s = Matrix.getauthorcharacter(0)*startinglenght

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

with open(filepath) as f:

    territory = 0
    matrix = Matrix()
    counter = 0

    for line in f:

        if line != "\n":

            counter += 1
            data = json.loads(line.replace("\n", ""))

            if territory == 0:
                territory = Territory(data["preDocLength"])

            if "Author" in data:
                authorid = matrix.getauthorid(data["Author"])
            else:
                authorid = 0

            start = data["preInterval"][0]
            end = data["preInterval"][1]

            for i in range(0, matrix.getauthorsnumber()):

                if i == authorid:
                    matrix.addistance(i, counter, 0)
                else:
                    matrix.addistance(i, counter, territory.getclosestdistance(matrix.getauthorcharacter(i), start, end))

            if data["opCode"] == "INS":
                territory.inscharacters(start, matrix.getauthorcharacter(authorid), data["touchedCharsLength"])
            elif data["opCode"] == "DEL":
                territory.delcharacters(start, end)
            elif data["opCode"] == "UPD":
                territory.updcharacters(start, end, matrix.getauthorcharacter(authorid))


print(matrix.lists)
