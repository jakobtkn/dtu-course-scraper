import requests
from bs4 import BeautifulSoup
import re

courseNumRegex = re.compile(r'course/([^>]+)"')

departments = {29 : 'DTU Biosustain', 34 : 'Institut for Fotonik', 12 : 'Institut for Vand og Miljøteknologi', 46 : 'Institut for Vindenergi', 30 : 'Institut for Rumforskning og -teknologi', 11 : 'Institut for Byggeri og Anlæg', 26: 'Institut for Kemi', 41:  'Institut for Mekanisk Teknologi', 25:  'Institut for Akvatiske Ressourcer', 23 : 'Fødevareinstituttet', 47 : 'Institut for Energikonvertering- og lagring', 1 :  'Institut for Matematik og Computer Science', 31 :  'Institut for Elektroteknologi', 22 : 'Institut for Sundhedsteknologi', 42 : 'Institut for Teknologi, Ledelse og Økonomi', 10 : 'Institut for Fysik', 27 : 'Institut for Bioteknologi og Biomedicin', 62 : 'DTU Diplom', 28 : 'Institut for Kemiteknik', 88 : 'Andre kurser'}


global session
session = None
class Course:
    def __init__(self,id):
        self.id = id
        self.recommended = []
        self.obligatory = []
        self.blocked = []
        self.name = []
        self.department = None
        self.html = None

    def url(self):
        return('http://kurser.dtu.dk/course/' + str(self.id))

    def fetch_html(self):
        global session
        if session == None:
            session = requests.Session()
            session.get('http://kurser.dtu.dk', allow_redirects=False)
        resp = session.get(self.url())
        self.html = BeautifulSoup(resp.content,'html.parser')

    def get_recommended(self):
        if self.html == None:
            self.fetch_html()

        #  'In case of multiple recommended prerequistes seperated by /. This method chooses the first one.
        label = self.html.find("label", text = 'Anbefalede forudsætninger')
        if label == None: return
        temp = label.next_element.next_element
        temp = re.sub(r'/<[^>]+>.','',str(temp))
        self.recommended = courseNumRegex.findall(str(temp))

    def get_obligatory(self):
        if self.html == None:
            self.fetch_html()

        label = self.html.find("label", text = 'Obligatoriske forudsætninger')
        if label == None: return
        templ = label.next_element.next_element.findAll('a',href=True)
        #Runs over the the links and matches them with reguler expressions, so only the course number  'Is added to the list
        for item in templ:
            tempstr = courseNumRegex.findall(str(item))
            self.obligatory.append((tempstr[0]))
            
    def get_blocked(self):
        if self.html == None:
            self.fetch_html()

        label = self.html.find("label", text = 'Pointspærring')
        if label == None: return
        templ = label.next_element.next_element.findAll('a',href=True)
        
        for item in templ:
            tempstr = courseNumRegex.findall(str(item))
            self.blocked.append((tempstr[0]))
            
    def get_name(self):
        if self.html == None:
            self.fetch_html()
            
        self.name = self.html.find("title").string[4:-4].strip()

    def get_department_id(self):
        if self.html == None:
            self.fetch_html()
        
        self.department_id = int(self.html.find("label", text = 'Institut').next_element.next_element.string[:3])
        #int(self.html.find("label", text = 'Institut').next_element.next_element.string[:3])
    def department_name(self):
        try:
            return departments[self.department_id]
        except:
            return None