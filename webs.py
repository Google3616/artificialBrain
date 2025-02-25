import random
import time
import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.connected_nodes = {}

    def connect(self, node, weight=0.5):
        """Create a bidirectional connection with initial weight"""
        self.connected_nodes[node] = weight
        node.connected_nodes[self] = weight  # Ensure mutual connection

    def fire(self, impulse, step=1):
        """Fire the neuron and propagate the impulse"""
        print(f"{self.id} fired with signal {impulse} at step {step}")
        total_connections = len(self.connected_nodes)
        if  impulse > 0.2 / (1+ total_connections):
            for node, weight in self.connected_nodes.items():
                node.fire((impulse / (1+total_connections)) * weight, step + 1)

    def hebbian(self, node, diff=0.1):
        """Increase connection strength bidirectionally"""
        if node not in self.connected_nodes:
            self.connect(node)  # If not connected, establish a connection
        else:
            self.connected_nodes[node] += self.connected_nodes[node]/2
            node.connected_nodes[self] += self.connected_nodes[node]/2
    

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

    def fire(self, nodes, fireAmounts):
        """Fire multiple nodes and update connection strengths"""
        for node in nodes:
            for other in nodes:
                if node != other:
                    node.hebbian(other)  # Strengthen connections
            #node.scale()  # Normalize connection weights
        for i,node in enumerate(nodes):
            node.fire(fireAmounts[i])
    def draw(self, offsets=[]):
        """Draws the neural network using Matplotlib with node labels and offset edges."""
        plt.figure(figsize=(8, 8))
        G = nx.Graph()
        pos = {}  # Dictionary to store node positions
        labels = {}  # Dictionary to store labels

        # Assign positions based on offsets and create labels
        for node in self.nodes:
            x, y = eval(node.id)  # Extract coordinates
            x1, y1 = offsets[x][y]  # Apply offsets
            pos[node] = (x1, -y1)  # Adjust position for visualization
            labels[node] = f'{["Volume","Band 1", "Band 2", "Band 3", "Band 4", "Band 5", "Band 6"][y]}, {x}'  # Store the label

            G.add_node(node)

        # Add edges with varying thickness based on weights
        edges = []
        edge_widths = []
        edge_pos = []  # Stores the offset positions for edges
        for node in self.nodes:
            for connected_node, weight in node.connected_nodes.items():
                if (connected_node, node) not in edges:  # Avoid duplicate edges
                    edges.append((node, connected_node))
                    edge_widths.append(weight * 5)  # Scale weight for visualization

                    # Get offset positions for both nodes
                    x1, y1 = pos[node]
                    x2, y2 = pos[connected_node]
                    edge_pos.append(((x1, y1), (x2, y2)))

        G.add_edges_from(edges)

        # Draw the network
        nx.draw(G, pos, with_labels=False, node_size=200, edge_color='black', width=edge_widths)

        # Manually draw edges with offset positions
        for (start, end), width in zip(edge_pos, edge_widths):
            plt.plot([start[0], end[0]], [start[1], end[1]], 'black', linewidth=width)

        # Draw labels near nodes
        for node, (x, y) in pos.items():
            plt.text(x, y + 0.05, labels[node], fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.3'))

        plt.show()
