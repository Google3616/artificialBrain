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
        #print(f"{self.id} fired with signal {impulse} at step {step}")
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
    def __init__(self, nodes):
        self.nodes = nodes  # A dictionary of nodes with keys as (x, y, type)

    def update(self, red, green, blue, edges_x, edges_y,keys):
        """
        Update the neural network based on the input arrays.
        Each array corresponds to a specific type of input and activates the respective neurons.
        """
        # Define a helper function to process each array
        fire = []
        weights = []
        def process_array(array, color_type):
            for x, row in enumerate(array):
                for y, intensity in enumerate(row):
                    if intensity > 0:
                        neuron_key = (x, y, color_type)
                        
                        if keys[neuron_key] in self.nodes and intensity > 125:
                            fire.append(keys[neuron_key])
                            weights.append(intensity/255.0)

        # Process each array with the corresponding neuron type
        process_array(red, "red")
        process_array(green, "green")
        process_array(blue, "blue")
        process_array(edges_x, "vert")
        process_array(edges_y, "horiz")
        self.fire(fire,weights)

    def fire(self, nodes, weights):
        """Fire multiple nodes and update connection strengths"""
        for node in nodes:
            for other in nodes:
                if node != other:
                    node.set_weight(other, 1)  # Strengthen connections
            #node.scale()  # Normalize connection weights
        for i,node in enumerate(nodes):
            node.fire(weights[i])

