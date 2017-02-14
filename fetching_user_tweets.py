from twython import Twython
import time
from tqdm import tqdm
import json
import sys
import string
import datetime

APP_KEY = '911OxmuGGaf2hIqEde5GHWdtt'
APP_SECRET = 'SKikxopjCYagMFWsNAANV2i7I4TAeHpDc4APeJso3ZbbmG2BSF'
OAUTH_TOKEN = '352324203-n1kDEH8yaXGrgPmW6gNLpiorlHyZdhvRkIkiTf1V'
OAUTH_TOKEN_SECRET = 'gPdGUbNJDWFULl0TjImEMkZuvoceGaE01TmHsBH158JZt'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#api = Twitter(auth=OAuth(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET))

def check_no_input():
	# print ("\n\nEnter the number of tweets you want to fetch from the user's timeline")
	num_of_tweets = input("The value should be a positive integer between 1 and 200. Default == 20\t")

		# Check the input for number of tweets to fetch
	if num_of_tweets == '':
		num_of_tweets = 20
		return(num_of_tweets)
	elif str(num_of_tweets).isnumeric() == False: 
		print("Please enter an integer between 1 and 200")
		iters = 0
		while iters < 3:
			if str(num_of_tweets).isnumeric() == False:
				print ("\nYou have ", 3 - iters, ' chance(s) left\n')
				print ("\n\nThe value should be a positive integer between 1 and 200. Default == 20\t")
				num_of_tweets = input('Re-enter value: ')

			else:
				break
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

def user_handle():
	#username = 'TSvelte'
	uName = input("Enter user's Twitter handle: ")
	return uName

def get_tweets():

	username = user_handle()
	noOfTweets = check_no_input()
	#no_of_tweets = 2

	#user_tweets = twitter.get_home_timeline(screen_name = username, count	= no_of_tweets)
	user_TL= twitter.get_user_timeline(screen_name = username, count = noOfTweets, include_rts = False) # include_retweets

	userTL_tweets = []

	#Save the tweets in a JSON file
	for i in tqdm(range(0, len(user_TL)), desc = 'Fetching tweets'):
		time.sleep(.5)
		with open('userTweets.json', 'w') as outfile:
			for tweet in user_TL:
				userTL_tweets.append(tweet['text'])

			json.dump(userTL_tweets[1:], outfile)

			return user_TL



def remove_stop_words():

	with open('stop_words_list.txt') as f:
		stop_words = f.readlines()

	stopWords = [x.strip() for x in stop_words] 

	user_TL = get_tweets()

	filtered_tweets = []

	for i in range(len(user_TL)):
		filtered_TL = []
		word_tokens = (user_TL[i]).split()
		filtered_TL = [w for w in word_tokens if not w in stop_words]
		filtered_tweets.append(filtered_TL)

	print (filtered_tweets)







def sentiment_analysis():

	print('\n-----------------------')
	print('Twitter Sentiment Analysis for {0} for {1} tweets'.format(username, noOfTweets))
	print('-----------------------\n')

	pass
	
#remove_stop_words()
get_tweets()