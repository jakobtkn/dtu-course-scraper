import pickle
from course import Course
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyvis.network import Network

with open('course_dictionary.pickle', 'rb') as handle:
    courseDict = pickle.load(handle)

G = nx.Graph()
nodes = []
node_names = []
rec_edges = []
obl_edges = []
blocks_edges = []

n = 1700
courses = list(courseDict.values())[: n+1 ]
labelDict = {}

for course in courses:
    # print(course.id)
    if bool(course.rec_reqs) | bool(course.obl_reqs) | bool(course.blocks):
        nodes.append(course)
        labelDict.update({course.id : course.id})
        for req in course.rec_reqs:
            rec_edges.append([course.id,req])
        for req in course.obl_reqs:
            obl_edges.append([course.id,req])
        for req in course.blocks:
            blocks_edges.append([course.id,req])

G.add_nodes_from(node_names, label = node_names)
G.add_edges_from(rec_edges, color = 'black')
G.add_edges_from(obl_edges, color = 'b')
G.add_edges_from(blocks_edges, color = 'r')

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]

#nx.draw_kamada_kawai(G,node_size = 10, edge_color = colors, labels = labelDict, with_labels = True)
#plt.savefig('graph.png', dpi = 900)

nt = Network("1080px", "1920px")
nt.from_nx(G)
nt.show("nx.html")