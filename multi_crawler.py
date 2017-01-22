from bs4 import *
import urllib
import re
import time
import threading
from Queue import Queue

titles = Queue()
fname = "title.txt"
semaphore = threading.Semaphore()

class Parser(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self) # initialize super class
        self.name = name

    def run(self):
        while titles.empty() is False:
            current_url = titles.get()
            parse(current_url)

counter = 0
def parse(current_url):
    global counter
    u = urllib.urlopen(current_url)
    html = u.read()
    soup = BeautifulSoup(html, "html.parser")

    title_tags = soup.find_all("div", {"class": "h5"})

    for tag in title_tags:
        title = re.findall('title="(.+)"', str(tag))
        try:
            line = title[0].strip('\n') + '\n'

            semaphore.acquire()
            with open(fname, "a") as myfile:
                myfile.write(line)

            counter += 1
            semaphore.release()
        except:
            pass

def main():

    for i in range(187):
        url = "http://news.nsysu.edu.tw/files/40-1342-2910-" + str(i + 1) + ".php?Lang=zh-tw"
        titles.put(url)
    threads = []
    for j in range(1):
        c = Parser('c' + str(j))
        c.start()
        threads.append(c)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    tStart = time.time()
    print "start parsing..."
    main()
    tEnd = time.time()
    print 'total numbers of titles : ' + str(counter)
    print 'Cost %d seconds' % (tEnd - tStart)










