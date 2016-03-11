#nonstandard libraries
import requests
from nltk import sent_tokenize, word_tokenize

#standard libraries
import string
import time
import os
from collections import Counter

WINDOW = 50
PUNCTUATION = string.punctuation 
WHTIESPACE = string.whitespace

CWD = os.path.dirname(os.path.realpath(__file__))
CLIFF_URL = "www.your.cliff.url.com"


def find_places(text):
	"""
	This function uses CLIFF (http://cliff.mediameter.org/) to 
	find place names from the input text.  Note that an error will 
	be returned if the url is too large (roughly 1,500 characters), 
	so it might be necessary to chunk the input text.

	The returned array contains tuples contain the place name 
	mentioned in the text and the official place name in CLIFF:

	Ex:  [('NYC', 'New_York_City'), ('L.A.', 'Los_Angeles')...]
	"""

	result = requests.post(CLIFF_URL, params={'q': text})

	if not result.ok:
		raise Exception("Cliff error!")

	result_json = result.json()['results']
	mentions = result_json['places']['mentions']
	
	return [(mention['source']['string'], mention['name'].replace(' ', '_')) for mention in mentions]


def persist(func, *args, **kwargs):
	"""
	This function will persist in calling func until successful.  
	This is used to handle errors that CLIFF sometimes throws.
	"""

	short_wait = kwargs.pop('short_wait', 1.5)
	long_wait = kwargs.pop('long_wait', 10.0)

	while True:
		try:
			time.sleep(short_wait)
			return func(*args)
		except:
			time.sleep(long_wait)
		else: 
			break


def chunk_text(text, chunk_size=1000):
	"""
	This function chunks text to avoid url-too-long errors.
	Note: This should be slicker, as it currently doesn't ensure 
	words aren't split if they fall on a boundary. 
	"""

	words = text.split()
	indx = 0

	while indx < len(words):
		chunk = ''

		#infinite loop if one word is larger than chunk_size!
		while len(chunk) <= chunk_size and indx < len(words)
			chunk = chunk + ' ' + words[indx]
			indx += 1

		yield chunk.strip()


def replace_chars(text, replace_with=u' ', replace_chars=WHTIESPACE):
	"""
	This function is used to replace bad characters
	(which for now means white space).
	"""

	if isinstance(text, unicode):
		translations = dict((ord(char), replace_with) for char in replace_chars)
		return text.translate(translations)

	return text.translate(None, replace_chars)


def clean_text(text):
	"""
	Right now this just replaces whitespace, but might also
	try to correct spelling errors from OCR?
	"""
	
	return replace_chars(text)


"""
The following functions are used to collect data from the Chronicling
America API (http://chroniclingamerica.loc.gov)
"""

def get_dates(lccn):
	"""
	Get all issue dates for a given lccn ID.
	"""

	url = "http://chroniclingamerica.loc.gov/lccn/{0}.json".format(lccn)

	return [issue['date_issued'] for issue in requests.get(url).json()['issues']]


def get_issue(lccn, date):
	"""
	Get issue text from the Chronicling America API.  Right now, 
	it assumes you know the lccn (ID for a newspaper) and the issue 
	date.
	"""

	url = "http://chroniclingamerica.loc.gov/lccn/{0}/{1}/ed-1.json".format(lccn, date)

	page_urls = [p['url'] for p in requests.get(url).json()['pages']]
	ocr_urls = [requests.get(url).json()['text'] for url in page_urls]

	return ' '.join([requests.get(url).text for url in ocr_urls])


def get_issues_by_year(lccn, year):
	"""
	Returns one long document that includes all of the issues
	for a given year.
	"""

	dates = [date for date in get_dates(lccn) if date.find(year) <> -1]

	return ' '.join([get_issue(lccn, date) for date in dates])




if __name__ == '__main__':
	"""
	Typical usage:
	"""

	#lccn is the newspaper identifier (in this case, the Aberdeen Herald)
	lccn = 'sn87093220'
	years = ['1907']

	for year in years:
		print "starting year", year

		print "getting issues..."
		document = get_issues_by_year(lccn, year)
		document = clean_text(document)

		print "finding places..."

		place_translator = dict((original, official) for chunk in chunk_text(document) for original, official in persist(find_places, chunk))
		places = place_translator.values()
		
		#convert all place names in the original text to the official CLIFF name in order to standardize
		document = reduce(lambda x, y: x.replace(y, place_translator.get(y, y)), place_translator, document)

		#tokenize words
		words = [word for sent in sent_tokenize(issue) for word in word_tokenize(sent) if word not in PUNCTUATION]	

		#find cooccurrences (better way to do this?)
		cooccurrences = Counter((center, neighbor) for i, center in enumerate(words) if center in places 
	 											for neighbor in words[max(0, i-WINDOW):i+WINDOW+1] if neighbor <> center and neighbor in places)

		print "writing files..."

		f = open(os.path.join(CWD, "{}_{}_issues.txt".format(lccn, year)), "w")
		f.write(document)
		f.close()

		f = open(os.path.join(CWD, "{}_{}_places.txt".format(lccn, year)), "w")
		f.write('\n'.join(places))
		f.close()

		#Cooccurrences are CSV format: a,b,w (connection from 'a' to 'b', with weight 'w')
		f = open(os.path.join(CWD, "{}_{}_cooccurrences.csv".format(lccn, year)), "w")
		f.write('\n'.join(["{0},{1},{2}".format(places[0], places[1], count) for places, count in cooccurrences.most_common()]))
		f.close()	

