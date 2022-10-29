from html.parser import HTMLParser
import urllib
import urllib.request
import sys
import sqlite3
import re
import time

viewers_re = re.compile("([0-9]+) viewers")

class CbParser(HTMLParser):

    def __init__(self):
        self.inroom = None
        self.next_page = None
        self.room_count = 0
        self.viewer_count = 0
        self.viewer_errs = 0
        super().__init__()

    def clear(self):
        self.url = None
        self.valid = False
        self.title = None

    def getattr(self, attrs, a):
        for (k, v) in attrs:
            if (k == a):
                return v
        return None

    def handle_starttag(self, startTag, attrs):
#        print(f"debug: {startTag}")
        if (not self.inroom):
            if (startTag == 'li'):
                if (self.getattr(attrs, 'class') == 'room_list_room'):
                    self.inroom = dict({'li':1})
            elif (startTag == 'a'):
                if (self.getattr(attrs, 'class') == 'next endless_page_link'):
                    self.next_page = self.getattr(attrs, 'href')
        elif (startTag == 'li'):
            self.inroom['li'] = self.inroom['li'] + 1
        elif (startTag == 'a'):
            if (not 'name' in self.inroom):
                self.inroom['name'] = self.getattr(attrs,'data-room')
        elif (startTag == 'span'):
            if (self.getattr(attrs, 'class') == 'viewers'):
                self.inroom['viewertext'] = True
                

    def handle_endtag(self, tag):
        if (self.inroom):
            if (tag == 'li'):
                level = self.inroom['li']
                if (level == 1):
                    self.finish_entry()
                else:
                    self.inroom['li'] = level - 1
            if (tag == 'span'):
                self.inroom['viewertext'] = False

    def handle_data(self, data):
        if (self.inroom and self.inroom.get('viewertext')):
            self.inroom['viewers'] = self.inroom.get('viewers', '') + data

    def finish_entry(self):
        m = viewers_re.match(self.inroom['viewers'])
        viewers = 0
        if (m):
            viewers = int(m.group(1))
            self.viewer_count += viewers
        else:
            self.viewer_errs += 1
        print(f"{self.inroom['name']}: {viewers}")
        self.room_count += 1
        self.inroom = None
        
parser = CbParser()

url = sys.argv[1]

while (url):
    html_page = urllib.request.urlopen(url)
    content = str(html_page.read())

    parser.feed(content)

    if (parser.next_page):
        url = urllib.parse.urljoin(url, parser.next_page)
        parser.next_page = None
        time.sleep(5)
    else:
        url = None

    print(f"Next: {url}")
    sys.stdout.flush()
    
    
print(f"Totals: {parser.room_count} rooms, {parser.viewer_count} viewers")
