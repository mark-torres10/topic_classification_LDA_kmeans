import numpy as np
import csv
import string
import nltk
from nltk.corpus import stopwords
import tweepy
import re 
import sys

###### The goal of this script is to get the tweets and documents necessary for the project #######
###### I will get the users who tweeted about a certain topic (here, climate change) and create 
###### documents of all of their tweets to get an idea of the topics that they are tweeting about #####

###### Input: uncleaned tweets
###### Output: cleaned tweets

def remove_punctuations(text):
	"""
		Function: removes punctuation from a line of text
	"""

	# remove punctuation
	for punctuation in string.punctuation:
		text = [''.join(c for c in s if c not in string.punctuation) for s in text]

	# get clean text
	cleaned_text = ''.join(text)

	# return clean text
	return cleaned_text

def remove_links(tweet):
	"""
		Function: takes a string and removes web links from it
	"""
	tweet = re.sub(r'http\S+', '', tweet) # remove http links
	tweet = re.sub(r'bit.ly/\S+', '', tweet) # rempve bitly links
	tweet = tweet.strip('[link]') # remove [links]
	return tweet

def remove_users(tweet):
	"""
		Function: takes a string and removes retweet and @user information
	"""
	tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet
	tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove tweeted at
	return tweet

def main():

	###### import data ######
	data_dir = "../data/labeled_tweets_climateChange.csv"

	# keep tweets in array:
	tweet_text = []

	with open(data_dir) as csv_file:
		readCSV = csv.reader(csv_file, delimiter = ',')

		# iterate by row
		for row in readCSV:
			# append to array that holds tweets
			tweet_text.append(row[1])

	# print length of array
	print("The length of the tweet array is: ", len(tweet_text))

	# test functions
	#test_text = "This, is.... a; sample: tweet"
	#print("Original sample tweet: ", test_text)
	#print("Tweet with no punctuation: ", remove_punctuations(test_text))

	#test_text = "This has a link http://www.worldwideweb.com check it out!"
	#print("Original sample tweet: ", test_text)
	#print("Tweet with no link: ", remove_links(test_text))
	#sys.exit("Finished testing")

	######  clean text ######

	# get stopwords list
	stopwords_list = nltk.corpus.stopwords.words('english')

	# convert to lowercase
	lowercase_tweets = [text.lower() for text in tweet_text]

	# print example tweet
	print("Example lowercase tweet : ", lowercase_tweets[2])

	# remove stopwords
	#tweets_no_stopwords = [word for word in tweet if word not in stopword_set for tweet in lowercase_tweets]

	# outer layer
	#[tweet for tweet in lowercase_tweets]

	# inner layer
	#[word for word in tweet if word not in stopword_set]

	# remove punctuation
	tweet_no_punctuation = [remove_punctuations(tweet) for tweet in lowercase_tweets]

	# print example
	print("Example of tweet with no punctuation: ", tweet_no_punctuation[2])

	# remove links
	tweet_no_link = [remove_links(tweet) for tweet in tweet_no_punctuation]

	# remove users
	tweet_no_users = [remove_users(tweet) for tweet in tweet_no_link]

	print("Example of tweet with no users or links: ", tweet_no_users[2])

	# combined
	#tweets_no_stopwords = [word for word in tweet_no_users.split(' ') if word not in stopwords_list]
	tweets_no_stopwords = [[word for word in tweet.split(' ') if word not in stopword_set] for tweet in tweet_no_users]

	print("Example tweet with no stopwords: ", tweets_no_stopwords[2])

	# re-combine the words
	cleaned_tweets = [''.join(word_arr) for word_arr in tweets_no_stopwords] 

	# print example of re-combined words
	print("Example tweet that's been re-combined: ", cleaned_tweets[2])

	# write cleaned csv
	with open("../data/cleaned_tweets.csv", 'w', newline = '') as csv_file:
		wr = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
		wr.writerow(cleaned_tweets)

if __name__ == "__main__":
	main()

