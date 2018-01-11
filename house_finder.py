import requests, re
from bs4 import BeautifulSoup
import sqlite3
import database

#Get the first page from specified URL to extract page numbers
r=requests.get("http://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=")
c=r.content

soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("div",{"class":"cassetteitem"})

# Just a test to see if scraper works
all[0].find("span",{"class":"cassetteitem_other-emphasis ui-text--bold"}).text.replace("\n","").replace(" ","")
test = all[0].find("li",{"class","cassetteitem_detail-col1"})
print(test)

# Interprets number of pages from page selector at bottom of first page
page_nr=soup.find_all("ol",{"class":"pagination-parts"})[-1].text
page_nr = [int(s) for s in page_nr.split() if s.isdigit()]
page_nr = page_nr[len(page_nr)-1]

# Informs of how many pages were found
print(page_nr,"pages were found")

l=[]
base_url='http://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2='

items = []
n = 0

# Goes through all discovered pages one by one
for page in range(1,2,1):
    #print(    )
    r=requests.get(base_url+'&pn='+str(page))
    c=r.content
    #c=r.json()["list"]
    soup=BeautifulSoup(c,"html.parser")
    all = soup.find_all(lambda tag: tag.name == 'div' and
                                   tag.get('class') == ['cassetteitem'])
    #all=soup.find_all("div",{"class":"cassetteitem"})

    # Locates and interprets information of interest for each rental property and stores it in dictionaries
    for item in all:
        d={}
        d["Title"]=item.find("div",{"class","cassetteitem_content-title"}).text

        #
        d["Locality"]=item.find("li",{"class","cassetteitem_detail-col1"}).text

        # Price
        d["Price"]=item.find("span",{"class","cassetteitem_other-emphasis ui-text--bold"}).text.replace("\n","").replace(" ","")

        # Number of rooms
        rooms = item.find("table",{"class","cassetteitem_other"}).text
        if 'ワンルーム' in rooms:
            d["Rooms"]=1
        elif '1K' in rooms:
            d["Rooms"]=1
        elif '2K' in rooms:
            d["Rooms"]=2
        else:
            d["Rooms"]="Unknown"

        table = item.find_all("table",{"class","cassetteitem_other"})[0]
        nums = re.findall(r'\d+(?:\.\d+)?', str(table))
        d["Size"]=nums[-6]+" m2"

        d["Link"]=item.find("td",{"class","ui-text--midium ui-text--bold"}).text

        #d[]=item.find_all("",{"",""})[0].text

        # Dictionaries appended to a list
        l.append(d)

database.create_table()
for d in l:
    database.insert(d["Title"],d["Locality"],d["Price"],d["Rooms"],d["Size"],d["Link"])

print(database.view())
