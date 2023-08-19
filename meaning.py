from gibberish_detector import detector
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import string
import itertools
import time
from multiprocessing import Pool
from multiprocessing import get_context
import multiprocessing
from tqdm import tqdm
import os

#4 walls
#5 shelves
#32 volumes
#410 pages

def main(location, n):
	os.system('cls')
	session = requests.Session()
	retry = Retry(total=20, connect=5, backoff_factor=0.2)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	f1 = open("meaning.txt","a", encoding="UTF-8")
	Detector = detector.create_from_model('gibberish-detector.model')
	lock = RLock()

	def page_extractor(page_content):
		pattern = r'<PRE id = "textblock">(.*?)</PRE>'
		match = re.search(pattern, page_content, re.DOTALL)

		if match:
			page_extracted = match.group(1)
			return page_extracted
		else:
			return None

	def pager(url):
		try:
			while True:
				try:
					s = session.get(url, timeout=300)
					s.close()
					page = page_extractor(s.text)
					if page == None:
						time.sleep(0.1)
						continue
					else:
						break
				except:
					time.sleep(0.1)
					continue

			with lock1:
				pbar.update(1)
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
	try:
		with tqdm(total=len(urls), desc="fetching hexagon: "+location, leave=False, position=n, unit="pages") as pbar:
			with ThreadPoolExecutor(max_workers=44) as executor: #maintain the following number of threads or change it if it takes a toll on your machine, if you have a machine with a high number of threads then increase it if not don't.
				executor.map(pager,urls)
	except Exception as e:
		print(e)

	completed_hexagons = open("hexagons_done.txt","a")
	completed_hexagons.write(location+"\n")
	completed_hexagons.close()
	f.close()
	f1.close()

def init(l):
    global lock1
    lock1 = l

if __name__ == '__main__':
	try:
		with open("hexagons_done.txt","r") as filename:
			already_completed = [ele.replace("\n","") for ele in filename.readlines()]

		combinations = [ "".join(element) for element in itertools.product(list(string.ascii_lowercase+string.digits), repeat=2)]#Modify the given digit for example 2 to any number that you like to achieve your desired combinations.
		locations = sorted(list(set(combinations)-set(already_completed)))
		l = multiprocessing.RLock()
		pool = get_context("spawn").Pool(5, initializer=init, initargs=(l,)) #The number 5 represents the number of processes. Modify the number depending on your machine. If left empty, it will utilize the entirety of available cores, but I recommend leaving at least 4 cores for your system.
		n = 0
		for location in locations:
			pool.apply_async(main, args=(location,n,))
			n += 1
			if n == 10:
				n = 0
		pool.close()
		pool.join()
	except Exception as e:
		print(e)
