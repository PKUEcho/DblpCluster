# This script calculates the frequency of English words in all paper titles
# for extended stopwords
# Not all words are converted to lower case

import dblp_utility

all_papers, all_authors = dblp_utility.readJsonFile()

filter_words = {'-'}

word_freq = {}

for pUrl in all_papers:
	title = all_papers[pUrl][0]
	words = dblp_utility.title2words(title)
	for w in words:
		if w in filter_words:
			continue
		if not w in word_freq:
			word_freq[w] = 0
		word_freq[w] += 1

sort_word_freq = sorted(word_freq.iteritems(), key = lambda d:d[1], reverse = True)

out_num = 500
out_file = open('data/most_freq_word_in_title', 'w+')

for i in xrange(out_num):
	print sort_word_freq[i][0]
	out_file.write(sort_word_freq[i][0].encode('utf-8') + '\t' + str(sort_word_freq[i][1]) + '\n')

out_file.close()

# for pUrl in all_papers:
# 	title = all_papers[pUrl][0]
# 	title = title.replace(',', '').replace('.', '').lower()
# 	words = title.split(' ')
# 	if '-' in words:
# 		print title