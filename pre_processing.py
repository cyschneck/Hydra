###########################################################################
# Pre-processing raw ext

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
	'''EXAMPLE
	{60: 'After rather a long silence, the commander resumed the conversation.'}
	'''
	tokens_sentence_dict = {} # returns dict with {token location in text #: sentence}
	for i in range(len(sent_tokenize(string_sentence))):
		tokens_sentence_dict[i] = sent_tokenize(string_sentence)[i]
	#print(tokens_sentence_dict)
	return tokens_sentence_dict

def partsOfSpeech(token_dict):
	'''EXAMPLE
	60: ('After rather a long silence, the commander resumed the conversation.', 
	[('After', 'IN'), ('rather', 'RB'), ('a', 'DT'), ('long', 'JJ'), ('silence', 'NN'),
	 (',', ','), ('the', 'DT'), ('commander', 'NN'), ('resumed', 'VBD'), ('the', 'DT'), 
	 ('conversation', 'NN'), ('.', '.')])}
	'''
	for key, value in token_dict.iteritems():
		token_dict[key] = (value, nltk.pos_tag(word_tokenize(value))) # adds part of speech tag for each word in the sentence
	#print(token_dict)
	return token_dict

def chunkNouns(token_dict):
	chunk_dict = {}

	#chunkGram = r"""Noun: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""  # any form , returns 0 or more, requires noun (singular)
	chunkGram = r"""Noun: {(<NN.?>|<PRP.?>)}"""  # any form , returns 0 or more, requires noun (singular)
	chunkParser = nltk.RegexpParser(chunkGram)
	for key, value in token_dict.iteritems():
		chunked = chunkParser.parse(value[1]) # parses part of speech tags
		#chunked.draw() #prints as a tree
		chunk_dict[key] = chunked # stores at the same index value in new dictionary

	return chunk_dict

def namedEntity(token_dict):
	'''named entity based on nltk'''
	named_ent_dict = {}

	for key, value in token_dict.iteritems():
		namedEnt = nltk.ne_chunk(value[1], binary=True) # classifies all tags as named entites (avoids different types, name, time, etc...)
		#namedEnt.draw()
		named_ent_dict[key] = namedEnt
	print(named_ent_dict[1].draw())

	return named_ent_dict

#def hierachy_tree (named_enity (parent->) pronoun/title (->child)) IS A PRINT for easy viewing
'''
Grandfather  +  Grandmother
             |
             |
--------------------    
   |         |          
Daughter    Son + Daughter in-law
                |
                |
      -----------------
         |         |
      Grandson Granddaughter
'''
#def neural_network trained on position of pronoun from named enitiy
# all pronouns are linked to all proper nouns and widdled down based on probabilitiy based on a manually tagged set of training data

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

	token_sentence_dict = tokenizeSentence(tokens_as_string)
	print(token_sentence_dict)
	dict_parts_speech = partsOfSpeech(token_sentence_dict)

	group_nouns = chunkNouns(dict_parts_speech)

	nltk_named_entity_recognition = namedEntity(dict_parts_speech)
	print(nltk_named_entity_recognition)
