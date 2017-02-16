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
#api = Twitter(auth=OAuth(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET))

# def check_no_input():
# 	# print ("\n\nEnter the number of tweets you want to fetch from the user's timeline")
# 	num_of_tweets = input("\nThe value should be a positive integer between 1 and 200. Default == 20\t")

# 		# Check the input for number of tweets to fetch
# 	if num_of_tweets == '':
# 		num_of_tweets = 20
# 		return(num_of_tweets)
# 	elif str(num_of_tweets).isnumeric() == False: 
# 		print("\nPlease enter an integer between 1 and 200")
# 		iters = 0
# 		while iters < 3:
# 			if str(num_of_tweets).isnumeric() == False:
# 				print ("\nYou have ", 3 - iters, ' chance(s) left\n')
# 				print ("\n\nThe value should be a positive integer between 1 and 200. Default == 20\t")
# 				num_of_tweets = input('Re-enter value: ')

# 			else:
# 				return(num_of_tweets)
# 			iters += 1
# 	elif str(num_of_tweets).isnumeric() == True:
# 		num_of_tweets = int(num_of_tweets)
# 		#Any values above 200 are defaulted to 200
# 		if num_of_tweets > 200:
# 			num_of_tweets = 200
# 			return(num_of_tweets)
# 		#Any values less than 1 are defaulted to 1
# 		elif num_of_tweets < 1:
# 			num_of_tweets = 1
# 			return(num_of_tweets)
# 		else:
# 			return(num_of_tweets)

"""
def check_common_input():
	# print ("\n\nEnter the number of tweets you want to fetch from the user's timeline")
	most_common_input = input("\nPlease enter a positive integer\t")

		# Check the input for number of tweets to fetch
	if str(most_common_input).isnumeric() == False:
		print("\nPlease enter a positive integer")
		iters = 0
		while iters < 1:
			if str(most_common_input).isnumeric() == False:
				print ("\nThe value should be a positive integer\t")
				most_common_input = input('Re-enter value: ')

			else:
				return(most_common_input)
			iters += 1
	elif str(most_common_input).isnumeric() == True:
		most_common_input = int(most_common_input)
		#Any values above 200 are defaulted to 200
		if most_common_input < 1:
			most_common_input = None
			return(most_common_input)
		else:
			return(most_common_input)
"""

def user_handle():
	uName = input("\nEnter user's Twitter handle: ")
	return uName


def get_tweets():

	username = user_handle()
	#noOfTweets = check_no_input()

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

		#toReturn = {('tweets',tuple(userTL_tweets)), ('username', username), ('noOfTweets', noOfTweets)}
		tweets_toReturn = {('tweets',tuple(userTL_tweets)), ('username', username)}
		tweets_toReturn = dict(tweets_toReturn)

		return tweets_toReturn
		
	except TwythonError as e:
		print ('\n')
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')
		print ('Error ', e.error_code, ': User {0} does not exist'.format(username))

		tweets_toReturn = {('tweets',''), ('username', username)}
		tweets_toReturn = dict(tweets_toReturn)

		return tweets_toReturn



def filtered_Posts(status = ''):

	forbidden_words = stopWords_module.stopWords_list_func()

	tokens_re = forbidden_words['tokens_re']
	emoticon_re = forbidden_words['emoticon_re']
	stop_words = forbidden_words['stopWords']
	punct =  forbidden_words['punct']


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

			filtered_TL = []
			word_tokens = (status[i]).split()
			#filtered_TL = [w for w in word_tokens.encode('utf-8').lower() if not w in stop_words]
			filtered_TL = [w for w in word_tokens if not w in filtered_tweets]

			#filtered_tweets.append(filtered_TL)
			
			filtered_tweets = filtered_tweets + allWords


		terms_stop = [text for text in filtered_tweets if text.lower() not in stop_words]
		terms_stop = [text for text in terms_stop if text.lower() not in punct]

		return (terms_stop)

def word_counter(list_of_words = ''):


    list_of_words = filtered_Posts()

    if len(list_of_words) != 0:
    	word_freq = Counter(list_of_words)
    	oupt = word_freq.most_common(10) #type == list
    	print (tabulate(oupt, ["WORD", "FREQUENCY"], tablefmt="fancy_grid"))

    else:
    	cprint("No word frequency performed", 'cyan')
    	print ('\n')

#word_counter()