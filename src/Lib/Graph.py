class Node(object):

    def __init__(self, name):
        self.name = name
        self.connections = 0
        self.neighbours = []

    def add_edge(self, edge):
        self.neighbours.append(edge)

    def is_neighbour(self, test_node):
        return test_node in self.neighbours

    def __str__(self):
        namestr = "Name of node: {} \nNeighbours: \n".format(self.name)
        for x in self.neighbours:
            namestr += "{} \n".format(x)
        return namestr

    def __eq__(self, other):
        return self.name == other.name


class Edge(object):

    def __init__(self, node_a, node_b, value):
        self.nodes = [node_a, node_b]
        self.value = value
        node_a.add_edge(self)
        node_b.add_edge(self)

        self.value = value

    def __str__(self):
        return "{}-{}".format(self.nodes[0].name, self.nodes[1].name)

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __int__(self):
        return self.value
