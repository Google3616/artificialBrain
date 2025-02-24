import cv2
import numpy as np
from webs import Web, Node
from video import VideoProcessor

# Initialize Video Processor
processor = VideoProcessor()

# Define grid dimensions
grid_rows = 30
grid_cols = 40
neuron_types = ["red", "green", "blue", "vert", "horiz"]

# Initialize Neural Network
neurons = {(i, j, neuron_types[k]): Node(f"({i},{j},{neuron_types[k]})")
           for i in range(grid_rows) for j in range(grid_cols) for k in range(len(neuron_types))}
web = Web(list(neurons.values()))

# Visualization parameters
canvas_width, canvas_height = 800, 600
neuron_radius = 5
inactive_color = (255, 255, 255)  # White for inactive neurons
active_color = (0, 0, 255)        # Red for active neurons
connection_color = (200, 200, 200)  # Light gray for connections

# Calculate spacing between neurons
spacing_x = canvas_width // grid_cols
spacing_y = canvas_height // grid_rows

# Function to map neuron grid positions to canvas coordinates
def get_neuron_position(i, j):
    x = j * spacing_x + spacing_x // 2
    y = i * spacing_y + spacing_y // 2
    return (x, y)

# Main loop
while True:
    # Capture and process video frame
    result = processor.update()
    if result:
        red, green, blue, edges_x, edges_y = result
        # Update neural network based on processed video data
        web.update(red, green, blue, edges_x, edges_y)

    # Create a blank canvas
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    # Draw connections
    for neuron in web.nodes:
        for connected_neuron in neuron.connected_nodes:
            # Extract grid positions from neuron IDs
            i1, j1, _ = eval(neuron.id)
            i2, j2, _ = eval(connected_neuron.id)
            pt1 = get_neuron_position(i1, j1)
            pt2 = get_neuron_position(i2, j2)
            cv2.line(canvas, pt1, pt2, connection_color, 1)

    # Draw neurons
    for neuron in web.nodes:
        try:
            i, j, _ = eval(neuron.id)
        except:
            i, j, _ = 1,1,0
        pt = get_neuron_position(i, j)
        color = active_color if red[i][j] > 0 else inactive_color
        cv2.circle(canvas, pt, neuron_radius, color, -1)

    # Display the canvas
    cv2.imshow('Neural Network Visualization', canvas)

    # Wait for 250 ms and check for 'q' key press to exit
    if cv2.waitKey(250) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
