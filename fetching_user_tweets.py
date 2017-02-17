import time
import json
import sys
import string
import datetime
import re
import operator 
import os

from collections import Counter
from colorama import *
from pyfiglet import figlet_format
from tabulate import tabulate
from twython import Twython, TwythonError
from termcolor import cprint
from tqdm import tqdm

from create_stop_words_list import stop_words


APP_KEY = '911OxmuGGaf2hIqEde5GHWdtt'
APP_SECRET = 'SKikxopjCYagMFWsNAANV2i7I4TAeHpDc4APeJso3ZbbmG2BSF'
OAUTH_TOKEN = '352324203-n1kDEH8yaXGrgPmW6gNLpiorlHyZdhvRkIkiTf1V'
OAUTH_TOKEN_SECRET = 'gPdGUbNJDWFULl0TjImEMkZuvoceGaE01TmHsBH158JZt'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def user_handle(username = ''):
	username = input("\nEnter user's Twitter handle: ")
	return username


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
			user_TL= twitter.get_user_timeline(screen_name = username, count = 1) # a dict inside a list

			#tweet id for the last tweet
			last_tweet_id = [dict(user_TL[0])['id']]

			#specify the max_id as the last item in the list (the last tweet id from each extraction).
			user_TL= twitter.get_user_timeline(screen_name = username, count = 50, include_rts = False, max_id=last_tweet_id[-1])

			# 10 secone rest between api calls
			#time.sleep(10)

			userTL_tweets = []

			#Save the tweets in a JSON file
			for i in tqdm(range(0, len(user_TL)), desc = 'Fetching tweets', unit = 'Tweets'):
				time.sleep(.05)
				for tweet in user_TL:
					userTL_tweets.append(re.sub(r'[^\x00-\x7F]+', '', tweet['text'])) # Remove unicode text

			with open('userTweets.json', 'w') as outfile:
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



def filtered_posts(status = '', source = 'function_input'):

	""" Function to filter input
	arg source: 1. function_input - from get_tweets() or user_input
	"""
	all_stop_words = stop_words()

	tokens_re = all_stop_words['tokens_re']
	emoticon_re = all_stop_words['emoticon_re']
	bad_words = all_stop_words['stop_words']
	punct = all_stop_words['punct']
	email_regex = all_stop_words['email_regex']

	if source == 'user_input':
		status = status['tweets']

	else:
		status = get_tweets()
		status = status['tweets'] #<class 'tuple'>

	if status == '':
		filtered_tweets = []
		return filtered_tweets

	else:
		filtered_tweets = []

		join_tweets = status
		join_tweets = ''.join(join_tweets)

		emails_in_tweet = email_regex.findall(join_tweets)
		emails = []
		if len(emails_in_tweet) > 0:

			for e in range(len(emails_in_tweet)):
				emails.append(emails_in_tweet[e][0].lower())

			for e in emails:
				join_tweets = re.sub(e, '', join_tweets.lower())
				join_tweets = re.sub(r'\s', ' ', join_tweets)

		allWords = tokens_re.findall(join_tweets)
		allWords = [token if emoticon_re.search(token) else token.lower() for token in allWords]
		
		# Remove stop words. See stop_words_list.txt	
		filtered_tweets = [text for text in allWords if text.lower() not in bad_words]

		# Remove any punctuation marks
		filtered_tweets = [text for text in filtered_tweets if text.lower() not in punct]

		filtered_tweets = filtered_tweets + emails

		return filtered_tweets

def word_counter(list_of_words = '', source = 'function_input'):

	input_source = source

	list_of_words = filtered_posts(status = '', source = input_source)

	if len(list_of_words) != 0:
		word_freq = Counter(list_of_words)
		oupt = word_freq.most_common(10) #type == list
		print (tabulate(oupt, ["WORD", "FREQUENCY"], tablefmt="fancy_grid"))

	else:
		cprint("No word frequency performed", 'cyan')
		print ('\n')