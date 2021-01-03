import time
from threading import Thread, Lock
import networkx as nx
<<<<<<< HEAD
import matplotlib.pyplot as plt
import matplotlib as mpl

import re
from itertools import islice
from bs4 import BeautifulSoup

global session
session = None
counter = 0
courseNumRegex = re.compile(r'>([0-9]+)</a>')

#defining the graph type
G = nx.MultiDiGraph()

class Course:
    def __init__(self,id):
        self.id = id
        self.rec_reqs = []
        self.obl_reqs = []
        self.blocks = []
        self.html = None

    def get_url(self):
        return('http://kurser.dtu.dk/course/' + str(self.id))

    def fetch_html(self):
        global session
        if session == None:
            session = requests.Session()
            session.get('http://kurser.dtu.dk', allow_redirects=False)
        resp = session.get(self.get_url())
        self.html = BeautifulSoup(resp.content,'html.parser')

    def get_rec_reqs(self):
        if self.html == None:
            fetch_html()

        label = self.html.find("label", text = 'Anbefalede forudsætninger')
        if label == None: return
        self.rec_reqs = label.next_element.next_element.findAll('a',href=True)

    def get_obl_reqs(self):
        if self.html == None:
            fetch_html()

        label = self.html.find("label", text = 'Obligatoriske forudsætninger')
        if label == None: return
        templ = label.next_element.next_element.findAll('a',href=True)
        #Runs over the the links and matces them with reguler expressions, so only the course number is added to the list
        for item in templ:
            tempstr = courseNumRegex.findall(str(item))
            self.obl_reqs.append((tempstr[0]))


#does the works
def worker(t_id,snip):
    counter = 0
    print("started")
    print(snip)
    for courseNumber, course in snip.items(): #items() allows splits the key and the value
        #print("sdsad")
        counter = counter + 1
        course.fetch_html()
        course.get_obl_reqs()
        links = course.obl_reqs
        #print(courseNumber)
        #print(links)
        #print("thread" + "id: " + str(t_id) + " progress: " + str(counter) + " current: " + courseNumber)
        #print(course.obl_reqs)
        for x in course.obl_reqs:
            edge = (courseNumber,x)
            mutex.acquire()
            try:
                #counter = counter + 1
                G.add_edge(*edge)
                #print("just added edge: " + x + courseNumber)
            finally:
                mutex.release()

	


=======
import pickle
import sys
from course import Course
from progressbar import ProgressBar

sys.setrecursionlimit(0x100000) # Ran into problemings saving list with pickle
>>>>>>> rewrite

f = open('list_of_course_numbers.txt','r')
<<<<<<< HEAD
#needs to be devisible with nt
n = 1600

#number of threads
nt = 10
courseDict = [{} for sub in range(nt)]


#makes the nodes ready and adds them to the dictonaires
for i in range(nt):
    for j in range(int(n/nt)):
        courseId = f.readline().rstrip('\n')
        courseDict[i].update({ courseId : Course(courseId)})
        G.add_node(courseId)


max = 0
count = 0


#initilies the mutex, that protects the graph object
mutex = Lock()
threads= []

#starts threads
for item in courseDict:
    thread = Thread(target=worker, args=(count, item,))
    count = count + 1
    threads.append(thread)
    thread.start()
    
for t in threads:
    t.join()
print(counter)
print(G.nodes)
print(G.edges)






################################################
#plotting an
nx.draw(G)
plt.show()


# print(courseDict['01003'].id)
# print(courseDict['01005'].html.prettify())
# # # # Start session.
# session = requests.Session()
# response = session.get('http://kurser.dtu.dk', allow_redirects=False)

# # courses = [while f.readline != None: ]

#  urls = ['http://kurser.dtu.dk/course/11569','http://kurser.dtu.dk/course/KU010','http://kurser.dtu.dk/course/02320']
#   response = session.get(urls[1], allow_redirects=False)
#   soup = BeautifulSoup(response.content, 'html.parser')
  # label = soup.find("label", text = 'Anbefalede forudsætninger')
# # if label == None:
# #     label = soup.find("label", text = 'Obligatoriske forudsætninger')
# if label != None:
#     print(label)
#     prereqs = label.next_element.next_element.findAll('a',href=True)
#     for a in prereqs:
#         print (a['href'])
# else:
#     print (soup)




#user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}
# for url in f:
#     session.get(url, allow_redirects=False)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     print(url)
#     time.sleep(1)
#     response = session.get(url, allow_redirects=False)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     label = soup.find("label", text = 'Anbefalede forudsætninger')
#     # if label == None:
#         # label = soup.find("label", text = 'Obligatoriske forudsætninger')
#     if label != None:
#         print(label)
#     #     prereqs = label.next_element.next_element.findAll('a',href=True)
#     #     for a in prereqs:
#     #         print (a['href'])
#     else:
#         print (soup)

# close(f)
=======
n = 1700
pbar = ProgressBar()


print('Reading course numbers')
for i in range(n):
    courseId = f.readline().rstrip('\n')
    courseDict.update({ courseId : Course(courseId)})

print('Fetching html from kurser.dtu.dk')
for course in pbar(courseDict.values()):
    course.fetch_html()

print('Extracting relevant info')
for course in courseDict.values():
    course.get_obl_reqs()
    course.get_rec_reqs()
    course.get_blocked()
    course.get_name()
    course.get_department_id()
    course.html = []
    
with open('course_dictionary.pickle', 'wb') as handle:
    pickle.dump(courseDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
>>>>>>> rewrite
