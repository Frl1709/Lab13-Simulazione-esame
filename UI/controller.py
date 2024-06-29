import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        self._listYear = self._model.listYears
        self._listShape = self._model.listShapes

        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))

        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value

        self._model.buildGraph(forma, anno)
        nN, nE = self._model.getGraphSize()
        pesoArchi = self._model.getArchiAdiacenti()

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {nN} Numero di archi: {nE}"))
        for e in pesoArchi:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {e[0].id}, somma pesi su archi = {e[1]}"))
        self._view.update_page()
    def handle_path(self, e):
        bestPath, bestWeight, grafo = self._model.getBestPath()

        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {bestWeight}"))

        for n in range(len(bestPath)-1):
            v1 = bestPath[n]
            v2 = bestPath[n+1]
            self._view.txtOut2.controls.append(ft.Text(f"{v1.id} --> {v2.id}: weight {grafo[v1][v2]['weight']} distance {self._model.getSingleWeight(v1, v2)}"))

        self._view.update_page()