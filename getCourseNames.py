import requests
from bs4 import BeautifulSoup

f = open('list_of_course_numbers.txt','w')

url_sitemap = 'http://kurser.dtu.dk/sitemap.xml'

resp = requests.get(url_sitemap)
soup = BeautifulSoup(resp.content, 'html.parser')

urls = soup.find_all('loc')
urls.pop(0) #Remove kurser.dtu.dk

for url in urls:
    f.writelines(url.text.rsplit('/',1)[1]+ '\n')
f.close()