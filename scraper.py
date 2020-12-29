import time
import networkx as nx
import pickle
import sys
from course import Course

sys.setrecursionlimit(0x100000) # Ran into problemings saving list with pickle

courseDict = {}
f = open('list_of_course_numbers.txt','r')
n = 100

print('Reading course numbers')
for i in range(n):
    courseId = f.readline().rstrip('\n')
    courseDict.update({ courseId : Course(courseId)})

print('Fetching html from kurser.dtu.dk')
for course in courseDict.values():
    course.fetch_html()

print('Extracting relevant info')
for course in courseDict.values():
    course.get_obl_reqs()
    course.get_rec_reqs()
    course.get_blocked()    
    course.html = []

with open('course_dictionary.pickle', 'wb') as handle:
    pickle.dump(courseDict, handle, protocol=pickle.HIGHEST_PROTOCOL)