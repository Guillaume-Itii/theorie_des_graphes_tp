class Station:
    def __init__(self, args):
        print('Création de la station : ' + str(args))
        self._name = args['name'][0]
        self._destinationString = args['destination']
        self._distance = args['distance']
        self._destination = []

    def setDestination(self, d):
        self._destination = d

    def getName(self):
        return self._name

    def getDestinationString(self, index=None):
        if index is None:
            return self._destinationString
        else:
            return self._destinationString[index]

    def getDestination(self, index=None):
        if self._destination is None:
            print('No route set yet')
            return False
        if index is None:
            return self._destination
        else:
            return self._destination[index]

    def getDistance(self, index=None):
        if index is None:
            return self._distance
        else:
            return self._distance[index]

    def addStation(self, s, d):
        print("La station : " + s.getName() + " à était ajouter à : " + self._name + " avec une distance de " + str(d))
        # print(self)
        # print(s)
        self._destination.append(s)
        self._destinationString.append(s.getName())
        self._distance.append(str(d))

    def removeStation(self,s):
        print(s.getName() + " à était supprimer de : " + self._name)
        self._distance.pop(self._destination.index(s))
        self._destination.remove(s)

    def formatToString(self):
        s = self._name + ";#;"
        for i in self._destination:
            s += i.getName() + ';'
        s += '#;'
        for i in self._distance:
            s += i + ';'
        s = s[:-1]

        return s

    def showStation(self):
        temp = []
        temp.append("Station : " + self._name + "\n")
        temp.append("Destination : \n")
        for i in range(len(self._destination)):
            temp.append('   ' + self._destination[i].getName() + " : " + self._distance[i] + '\n')
        s = ''
        for i in range(len(temp[-1])):
            s += '='
        temp.append(s)
        s = ""
        for i in temp:
            s += i
        return s
