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


def createMatrice(station_list):
    # Création de la matrice d'adjacense
    matrice = {}
    for j in range(len(station_list)):
        matrice_i = {}
        for i in range(len(station_list)):
            matrice_i[station_list[i].getName()] = None
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

    return matrice


def saveStation(column_string, station_list):
    f = open('./station.csv', 'w')
    f.write(column_string + '\n')
    for s in station_list:
        f.write(s.formatToString() + '\n')
    f.close()


def readStation():
    with open('./station.csv') as f:
        temp = f.readlines()

    station_list_string = []
    for s in temp:
        s = s.replace('\n', '')
        station_list_string.append(s)

    column_string = station_list_string[0]
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
    # print(station_list)

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
    return column, column_string, station_list


column, column_string, station_list = readStation()
while True:
    print("Saisir commannde (help : affiche l'aide) : ")
    action = input('>> ')
    station_name_list = []
    for s in station_list:
        station_name_list.append(s.getName())
    if action == "afficher":
        for s in station_list:
            print(s.showStation())
    elif action == "nouvelle":
        nom = input("Saisir un nom : ")
        while nom == '' or nom in station_name_list:
            nom = input("Saisir un nom valide : ")
        station_list.append(Station({'name': [nom], 'destination': [], 'distance': []}))
    elif action == "ajouter":
        nom_arrive, nom_depart, distance = '', '', 0
        nom_depart = input("Saisir un nom de depart: ")
        while nom_depart == '' or nom_depart not in station_name_list:
            nom_depart = input("Saisir un nom de depart valide : ")
        nom_arrive = input("Saisir un nom de arrive: ")
        while nom_arrive == '' or nom_arrive not in station_name_list:
            nom_arrive = input("Saisir un nom de arrive valide : ")
        distance = int(input("Saisir une distance : "))
        while distance == '' or 0 > distance:
            distance = int(input("Saisir une distance valide : "))
        for s in station_list:
            if nom_depart == s.getName():
                depart = s
            if nom_arrive == s.getName():
                arrive = s
        depart.addStation(arrive, distance)
    elif action == "sauvegarder":
        saveStation(column_string, station_list)
    elif action == "supprimer":
        nom = ''
        nom = input("Saisir un nom de station à supprimer : ")
        while nom == '' or nom not in station_name_list:
            nom = input("Saisir un nom de station à supprimer  : ")
        for s in station_list:
            if nom == s.getName():
                supprimer = s
        for s in station_list:
            if supprimer in s.getDestination():
                s.removeStation(supprimer)
        station_list.remove(supprimer)
    elif action == "deconnecter":
        nom_suppr,nom_target = '',''
        nom_suppr = input("Saisir un nom de station à supprimer : ")
        while nom_suppr == '' or nom_suppr not in station_name_list:
            nom_suppr = input("Saisir un nom de station à supprimer  : ")
        nom_target = input("Saisir un nom de la cible : ")
        while nom_target == '' or nom_target not in station_name_list:
            nom_target = input("Saisir un nom de la cible : ")

        for s in station_list:
            if nom_suppr == s.getName():
                supprimer = s
        for s in station_list:
            if nom_target == s.getName():
                if supprimer in s.getDestination():
                    s.removeStation(supprimer)
    elif action == "matrice":
        print(createMatrice(station_list))
    elif action == "help" or "?" :
        print("Commande dispo : ")
        print("-> afficher    : Affiche un résumer de toute les stations du réseau")
        print("-> nouvelle    : Permet de crée une nouvelle station vierge")
        print("-> ajouter     : Permet de crée un connexion unidirectionnel entre deux stations")
        print("-> supprimer   : Supprime une station ainsi que ses connections")
        print("-> deconnecter : Supprime une connection entre deux stations")
        print("-> sauvegarder : Sauvegarde l'actuelle réseau")

    else:
        for s in station_list:
            if action == s.getName():
                print(s.getName())
                print(s.getDestination())
                print(s.getDestinationString())
                print(s.getDistance())