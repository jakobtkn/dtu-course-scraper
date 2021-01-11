import pickle
from course import Course
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyvis.network import Network

with open('course_dictionary.pickle', 'rb') as handle:
    courseDict = pickle.load(handle)

departmentColor = {29 : 'green', 34 : 'orange', 12 : 'cyan', 46 : 'blue', 30 : 'black', 11 : 'gray', 26: 'yellow', 41 : 'dark gray', 25:  'dark blue', 23 : 'brown', 47 : 'purple', 1 :  'red', 31 :  'magenta', 22 : 'purple', 42 : 'purple', 10 : 'purple', 27 : 'green', 62 : 'black', 28 : 'yellow', 88 : 'dark red'}
node_names = []

n = 1739
courses = list(courseDict.values())[: n+1 ]
nt = Network("1080px", "1920px")

# Change filter to get a different selection of courses. Here the graph is limited to courses from DTU Compute.
filtered = list(filter(lambda x: x.department_id == 1, courses))

for course in filtered:
    nt.add_node(course.id, label = course.id, title = course.name, physics = True, color = departmentColor[course.department_id])
    node_names.append(course.id)
    for target in list(set(course.recommended) & set(node_names)):
            nt.add_edge(target,course.id, color = 'black', arrows = 'middle')
    for target in list(set(course.obligatory) & set(node_names)):
            nt.add_edge(target,course.id, color = 'blue', arrows = 'middle')
    for target in list(set(course.blocked) & set(node_names)):
            nt.add_edge(target,course.id, color = 'red')

nt.show("nx.html")