import requests
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
    
    def get_blocked(self):
        return
