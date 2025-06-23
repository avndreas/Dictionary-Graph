from pyvis.network import Network
import json
import re
import networkx as nx


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
    for def_word in list(def_words)[:30]:
        if def_word in dictionary:  # Ensure target word exists
            G.add_edge(word, def_word)

# Visualize
net = Network(notebook=False)
net.from_nx(G)
net.show('graph.html', notebook=False)

# Save graph
import pickle
with open('graph.pkl', 'wb') as f:
    pickle.dump(G, f)