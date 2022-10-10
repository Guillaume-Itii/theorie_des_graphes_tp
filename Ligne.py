class Ligne:

    def __init__(self,args):
        print("La ligne : " + args['name'] + " à était créer")
        self._name = args['name']
        self._stations = args['stations']

    def getName(self):
        return self._name
    def getStations(self):
        return self._stations