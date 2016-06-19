from bs4 import BeautifulSoup
import gzip
import json
import nltk

extended_stopwords = nltk.corpus.stopwords.words('english') + [
	'using', 'based', 'approach'
	# Add more!
]

def title2words(title):
	return title.replace(',', '').replace('.', '').lower().split(' ')

def paperUrl2conf(pUrl):
	return pUrl[:pUrl.rfind('/')]

def readJsonFile():
	print "Reading total json from file to memory..."
	print "It may take several minutes"
	content = gzip.open('data/dblp.json.gz').read()
	papers = json.loads(content)
	authors = {}
	for i in xrange(len(papers)):
		for author in papers[i][1]:
			if not author in authors:
				authors[author] = []
			authors[author].append(i)
	print "Finish reading json file"
	return papers, authors

def author2url(author):
	url = ''
	items = author.strip().split(' ')
	url += (items[-1] + ':')
	del items[-1]
	url += '_'.join(items)
	url = url.replace('.', '=')
	return 'http://dblp.uni-trier.de/pers/hd/' + url[0].lower() + '/' + url


def parseAuthorPage(response):
	papers = []
	soup = BeautifulSoup(response.text, 'lxml')
	divs = soup.find_all('div', attrs = {'class': 'data', 'itemprop': 'headline'})
	for div in divs:
		# print div
		new_paper = {}
		# Find all coauthors
		coauthors_span = div.find_all('span', attrs = {'itemprop': 'author'})
		new_paper['authors'] = [a_span.text for a_span in coauthors_span]
		# Find the paper title
		title_span = div.find('span', attrs = {'class': 'title', 'itemprop': 'name'})
		new_paper['title'] = title_span.text
		# Find the Conference/Journal
		temp_span = div.find('span', attrs = {'itemprop': 'isPartOf'})
		if temp_span == None:
			new_paper['conf'] = ''
		else:
			conf_span = temp_span.find('span', attrs = {'itemprop': 'name'})
			new_paper['conf'] = conf_span.text
		# Find the publis year
		year_span = div.find('span', attrs = {'itemprop': 'datePublished'})
		new_paper['year'] = year_span.text

		papers.append(new_paper)
	return papers