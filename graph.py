import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.modalview import ModalView
from matplotlib import pyplot as plt


class Graph(ModalView):  # creating a class to show graph of user activity in to graph using matplotlib
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_graph(self, id):  # here creating a function to show graph on graph section of the app.

        if id == "daily":  # This graph show daily activity
            values = np.random.uniform(low=1.0, high=24.0, size=(24,))
            plt.clf()
            plt.plot(values)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True, color='#433A66')
            self.ids.graph.clear_widgets()
            self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        elif id == "weekly":  # This graph shows weekly activity
            values = np.random.uniform(low=1.0, high=24.0, size=(7,))
            plt.clf()
            plt.plot(values)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True, color='#433A66')
            self.ids.graph.clear_widgets()
            self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        else:  # This graph shows monthly graph
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
