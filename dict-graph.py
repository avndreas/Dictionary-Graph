from graph_tool.all import *
import matplotlib.pyplot as plt
import json
import re


# Load dictionary
with open('dictionary.json', 'r') as f:
    dictionary = json.load(f)

# Clean definitions
def clean_definition(text):
    return re.findall(r'\b\w+\b', text.lower())

word_definitions = {word: clean_definition(definition) for word, definition in list(dictionary.items())[:20]}  # Subset for testing

g = Graph()

# Create vertex properties
v_label = g.new_vertex_property("string")
v_size = g.new_vertex_property("double")

# Function to add vertex with label if it doesn't exist and add an edge
def add_vertex_and_edge(graph, source_label, target_label):
    # Check if source vertex exists
    source_vertex = None
    for v in graph.vertices():
        if v_label[v] == source_label:
            source_vertex = v
            break
    
    # If source vertex doesn't exist, create it
    if source_vertex is None:
        source_vertex = graph.add_vertex()
        v_label[source_vertex] = source_label
    
    # Check if target vertex exists
    target_vertex = None
    for v in graph.vertices():
        if v_label[v] == target_label:
            target_vertex = v
            break
    
    # If target vertex doesn't exist, create it
    if target_vertex is None:
        target_vertex = graph.add_vertex()
        v_label[target_vertex] = target_label
    
    if source_vertex == target_vertex:
        return  # Avoid self-loops

    # Add edge from source to target
    graph.add_edge(source_vertex, target_vertex)


for word, def_words in word_definitions.items():
    for def_word in list(def_words)[:]:
        if def_word in dictionary:  # Ensure target word exists
            add_vertex_and_edge(g, word, def_word)

# Set vertex sizes based on degree
min_size = 4.0    # Minimum vertex size
max_size = 20.0   # Maximum vertex size
max_degree = max(v.in_degree() for v in g.vertices()) or 1  # Avoid division by zero
for v in g.vertices():
    degree = v.in_degree()  # Total degree for directed graph
    # Linear scaling: size = min_size + (degree/max_degree) * (max_size - min_size)
    v_size[v] = min_size + (degree / max_degree) * (max_size - min_size)

plt.switch_backend("cairo")   # to enable vector drawing

# Compute layout using sfdp_layout for large graphs
pos = sfdp_layout(
    g,
    multilevel=True, 
    cooling_step=0.99,      # Gradual convergence for better spacing
    epsilon=1e-3,           # Convergence threshold (balance speed vs. quality)
    C=1.0,                  # Increase repulsion for more spacing
    K=0.1,
    p=1.5,
    max_iter=100            # Limit iterations for performance
)

# Draw the graph with optimized settings
graph_draw(
    g,
    pos=pos,                        # Use computed layout
    vertex_text=v_label,            # Display labels
    vertex_text_position=0.0,       # Place labels directly below vertices (0 radians = bottom)
    vertex_text_offset=[0, 0],     # Offset labels slightly below vertices
    vertex_font_size=6,             # Small font to avoid clutter
    vertex_size=v_size,                  # Uniform small vertex size
    vertex_anchor=0,                # Anchor vertices at center
    edge_pen_width=0.5,             # Thin edges for clarity
    output_size=(5000, 5000),       # Large canvas for enormous graph
    adjust_aspect=False,            # Preserve layout scale
    bg_color=(1, 1, 1, 1),    # White background
    output="dict-graph.svg"         # Save to svg
)