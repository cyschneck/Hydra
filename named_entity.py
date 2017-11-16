###########################################################################
# Named Entity Recognition

# Date: November 2017

# Determine the subject within raw text
# Group pronouns and titles together based on subject

###########################################################################
import os
import nltk # Natural Language toolkit
from nltk.tokenize import sent_tokenize, word_tokenize # form tokens from words/sentences

########################################################################
## READING AND TOKENIZATION OF RAW TEXT (PRE-PROCESSING)

def readFile(filename):
	file_remove_extra = []
	with open(filename, "r") as given_file:
		string_words = given_file.read()
		# remove puntucation from text
		string_words = string_words.replace("\n", " ")
		string_words = string_words.replace(";" , " ")
		string_words = string_words.replace("--", " ")
		# keep quotes, but move into their own token
		#string_words = string_words.replace("\"", "\" ")

		# store all words in order in a list
		file_remove_extra = string_words.split(' ')
		file_remove_extra = filter(None, file_remove_extra) # remove empty strings from list
		#file_remove_extra = map(str.lower, file_remove_extra) # convert all words to upper case for consitency
	#print(file_remove_extra)
	return file_remove_extra

def tokenizeSentence(string_sentence):
	tokens_sentence_dict = {}
	for i in range(len(sent_tokenize(string_sentence))):
		tokens_sentence_dict[i] = sent_tokenize(string_sentence)[i]
	print(tokens_sentence_dict)
	return tokens_sentence_dict

def tokenizeWord(string_sentence):
	tokens_word_dict = {}
	for i in range(len(word_tokenize(string_sentence))):
		tokens_word_dict[i] = word_tokenize(string_sentence)[i]
	#print(tokens_word_dict)
	return tokens_word_dict


########################################################################
## Parse Arguments
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="flag format given as: -F <filename>")
	parser.add_argument('-F', '-filename', help="filename from Raw_Text directory")
	args = parser.parse_args()

	filename = args.F

	if filename is None:
		print("\n\tWARNING: File not given to tokenize, exiting...\n")
		exit()

	tokens_in_order = readFile(filename)
	tokens_as_string = " ".join(tokens_in_order)

	token_sentence_dict = tokenizeSentence(tokens_as_string)
	#token_word_dict = tokenizeWord(tokens_as_string)
