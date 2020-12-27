import requests
import time
import networkx as nx
from bs4 import BeautifulSoup

global session
session = None
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
        self.obl_reqs = label.next_element.next_element.findAll('a',href=True)

courseDict = {}
f = open('list_of_course_numbers.txt','r')
n = 1000

for i in range(n):
    courseId = f.readline().rstrip('\n')
    courseDict.update({ courseId : Course(courseId)})

max = 0
for course in courseDict:
    courseI = courseDict[course]
    courseI.fetch_html()
    courseI.get_obl_reqs()
    links = courseI.obl_reqs
    if links != None and len(links) > max:
        max = len(links)
        print(course + ' new record: ' + str(max))

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