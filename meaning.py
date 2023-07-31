from gibberish_detector import detector
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import string
import itertools
import time
from multiprocessing import Pool

#4 walls
#5 shelves
#32 volumes
#410 pages

def main(location):
	session = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	f1 = open("meaning.txt","a", encoding="UTF-8")
	Detector = detector.create_from_model('gibberish-detector.model')
	lock = Lock()

	def pager(url):
		try:
			try:
				s = session.get(url)
				soup = BeautifulSoup(s.content, "html.parser")
				page = soup.find('pre',{"id":"textblock"}).text
			except:
				s = session.get(url)
				soup = BeautifulSoup(s.content, "html.parser")
				if soup.find('pre',{"id":"textblock"}) == None:
					while True:
						s = session.get(url)
						if s.status_code == 200:
							soup = BeautifulSoup(s.content, "html.parser")
							page = soup.find('pre',{"id":"textblock"}).text
							break
						else:
							continue
				else:
					soup = BeautifulSoup(s.content, "html.parser")
					page = soup.find('pre',{"id":"textblock"}).text


			if Detector.is_gibberish(page) == True:
				with lock:
					f.write(url.replace("https://libraryofbabel.info/book.cgi?","").replace(":","-p")+"\n")
			else:
				with lock:
					f1.write(url.replace("https://libraryofbabel.info/book.cgi?","").replace(":","-p")+"\n")
		except Exception as e:
			print(e)

	f = open(r"gibberish\hexagon-"+location+".txt","a", encoding="UTF-8")
	urls = ["https://libraryofbabel.info/book.cgi?"+str(location)+"-w"+str(wall)+"-s"+str(shelf)+"-v"+str("0"+str(volume))+":"+str(page)+"" if volume<10 else "https://libraryofbabel.info/book.cgi?"+str(location)+"-w"+str(wall)+"-s"+str(shelf)+"-v"+str(str(volume))+":"+str(page)+""for wall in range(1, 5) for shelf in range(1, 6) for volume in range(1, 33) for page in range(1, 411)]
	with ThreadPoolExecutor(max_workers=44) as executor:#maintain the following number of threads or change it if it takes a toll on your machine, if you have a machine with a high number of threads then increase it if not don't.
		executor.map(pager,urls)
	print("completed fetching hexagon: "+location)
	completed_hexagons = open("hexagons_done.txt","a")
	completed_hexagons.write(location+"\n")
	completed_hexagons.close()
	f.close()
	f1.close()

if __name__ == '__main__':
	with open("hexagons_done.txt","r") as filename:
		already_completed = [ele.replace("\n","") for ele in filename.readlines()]

	combinations = [ "".join(element) for element in itertools.product(list(string.ascii_lowercase+string.digits), repeat=2)]#Modify the given digit for example 2 to any number that you like to achieve your desired combinations.
	locations = sorted(list(set(combinations)-set(already_completed)))
	pool = Pool(5) #The number 5 represents the number of processes. Modify the number depending on your machine. If left empty, it will utilize the entirety of available cores, but I recommend leaving at least 4 cores for your system.
	for location in locations:
		pool.apply_async(main, args=(location,))
	pool.close()
	pool.join()
