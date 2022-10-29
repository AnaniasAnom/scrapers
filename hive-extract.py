from html.parser import HTMLParser
import urllib.request as urllib2
import sys
import sqlite3

# from firefox, save the page with thumbnails as "cshive.com" in the screenshots directory
# cd screenshots/whoever
# python ~/devel/scrapers/hive-extract.py cshive.com
# mv cshive_files hive
# cd hive
# bash ~/devel/scrapers/tag-hive-thumbs.sh
# rm *.svg *.js *.css *_original




class MyHTMLParser(HTMLParser):

    def __init__(self, connection):
        self.db = connection
        self.cur = db.cursor()
        self.clear()
        super().__init__()

    def clear(self):
        self.url = None
        self.valid = False
        self.title = None

    def handle_starttag(self, startTag, attrs):
        if (startTag == 'img'):
            for (k, v) in attrs:
                if (k == 'class'):
                    self.valid = (v == 'm-1')
                elif (k == 'title'):
                    self.title = v
                elif (k == 'src'):
                    self.url = v
            if (self.valid and self.title and self.url):
                filename = self.url.split("/").pop()
                basename = filename.removesuffix('.jpg')
                parts = basename.split("-")
            
                # print(f"id = {parts[1]}")
                self.cur.execute("INSERT INTO thumb (id, girlid, tstamp) VALUES (?, ?, ?)", [ parts[1], parts[0], self.title[-19:] ])
                self.clear()

    def handle_endtag(self, tag):
        if (tag == 'html'):
            self.db.commit();
                
def initdb(db):
    cursorObj = db.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS thumb (id INTEGER PRIMARY KEY, girlid INTEGER, tstamp VARCHAR(30))")
    
db = sqlite3.connect('hivedata.db')

initdb(db)

#creating an object of the overridden class
parser = MyHTMLParser(db)

html_page = open(sys.argv[1],"r")

#Feeding the content
content = str(html_page.readlines())

parser.feed(content)
    
