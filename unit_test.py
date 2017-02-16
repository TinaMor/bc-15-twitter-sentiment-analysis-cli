import unittest

from functions import *
from sentiment_analysis import sentiment_Analysis

class API_tests(unittest.TestCase):

    def test_if_stopwords_removed(self):
		#Test tweets
    	sampleTweets = {'tweets': ("RT Margit's Note: Yearning to Breathe Free https://t.co/fQfkI9Jut8 via @TueNight @margit #refugeeswelcome #firstnameclub", 'This play is going to be the best thing to happen in 2017!!! Mark my words!! #BeiYaJioni')}

    	result = ["margit's", 'note', 'yearning', 'breathe', 'free', 'https://t.co/fqfki9jut8', '@tuenight', '@margit', '#refugeeswelcome', '#firstnameclub', 'play', 'going', 'best', 'thing', 'happen', '2017', 'mark', 'words', '#beiyajioni']

    	self.assertEqual (result, filtered_Posts(sampleTweets, source = 'user_input'), "The output is incorrect")


    def test_correctness_of_sentiment_analysis(self):
    	sampleTweets = {'tweets': ("RT Margit's Note: Yearning to Breathe Free https://t.co/fQfkI9Jut8 via @TueNight @margit #refugeeswelcome #firstnameclub", 'This play is going to be the best thing to happen in 2017!!! Mark my words!! #BeiYaJioni')}

    	computed_result = sentiment_Analysis(sampleTweets, source = 'user_input') #646624

    	self.assertEqual (0.646624, float(re.findall('0.[0-9]*', computed_result)[0]), "The output is incorrect")

if __name__ == '__main__':
    unittest.main()