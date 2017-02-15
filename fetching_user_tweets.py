from twython import Twython
import time
from tqdm import tqdm
import json
import sys
import string
import datetime
import re
import stopWords_module
import operator 
from collections import Counter
from tabulate import tabulate

APP_KEY = '911OxmuGGaf2hIqEde5GHWdtt'
APP_SECRET = 'SKikxopjCYagMFWsNAANV2i7I4TAeHpDc4APeJso3ZbbmG2BSF'
OAUTH_TOKEN = '352324203-n1kDEH8yaXGrgPmW6gNLpiorlHyZdhvRkIkiTf1V'
OAUTH_TOKEN_SECRET = 'gPdGUbNJDWFULl0TjImEMkZuvoceGaE01TmHsBH158JZt'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#api = Twitter(auth=OAuth(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET))

def check_no_input():
	# print ("\n\nEnter the number of tweets you want to fetch from the user's timeline")
	num_of_tweets = input("\nThe value should be a positive integer between 1 and 200. Default == 20\t")

		# Check the input for number of tweets to fetch
	if num_of_tweets == '':
		num_of_tweets = 20
		return(num_of_tweets)
	elif str(num_of_tweets).isnumeric() == False: 
		print("\nPlease enter an integer between 1 and 200")
		iters = 0
		while iters < 3:
			if str(num_of_tweets).isnumeric() == False:
				print ("\nYou have ", 3 - iters, ' chance(s) left\n')
				print ("\n\nThe value should be a positive integer between 1 and 200. Default == 20\t")
				num_of_tweets = input('Re-enter value: ')

			else:
				return(num_of_tweets)
			iters += 1
	elif str(num_of_tweets).isnumeric() == True:
		num_of_tweets = int(num_of_tweets)
		#Any values above 200 are defaulted to 200
		if num_of_tweets > 200:
			num_of_tweets = 200
			return(num_of_tweets)
		#Any values less than 1 are defaulted to 1
		elif num_of_tweets < 1:
			num_of_tweets = 1
			return(num_of_tweets)
		else:
			return(num_of_tweets)

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


def user_handle():
	#username = 'TSvelte'
	uName = input("\nEnter user's Twitter handle: ")
	return uName


def get_tweets():

	username = user_handle()
	noOfTweets = check_no_input()

	print('\n-----------------------')
	print('Word frequency for {0} for {1} tweets'.format(username, noOfTweets))
	print('-----------------------\n')

	#user_tweets = twitter.get_home_timeline(screen_name = username, count	= no_of_tweets)
	user_TL= twitter.get_user_timeline(screen_name = username, count = noOfTweets, include_rts = False) # include_retweets

	print ('\n-----------------------', len(user_TL))

	userTL_tweets = []

	#Save the tweets in a JSON file
	for i in tqdm(range(0, len(user_TL)), desc = 'Fetching tweets', unit = 'Tweets'):
		time.sleep(.05)
		with open('userTweets.json', 'w') as outfile:
			for tweet in user_TL:
				userTL_tweets.append(re.sub(r'[^\x00-\x7F]+', '', tweet['text'])) # Remove unicode text

			json.dump(userTL_tweets[1:], outfile)

			return userTL_tweets


def filtered_Posts():

	forbidden_words = stopWords_module.stopWords_list_func()

	tokens_re = forbidden_words[0]
	emoticon_re = forbidden_words[1]
	stop_words = forbidden_words[2]
	punct =  forbidden_words[3]

	status = get_tweets()

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


def word_counter():

    list_of_words = filtered_Posts()
    word_freq = Counter(list_of_words)

    #n = check_common_input()
    oupt = word_freq.most_common(10)

    print (tabulate(oupt, ["WORD", "FREQUENCY"], tablefmt="fancy_grid"))

    # for l in set(list_of_words):
    # 	print ('%s : %d' % (l, word_freq[l]))

    # for letter, count in word_freq.most_common(n):
    # 	return ('%s: %7d' % (letter, count))

get_tweets()