import requests
from bs4 import BeautifulSoup
import re

courseNumRegex = re.compile(r'course/([^>]+)"') # Rewrote numregex to be more consistent. Now also works for KU courses.

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

        # In case of multiple recommended prerequistes seperated by /. This method chooses the first one.
        label = self.html.find("label", text = 'Anbefalede forudsætninger')
        if label == None: return
        temp = label.next_element.next_element
        temp = re.sub(r'/<[^>]+>.','',str(temp))
        self.rec_reqs = courseNumRegex.findall(str(temp))

    def get_obl_reqs(self):
        if self.html == None:
            fetch_html()

        label = self.html.find("label", text = 'Obligatoriske forudsætninger')
        if label == None: return
        templ = label.next_element.next_element.findAll('a',href=True)
        #Runs over the the links and matches them with reguler expressions, so only the course number is added to the list
        for item in templ:
            tempstr = courseNumRegex.findall(str(item))
            self.obl_reqs.append((tempstr[0]))
            
    def get_blocked(self):
        if self.html == None:
            fetch_html()

        label = self.html.find("label", text = 'Pointspærring')
        if label == None: return
        templ = label.next_element.next_element.findAll('a',href=True)
        
        for item in templ:
            tempstr = courseNumRegex.findall(str(item))
            self.blocks.append((tempstr[0]))
