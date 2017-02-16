import json
import requests

from colorama import *
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint
from watson_developer_cloud import AlchemyLanguageV1

from fetching_user_tweets import get_tweets


API_KEY = "74432c64897b5ad87a245807459cf995626087d9"

alchemy_language = AlchemyLanguageV1(api_key = API_KEY)

def sentiment_Analysis(tweet_posts = ''):

	status = get_tweets()

	tweet_posts = status['tweets']
	uname = status['username']

	if tweet_posts == '':
		print ("Sentiment Analysis on {0}'s timeline not performed".format(uname))
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')

	else:
		print ('\n')
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')
		print('Twitter Sentiment Analysis for {0} tweets'.format(uname))

		sent_opt = (json.dumps(
			alchemy_language.sentiment(
				text = tweet_posts),
			indent = 2))


		sentimentAnalysis = json.loads(sent_opt)
		sentiment_type = sentimentAnalysis['docSentiment']['type']

		if sentiment_type == 'neutral':
			score = float(0)
		else:
			score = float(sentimentAnalysis['docSentiment']['score'])


		print ("Sentiment Analysis on {0}'s timeline are {1} with a sentiment strength score of {2}".format(uname, sentiment_type, score))
		print ('\n\n')

#sentiment_Analysis()