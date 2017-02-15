
# Functions:
# 	get_tweets
# 	word_counter
# 	emotions_Analysis
# 	sentiment_Analysis

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

import sys
import cmd
import os
from docopt import docopt, DocoptExit
from emotions_analysis import emotions_Analysis
from fetching_user_tweets import *
from termcolor import cprint
from pyfiglet import figlet_format
from sentiment_analysis import sentiment_Analysis


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
	cprint(figlet_format("TSA".center(10), font = "standard"), "yellow", attrs = ["bold"])

	def introduction():
		""" TSA App commands
		"""
		cprint("\n")
		cprint("TSA COMMAND LIST:", "green")
		cprint("\n")
		cprint("1. To fetch tweets use the command fetch_tweets", "green")
		cprint("2. word_count", "green")
		cprint("3. word_count", "green")
		cprint("4. word_count", "green")

	intro= introduction()
	prompt = "(tsa) "
	file = None


	@docopt_cmd
	def do_fetch_tweets(self, args):
		"""Usage: fetch_tweets """
		print(get_tweets())

	def do_word_count(self, args):
		"""Usage: word_count """
		print(word_counter())

	def do_analyse_sentiments(self, args):
		"""Usage: analyse_sentiments """
		print(sentiment_Analysis())

	def do_analyse_emotions(self, args):
		"""Usage: analyse_emotions"""
		print(emotions_Analysis())

	def do_quit(self, arg):
		"""Quits out of Interactive Mode."""

		print("Exiting Application. Catch you later!")
		exit()

if __name__ == "__main__":
	try:
		tsa().cmdloop()
	except KeyboardInterrupt:
		os.system("clear")
		print('Application Exiting')

# opt = docopt(__doc__, sys.argv[1:])

# if opt['--interactive']:
# 	tsa().cmdloop()

# print (opt) 