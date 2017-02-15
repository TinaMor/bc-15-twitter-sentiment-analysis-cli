import re
import string

def stopWords_list_func():

# Reference: https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

	punct = list(string.punctuation) # punctuation

	emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
    )"""

	with open('stop_words_list.txt') as f:
		stop_words = f.readlines()

	stopWords = [x.strip() for x in stop_words] 


	regex_str = [
		emoticons_str,
	    r'<[^>]+>', # HTML tags
		r'(?:@[\w_]+)', # @-mentions
		r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
		r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
		r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
		r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
		r'(?:[\w_]+)', # other words
		r'(?:\S)' # anything else
	]

	tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
	emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

	all_stop_words = dict({('tokens_re',tokens_re), ('emoticon_re',emoticon_re), ('stopWords',tuple(stopWords)), ('punct',tuple(punct))})

	return all_stop_words

#