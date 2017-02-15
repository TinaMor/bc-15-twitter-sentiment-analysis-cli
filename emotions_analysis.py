from fetching_user_tweets import get_tweets
import json
from watson_developer_cloud import AlchemyLanguageV1
import requests
from tabulate import tabulate


API_KEY = "74432c64897b5ad87a245807459cf995626087d9"

alchemy_language = AlchemyLanguageV1(api_key = API_KEY)

def emotions_Analysis():

	status = get_tweets()

	tweet_posts = status['tweets']
	uname = status['username']

	print('\n-----------------------')
	print('Twitter Emotion Analysis for {0} tweets'.format(uname))
	print('-----------------------\n')

	emotions_opt = (json.dumps(
		alchemy_language.emotion(
			text = tweet_posts),
		indent = 2))

	emotionsAnalysis = json.loads(emotions_opt)
	emotionsDict = emotionsAnalysis['docEmotions']
	# Sort and convert to alist for tabulation
	emotionsList = [(k, emotionsDict[k]) for k in sorted(emotionsDict, key=emotionsDict.get, reverse=True)]

	print (tabulate(emotionsList, ["EMOTION", "SCORE"], tablefmt="fancy_grid"))

#emotions_Analysis()