import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:

    @staticmethod
    def draw(graph):

        nx.draw(

            graph,

            with_labels=True,

            node_size=2500,

            font_size=10

        )

        plt.show()