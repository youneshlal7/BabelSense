# BabelSense
BabelSense is a project that aims to explore and uncover meaningful pages within the vast expanse of the Library of Babel. The Library of Babel is a website created by Jonathan Basile and inspired by the fictional universe created by Jorge Luis Borges, where an infinite library that is finite in nature contains every possible combination of the 26 latin letters plus the dot, comma and space.
# How it works

BabelSense is a Python program designed to scrape [Jonathan Basile's website](libraryofbabel.info) using 'requests' and 'BeautifulSoup' libraries. The program uses 'requests' to retrieve HTML content and 'BeautifulSoup' to parse the HTML and extract individual book pages from the library's hexagons.

The Library of Babel is structured with 4 walls, each wall containing 5 shelves, and each shelf housing 32 volumes. Each volume consists of 410 pages. To efficiently retrieve these pages, we employ list comprehension to create each of the 262,400 URLs required for parsing and extracting the content.

Hexagons in the library are uniquely identified using a combination of 36 letters and numbers (0-9, a-z). By employing 'itertools.product' in Python, which utilizes the Cartesian product, we efficiently create a list of locations of each hexagon.

To determine if a page contains meaningful content, we employ a [gibberish detector model](https://github.com/domanchi/gibberish-detector) based on [markov chain](https://en.wikipedia.org/wiki/Markov_chain). If the model returns 'True,' indicating gibberish, the page's location is recorded in the 'gibberish' folder. Conversely, if the model returns 'False,' indicating meaningful content, the location is recorded in the 'meaning.txt' file.

Performance was a priority during development, and the program takes advantage of parallel processing by running five instances simultaneously (you can adjust this based on your machine's core count in line 77 of 'meaning.py'). Each instance processes a hexagon with 44 threads, effectively increasing the number of URLs parsed concurrently (you can modify the thread count in line 62 of 'meaning.py').

Once the BabelSense Python program completes its parsing process and extracts the relevant content from each hexagon, the program records the location of each processed hexagon in the 'hexagons_done.txt' file. This ensures that during the next run of the program, previously processed hexagons won't be repeated, avoiding duplication of effort. By maintaining this log, BabelSense optimizes the retrieval process and ensures a more efficient exploration of the Library of Babel, focusing solely on the remaining unexplored hexagons in subsequent runs.
