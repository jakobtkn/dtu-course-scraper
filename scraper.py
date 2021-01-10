import time
import networkx as nx
import pickle
import sys
from course import Course
from progressbar import ProgressBar
sys.setrecursionlimit(0x100000) # Required for pickle to be able to save the dictionary

courseDict = {}
f = open('list_of_course_numbers.txt','r')
n = 1739

for i in range(n):
    courseId = f.readline().rstrip('\n')
    courseDict.update({ courseId : Course(courseId)})

print('Fetching html from kurser.dtu.dk')
for course in ProgressBar()((courseDict.values())):
    course.fetch_html()
    course.get_obligatory()
    course.get_recommended()
    course.get_blocked()
    course.get_course_name()
    course.get_department_id()
    course.html = [] # Deletes HTML now that we have extracted relevant info
    
with open('course_dictionary.pickle', 'wb') as handle:
    pickle.dump(courseDict, handle, protocol=pickle.HIGHEST_PROTOCOL)