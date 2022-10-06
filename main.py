class Station:
    def __init__(self, args):
        self._name = args['name'][0]
        self._destinationString = args['destination']
        self._distance = args['distance']
        self._destination = None

    def setDestination(self,d):
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


with open('./station.csv') as f:
    temp = f.readlines()

station_list_string = []
for s in temp:
    s = s.replace('\n', '')
    station_list_string.append(s)

# Recup les noms de colonne
column = station_list_string.pop(0).split('#')
for i in range(len(column)):
    column[i] = column[i].split(';')
    for j in column[i]:
        if j != '':
            column[i] = j
# print(column)
# print(station_list_string)

for j in range(len(station_list_string)):
    s = station_list_string[j].split('#')
    t = {}
    for i in range(len(s)):
        t[column[i]] = s[i]
    station_list_string[j] = t

# print(station_list_string)
for j in range(len(station_list_string)):
    # print(station_list_string[j])
    d = {}
    for col_name in column:
        t = []
        # print(col_name)
        for i in station_list_string[j][col_name].split(';'):
            if i != '':
                t.append(i)
        d[col_name] = t
    station_list_string[j] = d
# print(station_list_string)
station_list = []
for i in station_list_string:
    station_list.append(Station(i))

for s in range(len(station_list)):
    # print('station : ' + station_list[s].getName())
    t = []
    for j in station_list[s].getDestinationString():
        for i in range(len(station_list)):
            if station_list[i].getName() == j:
                t.append(station_list[i])
                # print(j)
    station_list[s].setDestination(t)
    # print('nom' + station_list[i].getName())

# print("==============================")
# for s in station_list:
    # print(s.getName())
    # print(s)
    # print("destination")
    # print(s.getDestination())

matrice = {}
for j in range(len(station_list)):
    matrice_i = {}
    for i in range(len(station_list)):
        matrice_i[station_list[i].getName()]=None
    matrice[station_list[j].getName()] = matrice_i
# print(matrice)


for j in range(len(station_list)):
    for i in range(len(station_list)):
        if station_list[j].getName() != station_list[i].getName():
            # print('j : ' + station_list[j].getName())
            # print('i : ' + station_list[i].getName())
            if station_list[i] in station_list[j].getDestination():
                k = station_list[j].getDestination().index(station_list[i])
                # print(station_list[j].getDistance(k))
                matrice[station_list[j].getName()][station_list[i].getName()] = station_list[j].getDistance(k)

print(matrice)