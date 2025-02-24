import random
import time

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.connected_nodes = {}

    def connect(self, node, weight=1.0):
        """Create a bidirectional connection with initial weight"""
        self.connected_nodes[node] = weight
        node.connected_nodes[self] = weight  # Ensure mutual connection

    def fire(self, impulse, step=1):
        """Fire the neuron and propagate the impulse"""
        print(f"{self.id} fired with signal {impulse} at step {step}")
        total_connections = len(self.connected_nodes)
        if total_connections > 0 and impulse > 0.1 / total_connections:
            for node, weight in self.connected_nodes.items():
                node.fire((impulse / total_connections) * weight, step + 1)

    def set_weight(self, node, diff=0.1):
        """Increase connection strength bidirectionally"""
        if node not in self.connected_nodes:
            self.connect(node, diff)  # If not connected, establish a connection
        else:
            self.connected_nodes[node] = min(1, self.connected_nodes[node] + diff)
            node.connected_nodes[self] = min(1, node.connected_nodes[self] + diff)

    def scale(self):
        """Normalize connection weights so they sum to 1"""
        total_weight = sum(self.connected_nodes.values())
        if total_weight > 0:
            for node in self.connected_nodes:
                self.connected_nodes[node] /= total_weight
        print(self.connected_nodes)

class Web:
    def __init__(self, size=10,n=[]):
        """Initialize a web of interconnected nodes"""
        if len(n) > 0:
            self.nodes = n
        else:
            self.nodes = [Node(i) for i in range(size)]

    def fire(self, *nodes):
        """Fire multiple nodes and update connection strengths"""
        for node in nodes:
            for other in nodes:
                if node != other:
                    node.set_weight(other, 0.1)  # Strengthen connections
            node.scale()  # Normalize connection weights
        for node in nodes:
            node.fire(1)

