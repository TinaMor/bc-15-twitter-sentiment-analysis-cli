from fetching_user_tweets import get_tweets
import json
from watson_developer_cloud import AlchemyLanguageV1
import requests

API_KEY = "74432c64897b5ad87a245807459cf995626087d9"

alchemy_language = AlchemyLanguageV1(api_key = API_KEY)

def sentiment_Analysis():

	tweet_posts = get_tweets()

	print('\n-----------------------')
	print('Twitter Sentiment Analysis for {0} for {1} tweets'.format(get_tweets.username, get_tweets.noOfTweets))
	print('-----------------------\n')

	sent_opt = (json.dumps(
		alchemy_language.sentiment(
			text = tweet_posts),
		indent = 2))

	sentimentAnalysis = json.loads(sent_opt)

	score = float(sentimentAnalysis['docSentiment']['score'])
	sentiment_type = sentimentAnalysis['docSentiment']['type']
	#'docSentiment': {'score': '0.496962', 'type': 'positive'}}

	print ("Sentiment Analysis on {0}'s timeline are {1} with a sentiment strength score of {2}".format('username', sentiment_type, score))