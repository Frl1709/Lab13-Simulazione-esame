import copy

import networkx as nx
from geopy import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listYears = []
        self.listShapes = []
        self.listStates = []

        self._graph = nx.Graph()
        self._nodes = []
        self._edges = []

        self.idMap = {}

        self.bestPath = []
        self.bestWeight = 0

        self.load_listYears()
        self.load_listShapes()
        self.load_listStates()

    def load_listStates(self):
        self.listStates = DAO.getStates()

    def load_listYears(self):
        self.listYears = DAO.getYears()

    def load_listShapes(self):
        self.listShapes = DAO.getShapes()

    def buildGraph(self, forma, anno):
        self._graph.clear()

        for n in self.listStates:
            self._nodes.append(n)

        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self.idMap[n.id] = n

        tmp_edge = DAO.getConnectionWeighted(self.idMap, forma, anno)

        for e in tmp_edge:
            self._edges.append((e[0], e[1], e[2]))

        self._graph.add_weighted_edges_from(self._edges)

    def getGraphSize(self):
        return len(self._nodes), len(self._edges)

    def getArchiAdiacenti(self):
        res = []
        for n in self._nodes:
            peso = 0
            for nn in self._graph[n]:
                peso += self._graph[n][nn]['weight']

            res.append((n, peso))
        return res

    def getBestPath(self):
        self.bestPath = []
        self.bestWeight = 0

        for n in self._nodes:
            parziale = [n]
            archi_visitati = []
            pesi = []
            self._ricorsione(parziale, archi_visitati, pesi)

        return self.bestPath, self.bestWeight, self._graph

    def _ricorsione(self, parziale, archi_visitati, pesi):
        if self.getWeight(parziale) > self.bestWeight:
            self.bestWeight = self.getWeight(parziale)
            self.bestPath = copy.deepcopy(parziale)

        vicini = sorted(self._graph[parziale[-1]], key=lambda x: self._graph[parziale[-1]][x]['weight'])
        for v in vicini:
            if (not pesi or self._graph[parziale[-1]][v]['weight'] > max(pesi)) and (
                    parziale[-1], v) not in archi_visitati and (v, parziale[-1]) not in archi_visitati:
                pesi.append(self._graph[parziale[-1]][v]['weight'])
                parziale.append(v)
                archi_visitati.append((parziale[-2], v))
                self._ricorsione(parziale, archi_visitati, pesi)
                pesi.pop()
                archi_visitati.pop()
                parziale.pop()

    def getWeight(self, lista):
        weight = 0
        for i in range(len(lista) - 1):
            v1 = lista[i]
            v2 = lista[i + 1]
            weight += distance.geodesic((v1.Lat, v1.Lng), (v2.Lat, v2.Lng)).km

        return weight

    def getSingleWeight(self, n1, n2):
        return distance.geodesic((n1.Lat, n1.Lng), (n2.Lat, n2.Lng)).km
