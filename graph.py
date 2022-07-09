import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.modalview import ModalView
from matplotlib import pyplot as plt


class Graph(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_graph(self, id):
        if id == "daily":
            values = np.random.uniform(low=1.0, high=24.0, size=(24,))
            plt.clf()
            plt.plot(values)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True, color='#433A66')
            self.ids.graph.clear_widgets()
            self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        elif id == "weekly":
            values = np.random.uniform(low=1.0, high=24.0, size=(7,))
            plt.clf()
            plt.plot(values)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True, color='#433A66')
            self.ids.graph.clear_widgets()
            self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        else:
            values = np.random.uniform(low=1.0, high=24.0, size=(28,))
            plt.clf()
            plt.plot(values)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True, color='#433A66')
            self.ids.graph.clear_widgets()
            self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def close_model(self):
        self.dismiss()
