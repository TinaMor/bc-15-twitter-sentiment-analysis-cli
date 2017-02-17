"""
 This example uses docopt with the built in cmd module to demonstrate an
 interactive command application.
 
 Usage:
 	tsa get_tweets
 	tsa word_counter
 	tsa sentiment_Analysis
 	tsa emotions_Analysis
 	tsa (-i | --interactive)
 	tsa (-h | --help)
 
 Options:
     -i, --interactive  Interactive Mode
     -h, --help  Show this screen and exit.
 """

import cmd
import os
import sys

from colorama import *
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint

from emotions_analysis import emotions_Analysis
from fetching_user_tweets import *
from sentiment_analysis import sentiment_Analysis

init(wrap=True)

def docopt_cmd(func):
	def fn(self, arg):
		try:
			opt = docopt(fn.__doc__, arg)
		except DocoptExit as error:

		# The DocoptExit is thrown when the args do not match
		# We print a message to the user and the usage block
			print("Invalid Command!")
			print(error)
			return

		except SystemExit:
		# The SystemExit exception prints the usage for --help
		# We do not need to do the print here
			return

		return func(self, opt)

	fn.__name__ = func.__name__
	fn.__doc__ = func.__doc__
	fn.__dict__.update(func.__dict__)
	return fn


class tsa(cmd.Cmd):
	cprint ("\n")
	cprint(figlet_format("Sentiment Analysis".center(15), font = "standard"), "yellow", attrs = ["bold"])

	def introduction():
		""" TSA App commands
		"""
		cprint("\n")
		cprint("TSA COMMAND LIST:".center(30), "green")
		cprint("\n")
		cprint("1. Perform a word-frequency analysis: count".center(10), "green")
		cprint("2. Perform sentiment analysis using the Alchemy API: sentim ".center(10), "green")
		cprint("3. Perform emotion analysis using the Alchemy API: emo".center(10), "green") 
		cprint("4. To quit: quit ".center(10), "green") 

	intro= introduction()
	prompt = "(sentiment analysis)>> "
	file = None


	@docopt_cmd
	def do_count(self, args):
		"""Usage: word_count """
		print(word_counter())

	@docopt_cmd
	def do_sentim(self, args):
		"""Usage: analyse_sentiments """
		print(sentiment_Analysis())
		
	@docopt_cmd
	def do_emo(self, args):
		"""Usage: analyse_emotions"""
		print(emotions_Analysis())
		
	def do_quit(self, arg):
		"""Quits out of Interactive Mode."""

		cprint("Exiting Application. Catch you later!", "red") 
		exit()

if __name__ == "__main__":
	try:
		tsa().cmdloop()
	except KeyboardInterrupt:
		#os.system("clear")
		cprint("Exiting Application. Catch you later!", "red") 