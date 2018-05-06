import requests, re
from bs4 import BeautifulSoup
import pandas
import database

# this is the URL generated after choosing specific search criteria on the website (e.g. location, house type, price range)
search_url = "http://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2="

# obtaining all content from pre-defined URL
r = requests.get(search_url)
c = r.content

# we use beautifulsoup to make sense of the data
soup = BeautifulSoup(c,"html.parser")

# it was determined that we need to look inside the class "cassetteitem" having inspected the HTML elements 
all = soup.find_all("div",{"class":"cassetteitem"})

# now we can see how all entries related to the search were split into pages by looking for "pagination-parts" class instances.
page_nr = soup.find_all("ol",{"class":"pagination-parts"})[-1].text
page_nr = [int(s) for s in page_nr.split() if s.isdigit()]
page_nr = page_nr[len(page_nr)-1]

print(page_nr,"pages were found")

# iterating through each page by adding page number to end of search URL each time
l = []
for page in range(1, 2):  # for the sake of this example, only one page is used to speed up the operation
    r = requests.get(search_url + '&pn=' + str(page))
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all(lambda tag: tag.name == 'div' and 
                                   tag.get('class') == ['cassetteitem'])    # "cassetteitem" is the class for each house

    # for each house discovered, let's collect information on title, locality, number of room, floor area and price
    # and put the information into a dictionary
    for item in all:
        d = {}
        d["Title"] = item.find("div",{"class","cassetteitem_content-title"}).text
        d["Locality"] = item.find("li",{"class","cassetteitem_detail-col1"}).text
        d["Price"] = item.find("span",{"class","cassetteitem_other-emphasis ui-text--bold"}).text.replace("\n","").replace(" ","")

        # finding number of rooms is more complicated in this situation, because categories need to be decoded
        rooms = item.find("table",{"class","cassetteitem_other"}).text
        if 'ワンルーム' in rooms:
            d["Rooms"] = 1
        elif '1K' in rooms:
            d["Rooms"] = 1
        elif '2K' in rooms:
            d["Rooms"] = 2
        else:
            d["Rooms"] = "Unknown"
        
        # need to dig inside tables to find the relevant number
        table = item.find_all("table",{"class","cassetteitem_other"})[0]
        nums = re.findall(r'\d+(?:\.\d+)?', str(table))
        d["Size"] = nums[-6]+" m2"
        
#         d["Link"] = item.find("td",{"class","ui-text--midium ui-text--bold"}).text
        
        l.append(d)

# goes back through all of the houses in the list of dictionaries and enters the respective information into database
database.create_table()
for d in l:
    database.insert(d["Title"],d["Locality"],d["Size"],d["Rooms"],d["Price"])