from fetching_user_tweets import get_tweets
import json
from watson_developer_cloud import AlchemyLanguageV1

API_KEY = "74432c64897b5ad87a245807459cf995626087d9"

alchemy_language = AlchemyLanguageV1(api_key='API_KEY')
link = 'https://twitter.com/'


def sentiment_Analysis():

	print('\n-----------------------')
	print('Twitter Sentiment Analysis for {0} for {1} tweets'.format(username, noOfTweets))
	print('-----------------------\n')

	tweet_posts = fetching_user_tweets.get_tweets()

	alchemy_language = AlchemyLanguageV1(api_key='API_KEY')
	sent_opt = (json.dumps(
		alchemy_language.sentiment(
			text = tweet_posts),
		indent = 2))

	sentimentAnalysis = json.loads(sent_opt)

	print (type(sentimentAnalysis))

