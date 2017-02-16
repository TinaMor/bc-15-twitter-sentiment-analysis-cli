import json
import requests

from colorama import *
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from tabulate import tabulate
from termcolor import cprint
from watson_developer_cloud import AlchemyLanguageV1

from fetching_user_tweets import get_tweets


API_KEY = "74432c64897b5ad87a245807459cf995626087d9"

alchemy_language = AlchemyLanguageV1(api_key = API_KEY)

def emotions_Analysis(tweet_posts = ''):

	status = get_tweets()

	tweet_posts = status['tweets']
	uname = status['username']

	if tweet_posts == '':
		print ("Emotion Analysis on {0}'s timeline not performed".format(uname))
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')

	else:
		print ('\n')
		cprint ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', 'magenta')
		print('Twitter Emotion Analysis for {0} tweets'.format(uname))

		emotions_opt = (json.dumps(
			alchemy_language.emotion(
				text = tweet_posts),
			indent = 2))

		emotionsAnalysis = json.loads(emotions_opt)
		emotionsDict = emotionsAnalysis['docEmotions']
		# Sort and convert to alist for tabulation
		emotionsList = [(k, emotionsDict[k]) for k in sorted(emotionsDict, key=emotionsDict.get, reverse=True)]

		print (tabulate(emotionsList, ["EMOTION", "SCORE"], tablefmt="fancy_grid"))
		print ('\n')