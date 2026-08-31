import networkx as nx


class GraphBuilder:

    @staticmethod
    def build(mapping):

        graph = nx.DiGraph()

        for connector in mapping.connectors:

            graph.add_edge(
                connector.from_instance,
                connector.to_instance
            )

        return graph

    @staticmethod
    def execution_order(graph):

        if not graph.nodes:
            return []

        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError(
                "Mapping contains a dependency cycle. "
                "Cannot determine execution order."
            )

        return list(nx.topological_sort(graph))

    @staticmethod
    def has_cycle(graph):

        return not nx.is_directed_acyclic_graph(graph)

    @staticmethod
    def root_nodes(graph):

        return [
            node
            for node, degree in graph.in_degree()
            if degree == 0
        ]

    @staticmethod
    def leaf_nodes(graph):

        return [
            node
            for node, degree in graph.out_degree()
            if degree == 0
        ]