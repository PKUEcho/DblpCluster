import requests
import dblp_utility
import dblp_sample_test
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


def filterPunctuation(sentence):
	exclude = set(string.punctuation)
	return ''.join(ch for ch in sentence if ch not in exclude)

# cPapers item format:
# [paper_url, [author1, author2, ...], title, year]
def preProcessing(cPapers):
	stopwords = dblp_utility.extended_stopwords
	res = []
	conference = ''
	title_words = []
	author_names = []
	for paper in cPapers:
		# We extract conference name from paper_url
		conference = dblp_utility.paperUrl2conf(paper[0])

		# Here we have an option whether we should use title
		# title_words = dblp_utility.title2words(paper[2])
		# title_words = [w for w in title_words if w not in stopwords]
		
		# We filter all punctuations here
		author_names = [name.replace(' ', '') for name in paper[1]]
		
		sentence = ' '.join(title_words) + ' ' + ' '.join(author_names) + ' ' + conference
		res.append(filterPunctuation(sentence))
		# print res[-1] + '\n'
	
	return res

def extract_feature(pro_papers):
	# We have done all preprocessing including filtering stopwords beforehand.
	# Set max_df < 1 strictly so we filter the original author name
	# whose papers we want to cluster.
	vect = TfidfVectorizer(
		min_df = 0.01, max_df = 0.99, max_features = 10000, stop_words = None,
		analyzer = "word", preprocessor = None, tokenizer = None,
		use_idf = True, lowercase = True, ngram_range = (1, 1))
	
	tfidf_matrix = vect.fit_transform(pro_papers)
	return 1 - cosine_similarity(tfidf_matrix)


def do_kmeans(matrix, num_clusters):
	km = KMeans(n_clusters = num_clusters)
	km.fit(matrix)
	clusters = km.labels_.tolist()
	return clusters

def print_clusters(result):
	for i in xrange(len(result)):
		one_cluster = result[i]
		print "\nCluster %d: %d" % (i, len(one_cluster))
		for paper in one_cluster:
			print str(paper[2])

def test():
	# test_author = "Yun Ma"
	# all_papers, all_authors = dblp_utility.readJsonFile()
	# test_papers = [all_papers[key] for key in all_authors[test_author]]
	# print test_papers
	test_author = 'Yun Ma'
	num_clusters = 5
	test_papers = dblp_sample_test.dblp_sample_author[test_author]
	papers = preProcessing(test_papers)
	matrix = extract_feature(papers)
	cluster_result = do_kmeans(matrix, num_clusters)
	output_result = []
	for i in xrange(num_clusters):
		one_cluster = [test_papers[k] for k in xrange(len(test_papers)) if cluster_result[k] == i]
		output_result.append(one_cluster)
	print_clusters(output_result)

def main():
	pass

action = "test"

if __name__ == '__main__':
	if action == 'test':
		test()
	else:
		main()