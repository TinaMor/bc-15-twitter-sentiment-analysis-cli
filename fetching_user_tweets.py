import time
import json
import sys
import string
import datetime
import re
import operator 

from collections import Counter
from colorama import *
from pyfiglet import figlet_format
from tabulate import tabulate
from twython import Twython, TwythonError
from termcolor import cprint
from tqdm import tqdm

import stopWords_module


APP_KEY = '911OxmuGGaf2hIqEde5GHWdtt'
APP_SECRET = 'SKikxopjCYagMFWsNAANV2i7I4TAeHpDc4APeJso3ZbbmG2BSF'
OAUTH_TOKEN = '352324203-n1kDEH8yaXGrgPmW6gNLpiorlHyZdhvRkIkiTf1V'
OAUTH_TOKEN_SECRET = 'gPdGUbNJDWFULl0TjImEMkZuvoceGaE01TmHsBH158JZt'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def user_handle(handle = ''):
	handle = input("\nEnter user's Twitter handle: ")
	return handle


def get_tweets(username = '', source = 'function_input'):
	""" Function to fetch tweets
	"""
	if source == 'function_input':
		username = user_handle()

	if username == '':
		print ('\n')
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')
		cprint ('Please enter a valid user Twitter handle', 'cyan')

		tweets_toReturn = {'tweets':'', 'username':'No user name entered'}
		tweets_toReturn = dict(tweets_toReturn)
		return tweets_toReturn

	else:
		try:
			user_TL= twitter.get_user_timeline(screen_name = username, count = 50, include_rts = False) # include_retweets
			

			userTL_tweets = []

			#Save the tweets in a JSON file
			for i in tqdm(range(0, len(user_TL)), desc = 'Fetching tweets', unit = 'Tweets'):
				time.sleep(.05)
				with open('userTweets.json', 'w') as outfile:
					for tweet in user_TL:
						userTL_tweets.append(re.sub(r'[^\x00-\x7F]+', '', tweet['text'])) # Remove unicode text

					json.dump(userTL_tweets, outfile)

			tweets_toReturn = {'tweets':tuple(userTL_tweets), 'username':username}
			tweets_toReturn = dict(tweets_toReturn)

			return tweets_toReturn
			
		except TwythonError as e:
			print ('\n')
			cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')
			print ('Error ', e.error_code, ': User {0} does not exist'.format(username))

			tweets_toReturn = {'tweets':'', 'username':username}
			return tweets_toReturn



def filtered_Posts(status = '', source = 'function_input'):

	""" Function to filter input
	arg source: 1. function_input - from get_tweets() or user_input
	"""
	forbidden_words = stopWords_module.stopWords_list_func()

	tokens_re = forbidden_words['tokens_re']
	emoticon_re = forbidden_words['emoticon_re']
	stop_words = forbidden_words['stopWords']
	punct =  forbidden_words['punct']

	if source == 'user_input':
		status = status['tweets']

	else:
		status = get_tweets()
		status = status['tweets'] #<class 'tuple'>

	if status == '':
		terms_stop = []
		return (terms_stop)

	else:
		filtered_tweets = []

		for i in range(len(status)):

			allWords = tokens_re.findall(status[i])
			allWords = [token if emoticon_re.search(token) else token.lower() for token in allWords]

			filtered_tweets = filtered_tweets + allWords
		
		# Remove stop words. See stop_words_list.txt	
		terms_stop = [text for text in filtered_tweets if text.lower() not in stop_words]

		# Remove any punctuation marks
		terms_stop = [text for text in terms_stop if text.lower() not in punct]

		return terms_stop

def word_counter(list_of_words = '', source = 'function_input'):

	input_source = source

	list_of_words = filtered_Posts(status = '', source = input_source)

	if len(list_of_words) != 0:
		word_freq = Counter(list_of_words)
		oupt = word_freq.most_common(10) #type == list
		print (tabulate(oupt, ["WORD", "FREQUENCY"], tablefmt="fancy_grid"))

	else:
		cprint("No word frequency performed", 'cyan')
		print ('\n')