import Ligne
import Station
from matplotlib import  pyplot as plt
import random

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
        if "#ligne#" in s:
            ligne_start = temp.index(s+'\n')
            break
        else:
            station_list_string.append(s)
    # ajoute les lignes a la liste de ligne
    ligne_list_string = {}
    for l in temp[ligne_start+1:]:
        l = l.replace('\n','')
        l_name = l.split(';')[0]
        temp = []
        for t in l.split(';')[1:]:
            if t != '' :
                temp.append(t)
        ligne_list_string[l_name] = temp
    print(ligne_list_string)

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
        station_list.append(Station.Station(i))
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
    ligne_list = []
    for l in ligne_list_string:
        t = []
        for s in station_list:
            if s.getName() in ligne_list_string[l]:
                t.append(s)
        ligne_list.append(Ligne.Ligne({'name':l,'stations':t}))
    return column, column_string, station_list,ligne_list


def printGraph(matrice_dict):
    x = 0
    matrice_num = []
    for j in range(len(matrice_dict)):
        temp = []
        for i in range(len(matrice_dict)):
            temp.append(None)
        matrice_num.append(temp)
    for j in matrice_dict:
        y = 0
        for i in matrice_dict[j]:
            # print(matrice_dict[j][i])
            if matrice_dict[j][i] is not None:
                matrice_num[x][y] = int(matrice_dict[j][i])
            else :
                matrice_num[x][y] = matrice_dict[j][i]
            y += 1
        x += 1
    # print(matrice_dict)
    # print(matrice_num)
    matrice_placement = []
    for j in range(len(matrice_num)):
        matrice_placement.append([random.randint(0,len(matrice_num)),random.randint(0,len(matrice_num))])
    label = []
    for i in matrice_dict:
        label.append(i)
    print(matrice_placement)
    for i in matrice_placement:
        plt.plot(i[0],i[1],marker="o",markerfacecolor="green")
        plt.text(i[0],i[1],label[matrice_placement.index(i)])
    plt.show()


def journey(matrice,depart,arrive):
    for j in matrice :
        for i in matrice[j]:
            print(matrice[j][i])

column, column_string, station_list ,ligne_list = readStation()
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
        station_list.append(Station.Station({'name': [nom], 'destination': [], 'distance': []}))
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
        print("Le réseau à bien était sauvegarder dans le CSV")
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
        matrice = createMatrice(station_list)
        print(matrice)
        # format_string = ""
        # for s in matrice :
        #     format_string += "|" + s + "|"
        # print(format_string)
        # print(type(matrice))
        # print('%-15s' % ('I am legend'))
    elif action == "ligne":
        for l in ligne_list:
            print(l.getName())
            for s in l.getStations():
                print('+->'+s.getName())
            print("==========================")
    elif action == "chemin":
        depart, arrive = '', ''
        depart = input("Saisir un nom de station de depart : ")
        while depart == '' or depart not in station_name_list:
            depart = input("Saisir un nom de station de depart  : ")
        arrive = input("Saisir un nom de station d'arriver : ")
        while arrive == '' or arrive not in station_name_list:
            arrive = input("Saisir un nom de station d'arriver : ")
        journey(createMatrice(station_list), depart, arrive)
    elif action == "graph":
        printGraph(createMatrice(station_list))

    elif action == "help" or action == "?" :
        print("Commande dispo : ")
        print("-> afficher    : Affiche un résumer de toute les stations du réseau")
        print("-> nouvelle    : Permet de crée une nouvelle station vierge")
        print("-> ajouter     : Permet de crée un connexion unidirectionnel entre deux stations")
        print("-> supprimer   : Supprime une station ainsi que ses connections")
        print("-> deconnecter : Supprime une connection entre deux stations")
        print("-> matrice     : Affiche la matrice d'adjacense")
        print("-> ligne       : Affiche les lignes de bus")
        print("-> chemin      : Donne le chemin entre deux points donner")
        print("-> sauvegarder : Sauvegarde l'actuelle réseau")

    else:
        for s in station_list:
            if action == s.getName():
                print(s.getName())
                # print(s.getDestination())
                print(s.getDestinationString())
                print(s.getDistance())