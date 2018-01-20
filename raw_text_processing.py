###########################################################################
# Pre-processing raw text

# Date: November 2017

###########################################################################
import os
import re
import nltk # Natural Language toolkit
from nltk.tokenize import sent_tokenize, word_tokenize # form tokens from words/sentences
import string
import codecs 

########################################################################
## READING AND TOKENIZATION OF RAW TEXT (PRE-PROCESSING)

basic_pronouns = "I Me You She He Him It We Us They Them Myself Yourself Himself Herself Itself Themselves My your Her Its Our Their His"

def readFile(filename):
	file_remove_extra = []
	with open(filename, "r") as given_file:
		string_words = given_file.read()
		string_words = string_words.replace("\n", " ")
		string_words = string_words.replace(";" , " ")
		string_words = string_words.replace("--", " ")
		string_words = re.sub(r'[\x90-\xff]', '', string_words, flags=re.IGNORECASE) # remove unicode
		string_words = re.sub(r'[\x80-\xff]', '', string_words, flags=re.IGNORECASE) # remove unicode
		file_remove_extra = string_words.split(' ')
		file_remove_extra = filter(None, file_remove_extra) # remove empty strings from list
	return file_remove_extra
'''
def readFile(filename):
	file_remove_extra = []
	with codecs.open(filename, "r", 'utf-8', errors='ignore') as given_file:
		string_words = given_file.read()
		# remove puntucation from text

		string_words = string_words.replace("\n", " ")
		string_words = string_words.replace(";" , " ")
		string_words = string_words.replace("--", " ")
		string_words = string_words.encode("ascii", "ignore") # convert back to ascii from unicode
		# keep quotes, but move into their own token
		#string_words = string_words.replace("\"", "\" ")

		# store all words in order in a list
		file_remove_extra = string_words.split(' ')
		file_remove_extra = filter(None, file_remove_extra) # remove empty strings from list
		#file_remove_extra = map(str.lower, file_remove_extra) # convert all words to upper case for consitency
	#print(file_remove_extra)
	return file_remove_extra
'''
def tokenizeSentence(string_sentence):
	'''EXAMPLE
	{60: 'After rather a long silence, the commander resumed the conversation.'}
	'''
	tokens_sentence_dict = {} # returns dict with {token location in text #: sentence}
	tokens_sent = string_sentence.split('.')
	for i in range(len(tokens_sent)):
		if tokens_sent[i] != '':
			tokens_sentence_dict[i] = tokens_sent[i].strip() #adds to dictionary and strips away excess whitespace
	print(tokens_sentence_dict)
	return tokens_sentence_dict

def partsOfSpeech(token_dict):
	'''EXAMPLE
	60: ('After rather a long silence, the commander resumed the conversation.', 
	[('After', 'IN'), ('rather', 'RB'), ('a', 'DT'), ('long', 'JJ'), ('silence', 'NN'),
	 (',', ','), ('the', 'DT'), ('commander', 'NN'), ('resumed', 'VBD'), ('the', 'DT'), 
	 ('conversation', 'NN'), ('.', '.')])}
	'''
	for key, value in token_dict.iteritems():
		no_punc = value.translate(None, string.punctuation) # remove puncuation from part of speech tagging
		token_dict[key] = (value, nltk.pos_tag(word_tokenize(no_punc))) # adds part of speech tag for each word in the sentence
	return token_dict

'''
def syntaxTree(token_dict):
	syntaxTreeStr = ''

	print("\n")
	for index in range(len(token_dict)):
		print(token_dict[index][0])
		print(token_dict[index][1])
		print(len(token_dict[index][0]))
		print(len(token_dict[index][1]))
	print("\n")
	syntax_list = '[' #https://yohasebe.com/rsyntaxtree/
	#[S[NNP_FIRST Alice][VP[VBS is][NP[DT a][NN student][IN of][NNS physics]]]][S[NNP_FIRST Alice][VP[VBS is][NP[DT a][NN student][IN of][NNS physics]]]]
	for index in range(len(token_dict)):
		for pos in token_dict[index][1]:
			#print(pos)
			syntax_list += str([pos[1], pos[0]])
	syntax_list += ']'
	#syntax_list = syntax_list.translate(None, ',') #remove quotes and commas for formatting
	#syntax_list = syntax_list.translate(None, '\'') #remove quotes and commas for formatting
	print("\n")
	print(syntax_list)
	return syntaxTreeStr
'''

def mostCommonPronouns(raw_text):
	# returns a dictionary of the most common pronouns in the text with their occureance #
	#{'it': 1291, 'him': 213, 'yourself': 16, 'his': 519, 'our': 292, 'your': 122}

	pronoun_common = {}
	from collections import Counter

	raw_words = re.findall(r'\w+', raw_text)

	total_words = [word.lower() for word in raw_words]
	word_counts = Counter(total_words)
		
	tag_pronoun = ["PRP", "PRP$"]

	for word in word_counts:
		captilize_options = [word.capitalize(), word.lower()] # dealing with ME seen as NN instead of PRP
		for options in captilize_options:
			if nltk.pos_tag(nltk.word_tokenize(options))[0][1] in tag_pronoun: # if word is a pronoun, then store it
				if options.lower() in basic_pronouns.lower().split():
					pronoun_common[word.lower()] = word_counts[word]

	# testing that it found the right pronouns (not in basic_pronouns)
	#if len(pronoun_common.keys()) != len(basic_pronouns.lower().split()):
	#	for found in pronoun_common.keys():
	#		if found not in basic_pronouns.lower().split():
	#			print("\n\tWARNING: INCORRECT PRONOUNS FOUND ==> {0}\n".format(found))

	return pronoun_common

########################################################################
## Parse Arguments, running main

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
	tokens_as_string = tokens_as_string.translate(None, "\r")
	
	# return the most common pronouns in the text (TODO: Automate)
	most_common_pronouns = mostCommonPronouns(tokens_as_string)
	print(most_common_pronouns)
	print("\n")

	token_sentence_dict = tokenizeSentence(tokens_as_string)
	#print(token_sentence_dict) # TODO: switch to namedTuples

	#dict_parts_speech = partsOfSpeech(token_sentence_dict)
	#print(dict_parts_speech)
