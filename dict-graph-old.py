from pyvis.network import Network
import json
import re
import networkx as nx

# NOTE FROM ME
# This was a first prototype for visualizing a dictionary and the words used in its definitions.
# I used networkx and pyvis so it would open in my browser and so I could use physics and interact with it.
# This is terribly infeasible, it has something like an O(n^2) complexity, making it horrible to run with any more than a few words.
# As a result I am starting new with more optimized libraries in a different file.
# END NOTE


# Load dictionary
with open('dictionary.json', 'r') as f:
    dictionary = json.load(f)

# Clean definitions
def clean_definition(text):
    return re.findall(r'\b\w+\b', text.lower())

word_definitions = {word: clean_definition(definition) for word, definition in list(dictionary.items())[:4]}  # Subset for testing

# Build graph
G = nx.DiGraph()
for word, def_words in word_definitions.items():
    G.add_node(word)
    for def_word in list(def_words)[:55]:
        if def_word in dictionary:  # Ensure target word exists
            G.add_edge(word, def_word)

# Visualize
net = Network(notebook=False, directed=True, height='700px')
net.from_nx(G)
net.toggle_physics(False)
net.show_buttons(filter_=['physics'])
net.show('graph.html', notebook=False)


# Save graph
import pickle
with open('graph.pkl', 'wb') as f:
    pickle.dump(G, f)