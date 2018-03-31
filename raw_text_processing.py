# -*- coding: utf-8 -*-
###########################################################################
# Pre-processing raw text

# Date: November 2017
###########################################################################
import os
import re
import nltk # Natural Language toolkit
from nltk.tokenize import sent_tokenize, word_tokenize # form tokens from words/sentences
import matplotlib
matplotlib.use('Agg')
import string
import csv
from datetime import datetime
from collections import namedtuple, Counter
import itertools
from itertools import imap, permutations # set up namedtuple
from collections import defaultdict # create dictionary with empty list for values
import matplotlib.pyplot as plt # graphs
import networkx as nx
import numpy as np
########################################################################
## READING AND TOKENIZATION OF RAW TEXT (PRE-PROCESSING)

#TODO: move to a seperate file (up to readFile)
basic_pronouns = "I Me You She He Him It We Us They Them Myself Yourself Himself Herself Itself Themselves My your Her Its Our Their His"
possessive_pronouns = "mine yours his hers ours theirs my"
reflexive_pronouns = "myself yourself himself herself itself oneself ourselves yourselves themselves you've"
relative_pronouns = "that whic who whose whom where when"

neutral_pronouns = ['I', 'Me', 'You', 'It', 'We', 'Us', 'They', 'Them', 'Myself', 'Mine',
					'Yourself', 'Itself', 'Themselves', 'My', 'Your', 'Its', 'Our', 'Their',
					"One", "Ourselves", 'Yours']

female_pronouns = ['Her', 'Hers', 'Herself', "She", 'Herself']
male_pronouns =   ['He', 'Him', 'His', 'Himself']

male_honorific_titles = ['M', 'Mr', 'Sir', 'Lord', 'Master', 'Gentleman', 
						 'Sire', "Esq", "Father", "Brother", "Rev", "Reverend",
						 "Fr", "Pr", "Paster", "Br", "His", "Rabbi", "Imam",
						 "Sri", "Thiru", "Raj", "Son", "Monsieur", "M", "Baron",
						 "Prince", "King", "Emperor", "Grand Prince", "Grand Duke",
						 "Duke", "Sovereign Prince", "Count", "Viscount", "Crown Prince",
						 'Gentlemen', 'Uncle', 'Widower', 'Don', "Mistah", "Commodore",
						 "Grandfather", "Mister", "Brother-in-Law", "Mester"]

female_honorific_titles = ['Mrs', 'Ms', 'Miss', 'Lady', 'Mistress',
						   'Madam', "Ma'am", "Dame", "Mother", "Sister",
						   "Sr", "Her", "Kum", "Smt", "Ayah", "Daughter",
						   "Madame", "Mme", 'Madame', "Mademoiselle", "Mlle", "Baroness",
						   "Maid", "Empress", "Queen", "Archduchess", "Grand Princess",
						   "Princess", "Duchess", "Sovereign Princess", "Countess",
							"Gentlewoman", 'Aunt', 'Widow', 'Doha', 'Comtesse', 'Baronne',
							"Grandmother", "Sister-in-Law", "Missus"]

ignore_neutral_titles = ['Dr', 'Doctor', 'Captain', 'Capt',
						 'Professor', 'Prof', 'Hon', 'Honor', "Excellency",
						 "Honourable", "Honorable",  "Chancellor", "Vice-Chancellor", 
						 "President", "Vice-President", "Senator", "Prime", "Minster",
						 "Principal", "Warden", "Dean", "Regent", "Rector",
						 "Director", "Mayor", "Judge", "Cousin", 'Archbishop',
						 'General', 'Secretary', 'St', 'Saint', 'San', 'Assistant', "Director",
						 "The Right Honorable", "The Right Honourable", "Highness", "Cuz"]

all_honorific_titles = male_honorific_titles + female_honorific_titles + ignore_neutral_titles


male_equ_titles = [['M', 'Mr', 'Mister', 'Mistah', 'Mester']]
female_equ_titles = [['Ms', 'Miss', 'Missus', 'Mademoiselle', 'Mlle'],
					['Madam', "Ma'am", "Madame", "Mme"]]
neutral_equ_titles = [['Dr', 'Doctor'], ['Capt', 'Captain'],
					  ['Professor', 'Prof'], ['St', 'Saint'], 
					  ["Cousin", "Cuz"]]

all_equal_titles = male_equ_titles + female_equ_titles + neutral_equ_titles
all_equal_titles = [item for sublist in all_equal_titles for item in sublist] # flat list of all titles for checking
potential_names_with_equal_titles = []


connecting_words = ["of", "the", "De", "de", "La", "la", 'al', 'y', 'Le', 'Las']

# WORDS TO IGNORE (parser has mislabeled)
words_to_ignore = ["Dear", "Chapter", "Volume", "Man", "God", "O", "Anon", "Ought", 
				   "Thou", "Thither", "Yo", "Till", "Ay", "Dearest", "Dearer", "Though", 
				   "Hitherto", "Ahoy", "Alas", "Yo", "Chapter", "Again", "'D", "One", "'T", "Poor",
				   "If", "thy", "Thy", "Thee", "Suppose", "There", "'There", "No-One", "Happily",
				   "Good-Night", "Good-Morning", 'To-Day', 'To-Mmorrow', "Compare", "Tis", "Good-Will",
				   'To-day', 'To-morrow', 'To-Night', 'Thine', 'Or', "D'You", "O'Er", "Aye", "Men"
				   "Ill", "Behold", "Beheld", "Nay", "Shall", "So-And-So", "Making-Up", "Ajar",
				   "Show", "Interpreting", "Then", "No", "Alright", "Tell", "Thereupon", "Yes",
				   "Abandon", "'But", "But", "'Twas", "Knelt", "Thou", "True", "False",
				   "Overhead", "Ware", "Fortnight", "Good-looking", "Something", "Grants", "Rescue",
				   "Head", "'Poor", "Tha'", "Tha'Rt", "Eh", "Whither", "Ah"] # ignores noun instances of these word by themselves

words_to_ignore += ["".join(a) for a in permutations(['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X'], 2)]
words_to_ignore += ["".join(a) for a in ['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X', 'XV']]

numbers_as_words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
					6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
					11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
					15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
					19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
					50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty',
					90: 'Ninety', 0: 'Zero'}

total_numbers = numbers_as_words.values()

words_to_ignore += ["Chapter {0}".format("".join(a)) for a in []]

words_to_ignore += ["Chapter {0}".format("".join(a)) for a in permutations(['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X'], 2)]
words_to_ignore += ["Chapter {0}".format("".join(a)) for a in ['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X']]

words_to_ignore += ["Chapter {0}".format("".join(a)) for a in permutations(['1','2','3','4','5','6','7','8','9','10'], 2)]
words_to_ignore += ["Chapter {0}".format("".join(a)) for a in ['1','2','3','4','5','6','7','8','9','10']]

words_to_ignore += ["CHAPTER {0}".format("".join(a)) for a in permutations(['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X'], 2)]
words_to_ignore += ["CHAPTER {0}".format("".join(a)) for a in ['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X']]

words_to_ignore += ["Volume {0}".format("".join(a)) for a in permutations(['1','2','3','4','5','6','7','8','9','10'], 2)]
words_to_ignore += ["Volume {0}".format("".join(a)) for a in ['1','2','3','4','5','6','7','8','9','10']]

words_to_ignore += ["Volume {0}".format("".join(a)) for a in permutations(['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X'], 2)]
words_to_ignore += ["Volume {0}".format("".join(a)) for a in ['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X']]

words_to_ignore += ["VOLUME {0}".format("".join(a)) for a in permutations(['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X'], 2)]
words_to_ignore += ["VOLUME {0}".format("".join(a)) for a in ['I', 'II','III', 'IV', 'VI', 'XX', 'V', 'X']]

words_to_ignore += ["VOLUME {0}".format("".join(a)) for a in permutations(['1','2','3','4','5','6','7','8','9','10'], 2)]
words_to_ignore += ["VOLUME {0}".format("".join(a)) for a in ['1','2','3','4','5','6','7','8','9','10']]


def readFile(filename):
	file_remove_extra = []
	with open(filename, "r") as given_file:
		string_words = given_file.read()
		string_words = string_words.replace("\r\n\r\n", ".") # create sentences for chapter titles
		string_words = string_words.replace("\n", " ")
		string_words = string_words.replace("--", ", ")
		string_words = string_words.replace("; ", ", ")
		string_words = string_words.replace("*", "")
		string_words = string_words.replace("_", "")
		string_words = string_words.replace("!”", "!”.") # “Ah-h-h!”  “How true!”  “Amazing, amazing!” into sub-sentences (twain)
		string_words = string_words.replace("'I", "' I") # fix puncutation where I 
		string_words = string_words.replace("'It", "' It")
		string_words = string_words.replace("'we", "' we")
		string_words = string_words.replace("'We", "' We")
		string_words = string_words.replace("Mr.", "Mr") # period created breaks when spliting
		string_words = string_words.replace("Ms.", "Ms")
		string_words = string_words.replace("Mrs.", "Mrs")
		string_words = string_words.replace("Dr.", "Dr")
		string_words = string_words.replace("St.", "St")
		# replace utf-8 elements
		string_words = string_words.replace("’", "\'") # replace signal quotes
		string_words = string_words.replace("“", "~\"") # isolate dialouge double quotes
		string_words = string_words.replace("” ", "\"~")

		string_words = re.sub(r'[\x90-\xff]', ' ', string_words, flags=re.IGNORECASE) # remove unicode (dash)
		string_words = re.sub(r'[\x80-\xff]', '', string_words, flags=re.IGNORECASE) # remove unicode
		file_remove_extra = string_words.split(' ')
		file_remove_extra = filter(None, file_remove_extra) # remove empty strings from list
	return file_remove_extra

def isDialogue(sentence):
	# return true/false if the value is a quote
	return '"' in sentence

def tokenizeSentence(string_sentence):
	'''EXAMPLE
	{60: 'After rather a long silence, the commander resumed the conversation.'}
	'''
	tokens_sentence_dict = {} # returns dict with {token location in text #: sentence}
	tokens_sent = string_sentence.split('.')

	index = 0
	for t in range(len(tokens_sent)):
		sent = tokens_sent[t].strip() # remove excess whitespace
		for dia in sent.split('~'):
			if dia != '': # store dialouge with its double quotes for identification
				tokens_sentence_dict[index] = dia # {4: '"Oh, why can\'t you remain like this for ever!"'}
				index += 1
				t += 1
	#print(tokens_sentence_dict)
	return tokens_sentence_dict

def partsOfSpeech(token_dict):
	'''EXAMPLE
	60: ('After rather a long silence, the commander resumed the conversation.', 
	[('After', 'IN'), ('rather', 'RB'), ('a', 'DT'), ('long', 'JJ'), ('silence', 'NN'),
	 (',', ','), ('the', 'DT'), ('commander', 'NN'), ('resumed', 'VBD'), ('the', 'DT'), 
	 ('conversation', 'NN'), ('.', '.')])}
	'''
	from subprocess import check_output
	import progressbar as pb
	widgets = ['Running POS tagger: ', pb.Percentage(), ' ', 
				pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
	timer = pb.ProgressBar(widgets=widgets, maxval=len(token_dict)).start()

	for i in range(len(token_dict)):
		timer.update(i)
		no_punc = token_dict[i].translate(None, string.punctuation) # remove puncuation from part of speech tagging
		pos_tagged = check_output(["./3_run_text.sh", token_dict[i]])
		if "docker not running, required to run syntaxnet" not in pos_tagged:
			pos_tagged = process_POS_conll(pos_tagged) # process conll output from shell
			token_dict[i] = (token_dict[i], pos_tagged) # adds part of speech tag for each word in the sentence
		else:
			print("\n\tWARNING: docker not running, cannot run syntaxnet for POS, exiting")
			exit()
	timer.finish()
	return token_dict

def process_POS_conll(conll_output):
	'''
	['1', 'At', '_', 'ADP', 'IN', '_', '13', 'prep', '_', '_']
	['2', 'the', '_', 'DET', 'DT', '_', '3', 'det', '_', '_']
	['3', 'period', '_', 'NOUN', 'NN', '_', '1', 'pobj', '_', '_']
	['4', 'when', '_', 'ADV', 'WRB', '_', '7', 'advmod', '_', '_']
	['5', 'these', '_', 'DET', 'DT', '_', '6', 'det', '_', '_']
	['6', 'events', '_', 'NOUN', 'NNS', '_', '7', 'nsubj', '_', '_']
	['7', 'took', '_', 'VERB', 'VBD', '_', '3', 'rcmod', '_', '_']
	['8', 'place', '_', 'NOUN', 'NN', '_', '7', 'dobj', '_', '_']
	'''
	pos_processed = conll_output
	#print(pos_processed)
	start_data = 0
	pos_processed = re.sub("\t", ",", pos_processed.strip())
	pos_processed = re.sub(",", " ", pos_processed.strip())
	pos_processed = pos_processed.splitlines()
	for i in range(len(pos_processed)):
		pos_processed[i] = pos_processed[i].split(" ")
		#print(pos_processed[i])
	return pos_processed

########################################################################
## GROUP PROPER NOUNS ENTITIES
def findProperNamedEntity(pos_dict):
	# returns {sentence index: [list of all proper nouns grouped]
	# {0: ["Scarlett O'Hara", 'Tarleton'], 1: ['Coast']}
	pos_type_lst = []
	# TODO: EXPAND PROPER NOUNS FOR COMMON WORDS AROUND WORD
	previous_nnp_index = 0
	for row, pos_named in pos_dict.iteritems():
		if "NNP" in pos_named.XPOSTAG: #"NN" in pos_named.XPOSTAG or "POS" in pos_named.XPOSTAG or "IN" in pos_named.XPOSTAG or "DT" in pos_named.XPOSTAG:
			pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))
			previous_nnp_index = int(pos_named.ID)
		if pos_named.FORM in connecting_words:
			pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))
			previous_nnp_index = int(pos_named.ID)
		#if "the" in pos_named.FORM or "The" in pos_named.FORM:
		#	if previous_nnp_index < int(pos_named.ID): # only store of if it is part of an existing sentence
		#		pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))
		#if "of" in pos_named.FORM:
		#	if previous_nnp_index < int(pos_named.ID): # only store of if it is part of an existing sentence
		#		pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))
		
	total_sentence_indices = list(set([i[0] for i in pos_type_lst]))

	sub_sentences = []
	for index in total_sentence_indices:
		# create sub sentences for each sentence [[0], [1])
		sub_sentences.append([x for x in pos_type_lst if x[0] == index])
	#print("\nsub_sentence={0}\n".format(sub_sentences))
	
	from operator import itemgetter # find sequences of consecutive values
	import itertools

	grouped_nouns = {}
	names_lst = []
	sentence_index = []
	for sentence in sub_sentences:
		noun_index = [s_index[1] for s_index in sentence] # noun location in a sentence (index)
		#print(sentence, noun_index)
		consec_lst = []
		for k, g in itertools.groupby(enumerate(noun_index), lambda x: x[1]-x[0]):
			consec_order = list(map(itemgetter(1), g))
			if len(consec_order) > 0: # if there is more than one noun in an order for a sentence
				consec_lst.append(consec_order)
		#consec_lst = [item for items in consec_lst for item in items]
		for c_l in consec_lst:
			g_name = [x for x in sentence if x[1] in c_l]
			nnp_in_sentence = False
			for i, v in enumerate(g_name):
				nnp_in_sentence = "NNP" in v
				if nnp_in_sentence: # if the nnp exist in the sub-list, exit and save
					break
			if nnp_in_sentence:
				#print(c_l)
				#print([x[2] for x in sentence if x[1] in c_l])
				#print(" ".join([x[2] for x in sentence if x[1] in c_l]))
				start_with_connecting_ignore = [x[2] for x in sentence if x[1] in c_l][0] in connecting_words
				end_with_connecting_ignore = [x[2] for x in sentence if x[1] in c_l][-1] in connecting_words
				if start_with_connecting_ignore or end_with_connecting_ignore:
				# if the gne starts with a connecting word, ignore the connecting name: 'of Divine Providence' -> 'Divine Providence'
					new_start_index = 0
					for first_words in [x[2] for x in sentence if x[1] in c_l]:
						if first_words not in connecting_words:
							break # if it doesn't start with a connecting word, ignore
						else:
							new_start_index += 1
					#print([x[2] for x in sentence if x[1] in c_l][new_start_index:])
					#print(" ".join([x[2] for x in sentence if x[1] in c_l][new_start_index:]))
					new_end_index = len([x[2] for x in sentence if x[1] in c_l]) # last element after it is been updated
					for last_words in reversed([x[2] for x in sentence if x[1] in c_l]):
					# if the gne ends with a connecting word, ignore the connecting name: 'Tom of the' -> 'Tom'
						if last_words not in connecting_words:
							break
						else:
							new_end_index -= 1
					#if new_end_index <  len([x[2] for x in sentence if x[1] in c_l]):
					#	print("original: {0}".format(" ".join([x[2] for x in sentence if x[1] in c_l])))
					#	print("update: {0}\n".format(" ".join([x[2] for x in sentence if x[1] in c_l][new_start_index:new_end_index])))
					#	print(new_start_index, new_end_index)
					if (new_end_index != 0) and (new_start_index != len([x[2] for x in sentence if x[1] in c_l])): # if the entire gne wasn't connecting words
						names_lst.append(" ".join([x[2] for x in sentence if x[1] in c_l][new_start_index:new_end_index]))
						sentence_index.append(list(set([x[0] for x in sentence if x[1] in c_l][new_start_index:new_end_index]))[0])
				else:
					names_lst.append(" ".join([x[2] for x in sentence if x[1] in c_l]))
					sentence_index.append(list(set([x[0] for x in sentence if x[1] in c_l]))[0])

	dic_tmp = zip(sentence_index, names_lst)
	grouped_nouns = defaultdict(list)
	for s, n in dic_tmp:
		grouped_nouns[s].append(n)
	return dict(grouped_nouns)

def commonSurrouding(grouped_nouns_dict):
	# find the most common preceding words to append
	pass

def groupSimilarEntities(grouped_nouns_dict):
	# filter out enities that only appear once and re-organize
	'''
	[['America'], ['Aronnax', 'Pierre', 'Pierre Aronnax'],
	['Captain Farragut', 'Captain', 'Farragut'], ['Conseil'], 
	['English'], ['Europe'], ['French'], ['Gentlemen'], ['God'], 
	['Land', 'Mr Ned Land', 'Ned', 'Ned Land'], ['Latin'],
	['Lincoln', 'Abraham', 'Abraham Lincoln'], ['Museum'], 
	['Natural'], ['OEdiphus'], ['Pacific'], ['Paris'], ['Professor'],
	['Sir'], ['Sphinx'], ['United States', 'States', 'United'],
	['sir']]
	'''
	#print("grouped_nouns_dict = {0}".format(grouped_nouns_dict))
	counter_dict = dict(Counter([val for sublist in grouped_nouns_dict.values() for val in sublist]))

	#print("counter={0}".format(counter_dict))

	names_all = list(set([val for sublist in grouped_nouns_dict.values() for val in sublist])) # is a list of all unquie names in the list
	compare_names_same_format = [val.upper() for val in names_all]
	# loop through to group similar elements
	gne_list_of_lists = grouped_nouns_dict.values()
	gne_list_of_lists = list(set([item for sublist in gne_list_of_lists for item in sublist])) # creates a list of unquie names

	import difflib 
	from difflib import SequenceMatcher
	gne_name_group = []
	# find most similar ['Professor', 'Professor Aronnax'], ['Aronnax', 'Mr Aronnax', 'Pierre Aronnax']
	for gne in gne_list_of_lists:
		for g in gne.split():
			compared = difflib.get_close_matches(g, gne_list_of_lists)
			if compared != []:
				gne_name_group.append(compared)

	subgrouping = []
	#print("\ngne_list_of_lists: {0}".format(gne_list_of_lists))
	if len(gne_list_of_lists) > 1: # if there is only one name in all the text (debugging short texts)
		for gne in gne_list_of_lists:
			sublist = []
			if len(gne.split()) == 1 and len(gne.split()[0]) > 1: # includes only single instance values that are not a single letter
				sublist.append(gne.split()) # include values that only appear once in a setence
			for i in gne.split():
				for gne_2 in gne_list_of_lists:
					if i in gne_2 and i != gne_2 and (i != [] or gne_2 != []):
						chapter_titles = ["CHAPTER", "Chapter", "Volume", "VOLUME"]
						# only save words that don't include the chapter titles
						found_in_i = any(val in chapter_titles for val in i.split())
						found_in_gne2 = any(val in chapter_titles for val in gne_2.split())
						if found_in_i or found_in_gne2:
							# 'CHAPTER XXII Mr Rochester' -> 'Mr Rochester'
							for title in chapter_titles:
								if found_in_i:
									#print(" ".join(i.split()[2:]))
									i = " ".join(i.split()[2:])
									break
								if found_in_gne2:
									#print(" ".join(gne_2.split()[2:]))
									gne_2 = " ".join(gne_2.split()[2:])
									break
							if i != '' and gne_2 != '':
								#print("FINAL APPEND={0}\n".format((i, gne_2)))
								sublist.append([i, gne_2])
					else:
						if gne_2 != i:
							if gne_2 not in i:
								if [gne_2] not in sublist: # only keep one iteration of the name
									if len(gne_2) > 1: # exclude single letter
										sublist.append([gne_2])
			subgrouping.append(sublist)
	else:
		subgrouping.append(gne_list_of_lists)

	final_grouping = []
	if len(subgrouping) > 1:
		subgrouping = [x for x in subgrouping if x != []]
		for subgroup in subgrouping:
			final_grouping.append(list(set([item for sublist in subgroup for item in sublist])))
	else:
		final_grouping = subgrouping # keep the single element

	iterate_list_num = list(range(len(final_grouping)))
	for i in range(len(final_grouping)):
		for num in iterate_list_num:
			if num != i:
				extend_val = list(set(final_grouping[i]).intersection(final_grouping[num]))
				if extend_val:
					final_grouping[i].extend(final_grouping[num])
					final_grouping[i] = sorted(list(set(final_grouping[i]))) # extend list to include similar elements

	#print("\nfinal_grouping: {0}".format(final_grouping))

	final_grouping = sorted(final_grouping) # organize and sort
	final_grouping = list(final_grouping for final_grouping,_ in itertools.groupby(final_grouping))
	#final_grouping = [x for x in final_grouping if x != []] # remove empty lists

	#print([item for item in final_grouping if item not in words_to_ignore])
	count = 0
	character_group_list = []
	# remove any word that is part of the 'words_to_ignore' list or is a title by itself
	for item in final_grouping:
		sublist = []
		for i in item:
			#print("'{0}' to ignore = {1}".format(i, i in words_to_ignore or i.title() in all_honorific_titles))
			if i in words_to_ignore or i.title() in all_honorific_titles:
				count += 1
				#print("in word to ignore = {0}".format(i))
			else:
				#print(i)
				sublist.append(i)
		#print("item = {0}".format(item))
		if item[0] in words_to_ignore:
			count += 1
			if item[0] in words_to_ignore:
				pass#print("in word to ignore = {0}".format(item[0]))
			else:
				#print(item[0])
				sublist.append(item[0])
		if sublist != []:
			character_group_list.append(sublist)
	#print("character_group_list: {0}".format(character_group_list))

	character_group = [] # only save unquie lists
	for i in character_group_list:
		if i not in character_group:
			character_group.append(i)

	#print("\nfinal group: \n{0}".format(final_grouping))
	#print("\ncharacter group: \n{0}".format(character_group))
	#print(len([item for item in final_grouping if item not in words_to_ignore]))
	#print(len(final_grouping))
	#print(len(character_group))
	#print("count = {0}".format(count))
	#print(words_to_ignore)
	return character_group

def lookupSubDictionary(shared_ent):
	# return a dictionary of proper nouns and surrounding values for one-shot look up
	'''
	{"Scarlett O'Hara": ["O'Hara", 'Scarlett'], 'Tarleton': ['Tarleton'], 
	"O'Hara": ["Scarlett O'Hara", 'Scarlett'], 'Scarlett': ["Scarlett O'Hara", "O'Hara"],
	 'Coast': ['Coast']}
	'''
	sub_dictionary_lookup = defaultdict(list)
	for group in shared_ent:
		iterate_list_num = list(range(len(group)))
		for i in range(len(group)):
			for j in iterate_list_num:
				if i != j:
					sub_dictionary_lookup[group[i]].append(group[j])
		if len(group) == 1:
			sub_dictionary_lookup[group[i]].append(group[i]) # for single instances, store {'Tarleton':'Tarleton'{ as its own reference

	return dict(sub_dictionary_lookup)

def mostCommonGNE(gne_grouped_dict):
	# find the longest most common version of a name in gnes to become the global
	#print("\nGlobal GNE")
	#for key, value in gne_grouped_dict.iteritems():
	#	print(key, value)
	#print(gne_grouped_dict.values())
	pass
	
########################################################################
## INDEX PRONOUNS
def findPronouns(pos_dict):
	# return the sentence index and pronouns for each sentence
	#{0: ['he', 'himself', 'his'], 1: ['He', 'his', 'he', 'his', 'he', 'his']}
	pos_type_lst = []
	for row, pos_named in pos_dict.iteritems():
		if "PRP" in pos_named.XPOSTAG:
			pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))

	total_sentence_indices = list(set([i[0] for i in pos_type_lst]))
	sub_sentences = []
	for index in total_sentence_indices:
		# create sub sentences for each sentence [[0], [1])
		sub_sentences.append([x for x in pos_type_lst if x[0] == index])

	grouped_pronouns = 	{}
	for pronoun_group in sub_sentences:
		pronoun_lst = []
		for pronoun in pronoun_group:
			pronoun_lst.append(pronoun[2])
		grouped_pronouns[pronoun[0]] = pronoun_lst

	return grouped_pronouns

def coreferenceLabels(filename, csv_file, character_entities_dict, global_ent, pos_dict):
	# save into csv for manual labelling
	# TODO: set up with average paragraph length as size_sentences
	size_sentences = 21000000000 # looking at x sentences at a time (could be automatically re-adjusted to fix max size of text)
	# set to large number so it runs through all sentences (could be set to look at x number of sentences)
	rows_of_csv_tuple = csv_file.values()
	all_sentences_in_csv = list(set([int(word.SENTENCE_INDEX) for word in csv_file.values()]))
	if size_sentences > max(all_sentences_in_csv)+1: # do not go out of range while creating sentences
		size_sentences = max(all_sentences_in_csv)+1
	print("Size of sentence for manual tagging = {0}".format(size_sentences))

	# save chucks of text (size sentences = how many sentences in each chunk of text)
	sub_sentences_to_tag = [all_sentences_in_csv[i:i + size_sentences] for i in xrange(0, len(all_sentences_in_csv), size_sentences)]
	#print("character entities keys: {0}\n".format(character_entities_dict.keys()))
	
	#print("\n")
	row_dict = {} # to print data into csv
	gne_index = 0 # display word of interst as [Name]_index
	pronoun_index = 0 # display word of interst as [Pronoun]_index
	for sentences_tag in sub_sentences_to_tag:
		#print(sentences_tag)
		# Test that csv is in order
		#from itertools import groupby
		#from operator import itemgetter
		#for k, g in groupby(enumerate(sentences_tag), lambda (i, x): i-x):
		#	#print(len(map(itemgetter(1), g)))
		#	print(map(itemgetter(1), g))
		#	print("\n")
		#	#print(len(sentences_tag), size_sentences)
		if len(sentences_tag) == size_sentences: # ignores sentences at the end that aren't the right length
			sentences_in_order = ''
			for i in range(sentences_tag[0], sentences_tag[-1]+1):
				new_sentence_to_add = list(set([row.SENTENCE for row in rows_of_csv_tuple if row.SENTENCE_INDEX == str(i)]))[0]
				if i+1 < sentences_tag[-1]+1:
					next_sentence_check = list(set([row.SENTENCE for row in rows_of_csv_tuple if row.SENTENCE_INDEX == str(i+1)]))[0]
					if len(next_sentence_check) == 1:
						#print("old: {0}".format(new_sentence_to_add))
						#print("NEXT IS NEARLY EMPTY, APPEND TO PREVIOUS SENTENCE: '{0}'".format(next_sentence_check))
						new_sentence_to_add += next_sentence_check # add the final dialouge tag into the previous sentence
						#print("new: {0}".format(new_sentence_to_add))
				# returns a sentence in range
				new_sentence_to_add = " {0} ".format(new_sentence_to_add) # add whitespace to the begining to find pronouns that start a sentence
				if "," in new_sentence_to_add:
					new_sentence_to_add = new_sentence_to_add.replace(",", " , ")
				if "\"" in new_sentence_to_add:
					new_sentence_to_add = new_sentence_to_add.replace("\"", " \" ")
				# add space to identify pronouns/nouns at the end of a sentence
				if "!" in new_sentence_to_add:
					new_sentence_to_add = new_sentence_to_add.replace("!", " ! ")
				if "?" in new_sentence_to_add:
					new_sentence_to_add = new_sentence_to_add.replace("?", " ? ")


				# tag pronouns first (from pos_dict)
				if i in pos_dict.keys():
					for pronoun in pos_dict[i]: # for all pronouns within the given sentence
						total_found = re.findall(r'\b{0}\b'.format(pronoun), new_sentence_to_add)
						if re.search(r' \b{0}\b '.format(pronoun), new_sentence_to_add): # match full word
							for tf in range(len(total_found)):
								new_sentence_to_add = new_sentence_to_add.replace(" {0} ".format(pronoun), " <{0}>_p{1} ".format(pronoun, pronoun_index), tf+1)
								pronoun_index += 1

				# tag proper nouns
				found_longest_match = ''
				gne_found_in_sentence = False # if found, print and update the sentence value
				
				lst_gne = []
				lst_gne = [gne_name for gne_name in character_entities_dict.keys() if gne_name in new_sentence_to_add]
				lst_gne = [x for x in lst_gne if x != []]

				index_range_list = [] # compare each index values
				all_index_values = [] # contains all index values of gnes
				to_remove = [] # if a value is encompassed, it should be removed

				if len(lst_gne) > 0:
					#print("\nlst_gne = {0}".format(lst_gne))
					for gne in lst_gne: # create the index values for each enitity
						#print("'{0}'  in         {1}".format(gne, new_sentence_to_add))
						search_item = re.search(r"\b{0}\b".format(gne), new_sentence_to_add)
						if not search_item: # if it return none
							break # skip item if not found
						else:
							start = search_item.start() # store the start index of the gne
							end = search_item.end() # store the end index of the gne
						index_range_word = [start, end]
						all_index_values.append(index_range_word)
						if len(index_range_list) == 0: # useful for debugging
							#print("FIRST GNE {0} has index {1}".format(gne, index_range_word))
							pass
						else:
							for range_index in index_range_list: # the index of the value is stored and new words are check to see if they are contained wtihing
								# example: united is within 'united states'
								if len(lst_gne) > 1:
									if (range_index[0] == index_range_word[0]) and (index_range_word[1] == range_index[1]):
										pass
									else:
										if (range_index[0] <= index_range_word[0]) and (index_range_word[1] <= range_index[1]):
												#print("{0} <= {1}-{2} <= {3}".format(range_index[0], index_range_word[0], index_range_word[1], range_index[1]))
												#print("{0} IS CONTAINED BY GNE = {1}\n".format(gne, new_sentence_to_add[range_index[0]:range_index[1]]))
												to_remove.append(index_range_word)
										if (index_range_word[0] <= range_index[0]) and(index_range_word[1] >= range_index[1]):
												#pass # reprsents the larger word that encompassing the smaller word
												#print("{0} <= {1}-{2} <= {3}".format(index_range_word[0], range_index[0],range_index[1], index_range_word[1]))
												#print("{0} IS EMCOMPASSED BY GNE = {1}\n".format(gne, new_sentence_to_add[index_range_word[0]:index_range_word[1]]))
												to_remove.append(range_index)
												#print("{0} <= {1} = {2}".format(index_range_word[0], range_index[0], index_range_word[0] <= range_index[0]))
												#print("{0} >= {1} = {2}".format(index_range_word[1], range_index[1], index_range_word[1] >= range_index[1]))
						index_range_list.append(index_range_word)
					#print("remove index values = {0}".format(to_remove))
					#print("largest gne index values ALL = {0}".format(all_index_values))
					all_index_values = sorted([x for x in all_index_values if x not in to_remove]) # index in order based on start value
					#print("shared (with removed encompassed) = {0}".format(all_index_values)) # remove all encompassed elements

					updated_index = []
					new_characters_from_update = 0 # new characters to keep track of character length when indexing
					repeats_to_find = []
					for counter, index_val in enumerate(all_index_values):
						if counter > 0:
							new_characters_from_update = len("<>_n ")*counter
						start_word = index_val[0] + new_characters_from_update
						end_word = index_val[1] + new_characters_from_update
						updated_index.append([start_word, end_word])
						find_repeats = new_sentence_to_add[start_word:end_word]
						repeats_to_find.append(find_repeats)
						replacement_string = "<{0}>_n ".format(new_sentence_to_add[start_word:end_word])
						new_sentence_to_add = "".join((new_sentence_to_add[:start_word], replacement_string, new_sentence_to_add[end_word:]))
						sub_counter = counter
					# add repeated gne values
					# if the same name appears more than once in a sentence 
					sub_counter = 0
					new_characters_from_update = 0 # new characters to keep track of character length when indexing
					for find_additional in repeats_to_find:
						repeat_item = re.finditer(r"\b{0}\b".format(find_additional), new_sentence_to_add)
						for m in repeat_item:
							index_to_check = [m.start(), m.end()]
							if [m.start()-1,m.end()-1] not in updated_index: # check that name hasn't been already assigned
								if new_sentence_to_add[m.start()-1] != '<' and new_sentence_to_add[m.end():m.end()+3] != '>_n':
									start_word = m.start() + new_characters_from_update
									end_word = m.end() + new_characters_from_update
									replacement_string = "<{0}>_n ".format(new_sentence_to_add[start_word:end_word])
									new_sentence_to_add = "".join((new_sentence_to_add[:start_word], replacement_string, new_sentence_to_add[end_word:]))
									sub_counter += 1
				new_sent = new_sentence_to_add.split()
				# label all proper nouns with an associated index value for noun
				for index, word_string in enumerate(new_sent):
					if '>_n' in word_string:
						if word_string != ">_n":
							new_sent[index] = '{0}{1}'.format(word_string, gne_index)
							new_sentence_to_add = " ".join(new_sent)
							gne_index += 1
				new_sentence_to_add = new_sentence_to_add.strip() # remove precending whitespace
				new_sentence_to_add = new_sentence_to_add.replace('" ', '"') # edit the speech puncutations
				new_sentence_to_add = new_sentence_to_add.replace(' "', '"') # edit the speech puncutations
				new_sentence_to_add = new_sentence_to_add.replace('\' ', '\'') # edit the speech puncutations
				new_sentence_to_add = new_sentence_to_add.replace(' , ', ', ') # edit the speech puncutations
				new_sentence_to_add = new_sentence_to_add.replace(' ! ', '! ') # edit the speech puncutations
				new_sentence_to_add = new_sentence_to_add.replace(' ? ', '? ') # edit the speech puncutations
				if new_sentence_to_add != '"': # if the value is just the end of a dialouge tag (already included, ignore)
					sentences_in_order += new_sentence_to_add + '. '
					#print(new_sentence_to_add + '. ')
			#print("\nFinal Sentence Format:\n\n{0}".format(sentences_in_order))
			saveTagforManualAccuracy(sentences_in_order)

def saveTagforManualAccuracy(sentences_in_order):
	## corefernece will call the csv creator for each 'paragraph' of text
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	output_filename = "manualTagging_{0}.csv".format(given_file.upper())

	fieldnames = ['FILENAME', 'TEXT',
				  'FOUND_PROPER_NOUN', 'MISSED_PROPER_NOUN',
				  'FOUND_PRONOUN', 'MISSED_PRONOUN']

	split_sentences_in_list = [e+'.' for e in sentences_in_order.split('.') if e] # split sentence based on periods
	split_sentences_in_list.remove(' .') # remove empty sentences
	sentence_size = 1 # size of the sentence/paragraph saved in manual tagging (one line for one sentence)
	sentence_range = [split_sentences_in_list[i:i+sentence_size] for i in xrange(0, len(split_sentences_in_list), sentence_size)]
	# range stores the sentences in list of list based on the size of tag

	#print("\n")
	#for sentence_tag in sentence_range:
	#	print(''.join(sentence_tag))
	#	print(''.join(sentence_tag).count("]_n"))
	#	print(''.join(sentence_tag).count("]_p"))
	#	print("\n")
	print("opening manual tag: {0}".format('manual_tagging/{0}'.format(output_filename)))
	with open('manual_tagging/{0}'.format(output_filename), 'w') as tag_data:
		writer = csv.DictWriter(tag_data, fieldnames=fieldnames)
		writer.writeheader() 
		# leave MISSED empty for manual tagging
		for sentence_tag in sentence_range:
			writer.writerow({'FILENAME': os.path.basename(os.path.splitext(filename)[0]), 
							 'TEXT': ''.join(sentence_tag),
							 'FOUND_PROPER_NOUN': ''.join(sentence_tag).count(">_n"),
							 'MISSED_PROPER_NOUN': None,
							 'FOUND_PRONOUN': ''.join(sentence_tag).count(">_p"),
							 'MISSED_PRONOUN': None 
							})
	print("{0} create MANUAL TAGGING for CSV".format(output_filename))

def breakTextPandN(manual_tag_dir, gender_gne_tree, loaded_gender_model):
	# resolve gender and pronoun noun interactions (resolution)
	pronoun_noun_dict = {}
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	
	# set up dict for pronouns and gender: {'His': 'Male', etc...}
	pronoun_gender = {f: 'Female' for f in female_pronouns}
	m_pronoun_gender = {m: 'Male' for m in male_pronouns}
	pronoun_gender.update(m_pronoun_gender)
	n_pronoun_gender = {n: 'Neutral' for n in neutral_pronouns}
	pronoun_gender.update(n_pronoun_gender)
	#check that all pronouns have been included in the dictionary
	test_full_list = female_pronouns + male_pronouns + neutral_pronouns
	for i in test_full_list:
		if i not in pronoun_gender:
			print("'{0}' NOT FOUND IN GENDER DICT".format(i))
	
	tagged_text = [] # store old rows
	with open(manual_tag_dir, 'r') as tag_data:
		reader = csv.reader(tag_data)
		next(reader) # skip header
		for row in reader:
			tagged_text.append(row[1]) # store the sentence in order

	sub_dict_titles = ['full_text', 'found_all_brackets', 'found_proper_name_value', 
					   'found_proper_name_index', 'found_pronoun_value', 'found_pronoun_index']
	line_by_line_dict = {}
	pronoun_noun_dict = {f: [] for f in sub_dict_titles}
	total_sentences_to_check_behind = 3 # TODO: update with pronouns average information
	#print("\n")
	for line_num, full_text in enumerate(tagged_text):
		#print(full_text)
		pronoun_noun_dict['full_text'].append([full_text])
		find_gne_in_sentence_pattern = r'(?<=\<)(.*?)(?=\>)'
		found_all_brackets = re.findall(find_gne_in_sentence_pattern, full_text) # everything together in the order that they appear
		pronoun_noun_dict['found_all_brackets'].append([found_all_brackets])
		#print('\n')
		#print(found_all_brackets)
		all_found_name_index = [[m.start(), m.end()] for m in re.finditer(find_gne_in_sentence_pattern, full_text)] # get index of all matches

		found_proper_name_value = [full_text[i[0]:i[1]] for i in all_found_name_index if full_text[i[1]+2] is 'n'] # store named ents
		found_proper_name_index = [i for i in all_found_name_index if full_text[i[1]+2] is 'n'] # store named index of names
		#for index_g in all_found_name_index:
		#	print(full_text[index_g[0]:index_g[1]])
		pronoun_noun_dict['found_proper_name_value'].extend([found_proper_name_value])
		pronoun_noun_dict['found_proper_name_index'].extend([found_proper_name_index])

		found_pronoun_value = [full_text[i[0]:i[1]] for i in all_found_name_index if full_text[i[1]+2] is 'p'] # store pronouns seperately
		found_pronoun_index = [i for i in all_found_name_index if full_text[i[1]+2] is 'p'] # store named index of pronouns
		pronoun_noun_dict['found_pronoun_value'].extend([found_pronoun_value])
		pronoun_noun_dict['found_pronoun_index'].extend([found_pronoun_index])

		# store in a sub-dictionary for each line
		line_by_line_dict[line_num] = {'full_text': full_text.strip(),
									   'found_all_brackets': found_all_brackets,
									   'found_proper_name_value': found_proper_name_value,
									   'found_proper_name_index': found_proper_name_index,
									   'found_pronoun_value': found_pronoun_value,
									   'found_pronoun_index': found_pronoun_index }

		#print("\nfound pronouns index: {0}".format(all_found_name_index))
		#for index_g in all_found_name_index:
		#	print(full_text[index_g[0]:index_g[1]])
		#print('\n')
		#print(found_proper_name_value)
		#for given_name in found_proper_name_value:
		#	print("{0} is {1}".format(given_name, gender_gne_tree[given_name]))
		#print('\n')
		#print(found_pronoun_value)
		#for pron in found_pronoun_value:
			#print("{0} is {1}".format(pron, pronoun_gender[pron.capitalize()]))
	
	# compress dictionray from a list of list to a single list
	for key, value in pronoun_noun_dict.iteritems():
		pronoun_noun_dict[key] = [item for sublist in value for item in sublist]
		if key == 'full_text':
			pronoun_noun_dict[key] = [''.join(pronoun_noun_dict[key])] # join the sentences into a single sentence
	return pronoun_noun_dict, line_by_line_dict

def determineGenderName(loaded_gender_model, gne_tree):
	# use trained model to determine the likely gender of a name
	gender_gne = {}
	
	all_gne_values =  gne_tree.keys()
	for key, values in gne_tree.iteritems():
		for k, v in values.iteritems():
			# add all sub_trees to list
			all_gne_values += [k]
			all_gne_values += v

	for full_name in all_gne_values:
		found_with_title = False
		female_prob = 0.0
		male_prob = 0.0

		full_name_in_parts = full_name.split()
		
		# if name is part of a gendered honorific, return: Mr Anything is a male
		if full_name_in_parts[0].title() in male_honorific_titles:
			#print("'{0}' contains '{1}' found: Male".format(full_name, full_name_in_parts[0]))
			gender_is = 'Male'
			male_prob += 1.0
			found_with_title = True
		if full_name_in_parts[0].title() in female_honorific_titles:
			#print("'{0}' contains '{1}' found: Female".format(full_name, full_name_in_parts[0]))
			gender_is = 'Female'
			female_prob += 1.0
			found_with_title = True
		
		# find the name for each part of the name, choose highest
		#print("'{0}' not found, calculating a probability...".format(full_name)) # not found in gendered honorifics
		# run test on each part of the name, return the largest so that last names don't overly effect
		dt = np.vectorize(DT_features) #vectorize dt_features function

		weight_last_name_less = 0.3
		
		if not found_with_title:
			for sub_name in full_name_in_parts:
				# determine if the name is likely to be the last name, if so, weight less than other parts of the name
				if sub_name in connecting_words:
					# do not calculate for titles "Queen of England" shouldn't find for England
					break
				else:
					if sub_name not in ignore_neutral_titles:
						# female [0], male [1]
						is_a_last_name = isLastName(gne_tree, sub_name)
						load_prob = loaded_gender_model.predict_proba(dt([sub_name.title()]))[0]
						#print("\tprobability: {0}\n".format(load_prob))
						if is_a_last_name: # if last name, weigh less than other names
							#print("'{0}' is a last name, will weight less".format(sub_name))
							load_prob = load_prob*weight_last_name_less
						female_prob += load_prob[0]
						male_prob += load_prob[1]
				#print("\t  updated: f={0}, m={1}".format(female_prob, male_prob))

			#if (abs(male_prob - female_prob) < 0.02): #within 2 percent, undeterminex
			#	gender_is = "UNDETERMINED"
			#else:
			gender_is = 'Male' if male_prob > female_prob else 'Female'

		#print("The name '{0}' is most likely {1}\nFemale: {2:.5f}, Male: {3:.5f}\n".format(full_name, gender_is, female_prob, male_prob))
		gender_gne[full_name] = gender_is
	return gender_gne

def isLastName(gne_tree, sub_name):
	# determine if the name is likely to be the last name
	#{'Samsa': ['Samsa'], 'Gregor': ['Gregor', 'Gregor Samsa']}
	# last name is the most common last element in a name and has no futher sub-roots
	# last name will be weighted less, if there are other elements present
	is_last_name = False

	for key, value in gne_tree.iteritems():
		if sub_name in key:
			if sub_name in key.split()[-1] and len(value) > 1: # if in the last position and isn't the only value {'John': ['John']}
				is_last_name = True
	#print("'{0}' is a last name = {1}".format(sub_name, is_last_name))
	return is_last_name

def loadDTModel():
	# load saved gender model from gender_name_tagger
	from sklearn.externals import joblib # save model to load
	model_file_dir = 'gender_name_tagger'
	updated_saved_model = [f for f in os.listdir(model_file_dir) if 'pipeline_gender_saved_model' in f][0]
	print("LOADING SAVED GENDER NAME MODEL: {0}".format(updated_saved_model))
	pipeline_loaded = joblib.load('{0}/{1}'.format(model_file_dir, updated_saved_model))
	return pipeline_loaded

def DT_features(given_name):
	test_given_name = ['corette', 'corey', 'cori', 'corinne', 'william', 'mason', 'jacob', 'zorro'] #small test
	FEATURE_TAGS = ['first_letter', 
				'first_2_letters',
				'first_half',
				'last_half',
				'last_2_letters',
				'last_letter',
				 'length_of_name']
	features_list = []
	name_features = [given_name[0], given_name[:2], given_name[:len(given_name)/2], given_name[len(given_name)/2:], given_name[-2:], given_name[-1:], len(given_name)]
	#[['z', 'zo', 'zo', 'rro', 'ro', 'o', 5], ['z', 'zo', 'zo', 'rro', 'ro', 'o', 5]]
	features_list = dict(zip(FEATURE_TAGS, name_features))
	return features_list

def gneHierarchy(character_entities_group, over_correct_for_multiple_title):
	# merge gne into a dict for look up
	'''
	key: Dr Urbino
	{'Dr': [['Dr', 'Dr Juvenal Urbino', 'Dr Urbino'], ['Urbino']], 
	'Urbino': [['Dr', 'Dr Juvenal Urbino', 'Dr Urbino'], ['Urbino']]}
	 '''
	# if there are a name with a different version of the title, include both
	if over_correct_for_multiple_title:
		character_entities_group, found_similar = addNameWithSameTitle(character_entities_group) # add names with different titles
	character_split_group = [x.split() for x in character_entities_group]
	character_split_group = sorted(character_split_group, key=len, reverse=True)
	gne_tree = defaultdict(dict)
	gne_dict_sub = {}

	for longer_name in character_split_group:
		#print("{0} IS NOT in gne_tree: {1}".format(" ".join(longer_name), gne_tree))
		#print("longer: {0}".format(longer_name))
		already_in_tree = any(" ".join(longer_name) in g for g in gne_tree)
		if not already_in_tree: # if not already in a sub tree
			if len(longer_name) > 1 or len(longer_name[0]) > 1: # ignore intials 'C'
				#print("base: {0}".format(longer_name))
				#print("base: {0}".format(" ".join(longer_name)))
				for sub_long_name in longer_name:
					gne_tree_word_tree = []
					#print("sub: {0}".format(sub_long_name))
					gne_tree_word_tree.append(sub_long_name)
					for smaller_name in character_entities_group:
						name_with_caps = sub_long_name
						is_sub_capitalized = sub_long_name.isupper()
						if is_sub_capitalized:
							name_with_caps = sub_long_name.title()
						if name_with_caps in smaller_name.split() and name_with_caps not in connecting_words:
							# store only honorific titles that include elements of the same name
							# 'Dr Juvenal Urbino' NOT 'Dr Lacides Olivella', but 'Dr Juvenal Urbino' and 'Dr Urbino' 
							if name_with_caps in all_honorific_titles and len(longer_name) > 1:
								if any(i.title() in longer_name for i in smaller_name.split() if i.title() not in all_honorific_titles):
									#print("\t\tindex: {0}".format(smaller_name.split().index(sub_long_name.title())))
									sub_name_join = " ".join(smaller_name.split()[smaller_name.split().index(sub_long_name.title()):])
									#print("\t\t\n\n\nnewfound: {0}".format(sub_name_join))
									#print("sub_name_join.title() not in gne_tree_word_tree = {0}".format(sub_name_join.title() not in gne_tree_word_tree))
									if sub_name_join.title() not in gne_tree_word_tree:
										gne_tree_word_tree.append(sub_name_join)
										if over_correct_for_multiple_title:
											# add other versions of the same name: "Capt Nemo" and "Captian Nemo"
											for potential_conflict in found_similar:
												#print("sub_name_join in potential_conflict = {0}".format(sub_name_join in potential_conflict))
												if sub_name_join in potential_conflict:
													for other_name in potential_conflict:
														if other_name != sub_name_join:
															if len(other_name.split()) > 1:
																sub_name_first_name = sub_name_join.split()[1]
																sub_name_last_name = sub_name_join.split()[-1]
																other_name_first_name = other_name.split()[1]
																other_name_last_name = other_name.split()[-1]
																if sub_name_first_name == other_name_first_name or other_name_last_name == sub_name_last_name:
																	#print("current = {0}".format(sub_name_join))
																	#print("first '{0}' = '{1}'".format(sub_name_first_name, other_name_first_name))
																	#print("last '{0}' = '{1}'".format(sub_name_last_name, other_name_last_name))
																	#print("new = {0}".format(other_name))
																	#print("\n")
																	gne_tree_word_tree.append(other_name)
							else:
								if name_with_caps not in connecting_words:
									# save non-caps version of a name
									sub_name_join = " ".join(smaller_name.split()[smaller_name.split().index(name_with_caps):])
									#print("\t\tsub orig: {0}".format(sub_long_name))
									#print("\t\tnewfound: {0}\n".format(sub_name_join.upper()))
									if sub_name_join not in gne_tree_word_tree:
										gne_tree_word_tree.append(sub_name_join)
					#print("\ttotal found: {0}".format(gne_tree_word_tree))
					#print("NEW DICT ITEM {0}:{1}\n".format(sub_long_name, gne_tree_word_tree))
					if sub_long_name not in connecting_words:
						gne_tree[" ".join(longer_name)][sub_long_name] = gne_tree_word_tree
					gne_tree_word_tree = []
	gne_tree = dict(gne_tree)
	# common first words to ignore: example (Poor, Dear, etc...)
	# find elements to remove if they are part of words_to_ignore

	# update keys to exclude words to ignore
	gne_tree = removeIgnoreWordsKeySubtree(gne_tree, is_sub_tree=False)
	# update values within the sub-dictionaries
	for key, sub_tree in gne_tree.iteritems():
		#print("######################REMOVE FROM SUBTREE###################")
		#print("before: {0}".format(gne_tree[key]))
		gne_tree[key] = removeIgnoreWordsKeySubtree(sub_tree, is_sub_tree=True)
		#print("after: {0}".format(gne_tree[key]))

	#for key, value in gne_tree.iteritems():
	#		print("key: {0}".format(key))
	#		print("value: {0}\n".format(value))
	#print("\n")
	return gne_tree

def addNameWithSameTitle(name_list):
	# run for all potential names to include both Mister and Mr in a name's subtree
	# final step: if the character has the same gender title "Mister Kurtz" and "Mistah Kurtz", group together
	# does not run for all male titles, just ones that are the same meaning
	updated_list = list(name_list)

	for p_n in name_list:
		if bool(set(p_n.split()) & set(all_equal_titles)):
			#print("NAME WITH TITLE THAT HAS MULTIPLE VERSION = {0}".format(key))
			potential_names_with_equal_titles.append(p_n)

	found_similar = defaultdict(list)
	if potential_names_with_equal_titles != []:
		if len(potential_names_with_equal_titles) > 1: # if there might be a conflict
			for conflict_name in potential_names_with_equal_titles:
				male_found  = [sublist for sublist in male_equ_titles if conflict_name.split()[0] in sublist]
				female_found  = [sublist for sublist in female_equ_titles if conflict_name.split()[0] in sublist]
				neutral_found  = [sublist for sublist in neutral_equ_titles if conflict_name.split()[0] in sublist]
				# find all versions of the name and the title that exist
				if male_found != []:
					#print("found in male")
					found_similar[", ".join(male_found[0])].append(conflict_name)
				if female_found != []:
					#print("found in female")
					found_similar[", ".join(female_found[0])].append(conflict_name)
				if neutral_found != []:
					#print("found in neutral")
					found_similar[", ".join(neutral_found[0])].append(conflict_name)

	# remove the other versions of the name, keep the longest name
	found_similar = dict(found_similar)
	list_of_similar = []
	for group, name_list in found_similar.iteritems():
		if len(name_list) > 1:
			#print(group.split(", "))
			check_list = list(name_list)
			#print(name_list)
			for name_p in name_list:
				title = name_p.split()[0]
				if name_p.split()[1:] != []:
					check_name = " ".join(name_p.split()[1:])
					for name_c in check_list:
						if name_p != name_c:
							if check_name.split()[0] in name_c or check_name.split()[-1] in name_c: # match the first name or the last name
								duplicate_title = name_c.split()[0]
								#print("duplicate found: {0}".format(name_c))
								new_name_to_add = duplicate_title + " " + check_name
								#print("NEW TO ADD: {0}".format(new_name_to_add))
								updated_list.append(new_name_to_add)
								for sub_list_index, similar_potential in enumerate(found_similar.values()):
									if name_c in similar_potential:
										if new_name_to_add not in found_similar.values()[sub_list_index]:
											found_similar.values()[sub_list_index].append(new_name_to_add) # add new value to sub instex for comparison in gne tree
								
	updated_list = list(set(updated_list))
	list_of_similar = found_similar.values()
	return updated_list, list_of_similar

def removeIgnoreWordsKeySubtree(tree_to_update, is_sub_tree=False):
	# remove all keys that contain words to ignore and then ignore all values in the sub-trees dictionaries
	tree_to_remove = []
	found_sub_names_to_ignore = []
	updated_key = {}
	for key, sub_tree in tree_to_update.iteritems():
		new_key = []
		contains_words_to_ignore = False
		# REMOVE KEYS THAT CONTAIN WORDS TO IGNORE
		for sub_name in key.split():
			#print("{0} in words_to_ignore = {1}".format(sub_name.title(), sub_name.title() in words_to_ignore))
			#print("{0} not in words_to_ignore = {1} and not sub_name.isupper() = {1}".format(sub_name.title() not in words_to_ignore, not sub_name.isupper()))
			if sub_name.title() not in words_to_ignore and not sub_name.isupper(): # Remove 'SOUTHLAND White Fang' from chapter titles
				if sub_name not in connecting_words and not sub_name.islower():
					new_key.append(sub_name) # only store values without words to ignore
			else:
				contains_words_to_ignore = True
				found_sub_names_to_ignore.append(sub_name)
			if sub_name.isupper():
				contains_words_to_ignore = True
				found_sub_names_to_ignore.append(sub_name)
		if not is_sub_tree:
			if len(key.split()) == 1:
				if key.title() in all_honorific_titles: # remove gnes that are just 'Lord'
					tree_to_remove.append(key) # remove value
		else:
			new_value = []
			for sub_value in sub_tree:
				contains_value_to_ignore = False
				#print("sub_value = {0}".format(sub_value))
				for cnt, word in enumerate(sub_value.split()):
					#print("current new value = {0}".format(new_value))
					#print("{0} in words_to_ignore = {1}".format(word.title(), word.title() in words_to_ignore))
					if word.title() not in words_to_ignore:
						#print("\tword to include = {0}".format(word))
						new_value.append(word)
					else:
						#print("word to ignore = {0}".format(word))
						contains_value_to_ignore = True
				if contains_value_to_ignore:
					join_word = " ".join(new_value)
					sub_tree[cnt] = join_word
					#print("NEW VALUE = {0}".format(" ".join(new_value)))
					#print(sub_tree)
				#print("\n")
				new_value = []
			# remove duplicates if updating word makes it the same as another
			if is_sub_tree:
				for key, values in tree_to_update.iteritems():
					tree_to_update[key] = list(set(values))
		
		#print("contains_words_to_ignore = {0}, {1}\n".format(contains_words_to_ignore, new_key))
		if contains_words_to_ignore: # if it contains words to ignore, use new key without the words to ignore
			if not new_key: # if the entire word was only words to ignore
				tree_to_remove.append(key) # remove value
			else:
				#print("'{0}' becomes '{1}'\n".format(key, " ".join(new_key)))
				updated_key[key] = " ".join(new_key)
			for sub_tree_to_delete in found_sub_names_to_ignore:
				tree_to_remove.append(sub_tree_to_delete)
			for s_t in sub_tree:
				if any(ig in " ".join(s_t) for ig in words_to_ignore):
					# only keep the parts of substrings that have element
					tree_to_remove.append(s_t)
						
	# remove all values in a named ent that are in words to ignore "Poor Dickens" Becomes "Dickens"
	# also removes sub_trees for "poor"
	for to_remove in tree_to_remove:
		if to_remove in tree_to_update.keys():
			base_gne_key = tree_to_update.pop(to_remove)
			#print("base_gne_key = {0}".format(base_gne_key))
		else:
			for sub_dict in tree_to_update.values():
				if to_remove in sub_dict:
					sub_tree_removed = sub_dict.pop(to_remove)
					#print("subtree to remove from '{0}' = {0}".format(sub_dict, sub_tree_removed))
	# rename old key values
	for old_key_to_update, new_key in updated_key.iteritems():
		if old_key_to_update in tree_to_update.keys():
			if new_key in tree_to_update.keys():
				tree_to_update[new_key].update(tree_to_update.pop(old_key_to_update)) # add to an existing dictionary
			else:
				tree_to_update[new_key] = tree_to_update.pop(old_key_to_update) # 'Dickens' mapped to the dictionary value for 'Poor Dickens'
	return tree_to_update

def identifyCharacterOfInterest(pronoun_noun_dict, gne_tree, gender_gne, print_info=False):
	print("\nIDENTIFY CHARACTER OF INTEREST\n")
	# count instances of a name appearing
	'''
	{'Brussels': 1, 'Mrs Darling': 4, 'East': 1, 'Miss Fulsom': 1,
	 'Neverland': 1, 'Michael': 2, 'Kindergarten': 1, 'Margaret': 3,
	 'John': 2, 'Wendy': 11, 'Jane': 1, 'Mr Darling': 4, 'Peter': 3, 
	 'George': 1, 'Napoleon': 1}
	'''
	name_counter = {}
	is_first_person_text = False
	main_character_is = ''
	
	pronoun_counter = Counter(pronoun_noun_dict['found_pronoun_value'])
	#print(pronoun_noun_dict['found_pronoun_value'])
	most_common_pronoun = pronoun_counter.most_common(1)[0][0].title() 
	first_person_pronouns = ['I', 'Me', 'Myself','My']
	if most_common_pronoun in first_person_pronouns:
		is_first_person_text = True
		
	# include all sub instances into a larger instance
	for counter, proper_name in enumerate(pronoun_noun_dict['found_proper_name_value']):
		# weight the first name that appear in the text an additional amount
		#print("'{0}' in gne_tree.keys() = {1}".format(proper_name, proper_name in gne_tree.keys()))
		is_first_name_mentioned = False
		if counter == 0:
			is_first_name_mentioned = True
			additional = 0#len(pronoun_noun_dict['found_proper_name_value'])/10 # random additional amount (TODO)
			if additional < 1:
				additional = 1
		if proper_name not in gne_tree.keys(): # if not in keys, add to an existing key
			#print("NOT FOUND IN TOP OF TREE")
			#print("'{0}' not in gne_tree.keys()".format(proper_name))
			#print(gne_tree.keys())
			contains_sub_name = []
			for sub_proper_name in proper_name.split():
				for gne_key in gne_tree.keys():
					if sub_proper_name in gne_key:
						contains_sub_name.append(gne_key)
			#print("contains_sub_name = {0}".format(contains_sub_name))

			if contains_sub_name != []:
				contains_sub_name = max(contains_sub_name, key=len)
				#print("max = {0}".format(contains_sub_name))
				if contains_sub_name not in name_counter.keys():
					name_counter[contains_sub_name] = 1
					if is_first_name_mentioned:
						name_counter[contains_sub_name] += additional
				else:
					name_counter[contains_sub_name] += 1
		else:
			if proper_name not in name_counter.keys():
				name_counter[proper_name] = 1
				if is_first_name_mentioned:
					name_counter[proper_name] += additional
			else:
				name_counter[proper_name] += 1

	import operator
	# merge all final values together based on trees: so Mr. Holmes is matches with Sherlock Holmes (longer gne)
	# convert dic to a list of tuples
	sorted_reverse = sorted(name_counter.items(), key=lambda x:x[1])[::-1] # store from largest to smallest
	#print(sorted_reverse)
	max_gne_tree = {}
	found_sub_tree_for_comparison_length = defaultdict(list)
	#print('\n')
	for key, sub_tree in gne_tree.iteritems():
		#print("key = {0}".format(key))
		max_gne_tree[key] = 0
		if key not in found_sub_tree_for_comparison_length[key]:
			found_sub_tree_for_comparison_length[key].append(key)
		if key in name_counter.keys():
			#print("\t'{0}' in {1}".format(key, name_counter[key]))
			max_gne_tree[key] += name_counter[key]
		#print("sub tree = {0}".format(sub_tree))
		for k, v in sub_tree.iteritems():
			#print('\tfirst level sub-tree element = {0}'.format(k))
			if k in name_counter.keys() and k not in max_gne_tree.keys():
				if not k not in found_sub_tree_for_comparison_length[key]:
					found_sub_tree_for_comparison_length[key].append(k)
				#print("\t#########'{0}' in {1}".format(k, name_counter[k]))
				max_gne_tree[key] += name_counter[k]
			for sub in v:
				#print('\t\tsecond level sub-tree element = {0}'.format(sub))
				if sub in name_counter.keys() and sub not in max_gne_tree.keys():
					#print("\t\t#########'{0}' in {1}".format(sub, name_counter[sub]))
					if sub not in found_sub_tree_for_comparison_length[key]:
						found_sub_tree_for_comparison_length[key].append(sub)
					max_gne_tree[key] += name_counter[sub]
		#print("final = {0}".format(max_gne_tree[key]))
		#print("final c = {0}".format(found_sub_tree_for_comparison_length[key]))
		#print('\n')
		if max_gne_tree[key] == 0:
			max_gne_tree.pop(key) # remove any element with no instances
	found_sub_tree_for_comparison_length = dict(found_sub_tree_for_comparison_length)
	sorted_final = sorted(max_gne_tree.items(), key=lambda x:x[1])[::-1] # store from largest to smallest
	#print(sorted_final)
	final_gne = {}
	character_with_sub_types = {}
	found_list = []
	# merge two trees if they have the same comparison (use longer gne)
	for key, v in found_sub_tree_for_comparison_length.iteritems():
		longer_name = ''
		#print("v = {0}".format(v))
		compare_values = [y for x in gne_tree[key].values() for y in x]
		if v not in compare_values:
			compare_values.extend(v) # add the key to the list of branch values
		compare_values = list(set(compare_values))
		longer_name = max(compare_values, key=len)
		#print("\nlongest name = {0}".format(longer_name))
		#print("existing keys = {0}".format(final_gne.keys()))
		#print("{0}: should create = {1}".format(key, longer_name not in final_gne.keys() and key not in final_gne.keys()))
		#print("gne_tree[key] values = {0}".format(compare_values))
		if longer_name not in final_gne.keys() and key not in final_gne.keys(): # check that key doesn't already exist for the name to use
			#print("longer name not in found list = {0}".format(longer_name not in found_list))
			if longer_name not in found_list: # do not include values that are already in list (even if they have a different sub_tree)
				to_update_key_with_longer_key = False
				if bool(set(final_gne.keys()) & set(compare_values)):
					#print("a key with the same sub_tree already exist = {0}".format(bool(set(final_gne.keys()) & set(compare_values))))
					existing_key = list(set(compare_values).intersection(final_gne.keys()))[0]
					#print("shared key = {0}".format(existing_key))
					#print("len(longer_name) {0} > len(existing_key) {1} = {2}".format(len(longer_name), len(existing_key), len(longer_name) > len(existing_key)))
					if len(longer_name) >= len(existing_key): # if current longer is greater than or equal, replace existing
						found_list.extend(compare_values)
						#print("IS LONGER REPLACE '{0}' with '{1}'".format(existing_key, longer_name))
						to_update_key_with_longer_key = True
						#print("{0} in final_gne = {1}".format(existing_key, existing_key in final_gne.keys()))
						final_gne.pop(existing_key) # remove existing key to replace
						#print("{0} in final_gne = {1}".format(existing_key, existing_key in final_gne.keys()))
						character_with_sub_types.pop(existing_key)
				else:
					to_update_key_with_longer_key = True
				if to_update_key_with_longer_key: 
					found_list.extend(compare_values)
					final_gne[longer_name] = 0
					character_with_sub_types[longer_name] = compare_values
					for sub_name in compare_values:
						if sub_name in name_counter.keys():
							#print("final_gne[{0}] += {1}".format(sub_name, name_counter[sub_name]))
							#print(name_counter[sub_name])
							final_gne[longer_name] += name_counter[sub_name]
						#print("final count = {0}\n".format(final_gne[longer_name]))
	# clean up final_gne: remove empty, update counters
	for k in final_gne.keys():
		if final_gne[k] == 0:
			final_gne.pop(k) # if empty, remove

	# include names with and without a title (if a title exists)
	for key, sub_tree in character_with_sub_types.iteritems():
		#print(key)
		for name in sub_tree:
			add_new_name = []
			# create an instance of all names in sub directory with and without a title
			if bool(set(name.split()) & set(all_honorific_titles)): # if word contains a title
				new_name_without_title = []
				for sub in name.split():
					contains_title = False
					if sub not in all_honorific_titles:
						new_name_without_title.append(sub)
						contains_title = True
					if contains_title:
						new_name = " ".join(new_name_without_title)
						if new_name not in sub_tree:
							#print("NEW NAME TO ADD TO '{0}' is {1}".format(key, new_name))
							add_new_name.append(new_name)
			sub_tree.extend(add_new_name) # add name without a title as well as the version with a title
			character_with_sub_types[key] =  [x for x in sub_tree if x not in all_honorific_titles] # remove a title that appears by itself
			# save updates to the dict
		#print(sub_tree)
		#print("\n")
	
	sorted_final = sorted(final_gne.items(), key=lambda x:x[1])[::-1] # store from largest to smallest
	#print("ALL GROUPED CHARACTERS: \n{0}\n".format(sorted_final))
	#print("TEXT: {0}".format(pronoun_noun_dict['full_text']))
	#print("\n")
	#for noun_index in pronoun_noun_dict['found_proper_name_index']:
	#	print(pronoun_noun_dict['full_text'][noun_index[0]:noun_index[1]])

	if print_info:
		print("IS FIRST PERSON TEXT: {0}".format(is_first_person_text))
		main_character_high_value = sorted_final[0][1]
		main_character_total = [k for k in sorted_final if k[1] == main_character_high_value]
		tie_found = False
		if len(main_character_total) > 1: # if more than one value have the same max
			tie_found = True
		main_character = sorted_final[0][0]
		if not is_first_person_text:
			if tie_found:
				print("Tie for character of focus found")
			lst_genders = []
			for tie in main_character_total:
				lst_genders.append(gender_gne[main_character])
			#print(most_common_pronoun)
			if most_common_pronoun in female_pronouns:
				print("\nPredicted gender of main character is 'Female' {0}: {1}".format(pronoun_counter.most_common(1), 'Female' in lst_genders))
			if most_common_pronoun in male_pronouns:
				print("\nPredicted gender of main character is 'Male' {0}: {1}".format(pronoun_counter.most_common(1), 'Male' in lst_genders))
		print("\nCHARACTER OF INTEREST: {0}\n".format(main_character_total))
		top_characters = sorted_final[len(main_character_total):len(main_character_total)+5]
		print("ADDITIONAL TOP CHARACTERS OF INTEREST: {0}\n".format(top_characters)) # print from highest to lowest
		
	# return a dict with the top character name and the sub elements:
	# { Master Colin: ['Master Colin', 'Colin', 'Master', 'Colin Craven']}

	#for key, value in character_with_sub_types.iteritems():
	#	if "Holmes" in key:
	#		print(key)
	#		print(value)
	return character_with_sub_types

def interactionsPolarity(character_gne_tree_dict, line_by_line_dict, filename):
	# break apart text into interactions
	# each number in the chunk is a sentence
	'''
	for key, sub_dict in line_by_line_dict.iteritems():
		print(key)
		print(sub_dict['full_text'])
		print(sub_dict['found_proper_name_value'])
		print(sub_dict['found_proper_name_index'])
		print(sub_dict['found_pronoun_value'])
		print(sub_dict['found_pronoun_index'])
		print(sub_dict['found_all_brackets'])
		print("\n")
	'''
	# create a sub_list of the line id to organize
	# [0, 1, 2, 3, 4, 5] -> [[0, 1], [2, 3], [4, 5]]
	# 
	ordered_lines = line_by_line_dict.keys()
	total_sentences_in_each_chunk = 8 # sentences in each group
	split_sentences = len(ordered_lines) / total_sentences_in_each_chunk
	if split_sentences > len(ordered_lines) or split_sentences < 1:
		split_sentences = 3 # debugging smaller text
	
	list_with_chunks = []
	split_num = 1.0/split_sentences*len(ordered_lines)
	for i in range(split_sentences):
		list_with_chunks.append(ordered_lines[int(round(i*split_num)):int(round((i+1)*split_num))]) # break into roughly thirds
	
	grouping_of_chunks = {} # maps group id to the sentences: {0: [0, 1], 1: [2, 3], 2: [4, 5]}
	for group_id, sub_list in enumerate(list_with_chunks):
		grouping_of_chunks[group_id] = sub_list
	#for i in list_with_chunks: # print the length of each chunk
	#	print len(i), 
	#print("\n")
	#print(list_with_chunks)
	#print(len(list_with_chunks))
	#print(grouping_of_chunks)
	#print(grouping_of_chunks.keys())

	# find proper noun in raw text
	grouping_of_characters = {} # group id: characters interacting in a scan of text
	characters_in_thirds = [[line_by_line_dict[x]['found_proper_name_value'] for x in sublist] for sublist in list_with_chunks]
	for group_num, character in enumerate(characters_in_thirds):
		#print("group_num = {0}".format(group_num))
		grouping_of_characters[group_num] = []
		for line_num, found_c in enumerate(character):
			#print("\tline_num = {0}".format(line_num))
			#print("\tcharacters in group = {0}".format(found_c))
			grouping_of_characters[group_num].extend(found_c)
	#print("Grouping Characters from raw text (ORIGINAL): \n{0}".format(grouping_of_characters))
	#print("\n")
	# convert proper noun to gne tree max (from character interactions)
	# Colin mapped with Colin Craven

	for group_id, characters_interacting in grouping_of_characters.iteritems():
		for lst_id, character in enumerate(characters_interacting):
			#print("Character = {0}".format(character))
			if character not in character_gne_tree_dict.keys():
				#print("NEED TO UPDATE TO MATCH TOP OF TREE")
				for key, sub_tree_name in character_gne_tree_dict.iteritems():
					if character in sub_tree_name:
						#print("FOUND UPPER TREE MATCH IN '{0}' for '{1}'\n".format(key, character))
						characters_interacting[lst_id] = key
			#print("\n")
	# keep only one instance of a character name
	for sentence_id, character_lst in grouping_of_characters.iteritems():
		grouping_of_characters[sentence_id] = list(set(character_lst))
		
	#print("Grouping characters with top of gne (UPDATED): \n{0}\n".format(grouping_of_characters))
	
	# Sentiment anaylsis for each sentence in a chunk
	from textblob import TextBlob
	sentence_id_polarity = {}
	for group_id, sub_sentences in grouping_of_chunks.iteritems():
		for sentence_id in sub_sentences:
			text_sentence = TextBlob(line_by_line_dict[sentence_id]['full_text'])
			sentiment_pole = text_sentence.sentiment.polarity
			# TODO: if sentiment is neutral, make it similar to the previous value
			sentence_id_polarity[sentence_id] = sentiment_pole # store each sentiment in a sublist
	#print(sentence_id_polarity)
	
	average_polarity_sentence = 0.0
	# map each interaction and find polarity of relationships over time
	character_interactions_polarity = {} # (group_id, sentence_id) = 
	for group_id, sentence_lst in grouping_of_chunks.iteritems():
		average_polarity_sentence += sentence_id_polarity[sentence_id]
		if grouping_of_characters[group_id] != []: # if there are characters in a group of sentences
			for sentence_id in sentence_lst:
				if group_id in character_interactions_polarity.keys():
					character_interactions_polarity[group_id] += sentence_id_polarity[sentence_id]
				else:
					character_interactions_polarity[group_id] = sentence_id_polarity[sentence_id]
			#character_interactions_polarity[group_id].append(grouping_of_characters[group_id])
		else:
			character_interactions_polarity[group_id] = 0.0 # empty

	# Save polarity and tagged sentence to a csv for graphing
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	output_filename = "sent_{0}.csv".format(given_file.upper())

	average_polarity_group = 0.0
	fieldnames = ['GROUP_ID', 'SENTENCE_INDEX', 'CHARACTERS', 'SENTENCE_POLARITY', 'GROUP_POLARITY']
	with open('sentiment_csv/{0}'.format(output_filename), 'w') as sent_data:
		writer = csv.DictWriter(sent_data, fieldnames=fieldnames)
		writer.writeheader() 
		for group_id, sentence_lst in grouping_of_chunks.iteritems():
			for sentence_id in sentence_lst:
				average_polarity_group +=  character_interactions_polarity[group_id]
				writer.writerow({'GROUP_ID': group_id,
								'SENTENCE_INDEX': sentence_id,
								'CHARACTERS': ", ".join(grouping_of_characters[group_id]),
								'SENTENCE_POLARITY': sentence_id_polarity[sentence_id],
								'GROUP_POLARITY': character_interactions_polarity[group_id]
								})

	print("SENTIMENT for each group/sentence CSV saved as {0}".format(output_filename))
	print("Average polarity: Group [{0:.5f}] vs. Sentence [{1:.5f}]".format(average_polarity_sentence / len(ordered_lines), 
																			(average_polarity_group / len(grouping_of_chunks.keys())/split_sentences)))
	# contains a list of characters in a section and the polarity of the section
	#sorted_groups = sorted(character_interactions_polarity.items(), key=lambda x:x[0])
	#for i in sorted_groups:
	#	print(i)
	return character_interactions_polarity

########################################################################
# NETWORK GRAPHS AND TREE
def generateGNEtree(gne_tree, filename):
	print("\nGENERATE TREE FROM GNE")
	import pygraphviz
	from networkx.drawing.nx_agraph import graphviz_layout

	gne_imge_directory_name = os.path.splitext(filename)[0].upper()
	if not os.path.exists("gne_trees/{0}".format(gne_imge_directory_name)):
		os.makedirs("gne_trees/{0}".format(gne_imge_directory_name))
	for key, value in gne_tree.iteritems():
		print("\ngne base name: {0}\n{1}".format(key, value))
	
	for key, value in gne_tree.iteritems():
		G = nx.DiGraph(name="GNE name tree: {0}".format(key))
		G.add_node(key) # root is the gne base name (Dr Juvenal Urbino)
		
		# add child (the name broken into parts)
		for split_name in key.split():
			G.add_edge(key, split_name)
		#for sub_name in value:
		#	print(sub_name)
		#G.add_edge(key, 
	
		nx.nx_pydot.write_dot(G, 'gne_trees/{0}/{1}.dot'.format(gne_imge_directory_name, key.replace(" ", "_")))
		plt.title("GNE name tree: {0}".format(key))
		pos=nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
		nx.draw(G, pos, with_labels=True, arrows=False, node_size=1600, cmap=plt.cm.Blues, node_color=range(len(G)))
		#nx.draw(G, with_labels=False, arrows=False)
		plt.savefig("gne_trees/{0}/GNE_{1}.png".format(gne_imge_directory_name, key.replace(" ", "_")))

def networkGraphs(gne_tree):
	print("\ngenerating network graphs of interactions")

	gne_labels = {} # set up same color for names in the same gne tree

	fig = plt.figure()
	fig.set_figheight(10)
	fig.set_figwidth(10)
	import graphviz

	G = nx.MultiGraph(name="Testing graph")

	for key, value in gne_tree.iteritems():
		print(key)
		G.add_node(key)
		for value_lst in value[0]:
			for v in value_lst:
				if v not in connecting_words:
					print(v)
					c = 'r'
					print(len(v))
					G.add_edge(key, v, color='red')
					#if len(v) > 10:
					#	G.add_edge(key, v) # add a second edge
		print("\n")

	print(nx.info(G))
	print("density={0}".format(nx.density(G)))
	for node in nx.degree(G):
		print("{0} has {1} connections".format(node[0], node[1]))
	nx.draw(G, with_labels=True, cmap=plt.cm.Blues, node_color=range(len(G)), node_size=2300)
	print("\n")
	plt.savefig("relationships_gne.png")
	print("finished generating graph")
	'''
	G=nx.star_graph(20)
	pos=nx.spring_layout(G)
	colors=range(20)
	nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)

	G=nx.random_geometric_graph(200,0.125)
	# position is stored as node attribute data for random_geometric_graph
	pos=nx.get_node_attributes(G,'pos')

	# find node near center (0.5,0.5)
	dmin=1
	ncenter=0
	for n in pos:
		x,y=pos[n]
		d=(x-0.5)**2+(y-0.5)**2
		if d<dmin:
			ncenter=n
			dmin=d

	# color by path length from node near center
	p=nx.single_source_shortest_path_length(G,ncenter)

	plt.figure(figsize=(8,8))
	nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
	nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),
						   node_size=80,
						   node_color=p.values(),
						   cmap=plt.cm.Reds_r)

	plt.xlim(-0.05,1.05)
	plt.ylim(-0.05,1.05)
	plt.axis('off')
	'''
	
########################################################################
# DATA ANAYLSIS
def percentagePos(total_words, csv_dict):
	# prints the percentage of the text that is pronouns vs. nouns
	percentageDict =  {}
        #TODO: finish percentages dictionary to pass into the csv and store if filename is new/modified
	pronouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("PRP")

	percentageDict['pronouns_count'] = pronouns_count

	pronoun_percentage = float(pronouns_count)/float(total_words)
	print("\npercent pronouns = {0:.3f}% of all text".format(pronoun_percentage*100.0))
	percentageDict['pronoun_in_all_words'] = pronoun_percentage

	proper_nouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNP") # proper noun singular
	proper_nouns_count += [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNPS") # proper noun plural: spaniards

	percentageDict['proper_nouns_count'] = proper_nouns_count

	proper_nouns_percentage = float(proper_nouns_count) / float(total_words)
	print("percent proper nouns = {0:.3f}% of all text".format(proper_nouns_percentage*100))
	percentageDict['proper_noun_in_all_words'] = proper_nouns_percentage

	nouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NN") # nouns: ship, language
	nouns_count += [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNS") # plurla noun: limbs


	nouns_percentage = float(nouns_count) / float(total_words)
	print("percent nouns = {0:.3f}% of all text".format(nouns_percentage*100))
	percentageDict['all_noun_in_all_words'] = nouns_percentage

	nouns_ratio= [pos.UPOSTAG for _, pos in csv_dict.iteritems()].count("NOUN")
	proper_to_ratio_percentage = float(proper_nouns_count) / float(nouns_ratio)
	print("proper nouns make up {0:.3f}% of all nouns".format((proper_to_ratio_percentage*100)))
	percentageDict['proper_noun_in_all_nouns'] = proper_to_ratio_percentage

	percentageDict['nouns_count'] = nouns_ratio

	all_nouns_to_ratio_percentage = float(nouns_count) / float(nouns_ratio)
	print("regular nouns make up {0:.3f}% of all nouns".format((all_nouns_to_ratio_percentage*100)))
	percentageDict['regular_nouns_in_all_nouns'] = all_nouns_to_ratio_percentage

	print("Text is approximately {0} words".format(total_words))
	percentageDict['text_size'] = total_words
	return percentageDict  

def saveDatatoCSV(filename, percentDict):
	# save data from each run to a csv for graphing (if text is new or has been updated)
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	output_filename = "nounData_allText.csv"
	print("\n")

	fieldnames = ['FILENAME', 'TEXT_SIZE', 
				  'ALL_NOUNS_IN_ALL_WORDS', 'PRONOUNS_IN_ALL_WORDS',
				  'PROPER_NOUNS_IN_ALL_WORDS', 'REGULAR_NOUNS_IN_ALL_NOUNS',
				  'PROPER_NOUNS_IN_ALL_NOUNS', 'GNE_IN_ALL_WORDS',
				  'GNE_IN_ALL_NOUNS']

	if not os.path.isfile("plot_percent_data/{0}".format(output_filename)): # if it doesn't exist, create csv file with dict data
		with open('plot_percent_data/{0}'.format(output_filename), 'w') as noun_data:
			writer = csv.DictWriter(noun_data, fieldnames=fieldnames)
			writer.writeheader() 
			writer.writerow({'FILENAME': os.path.basename(os.path.splitext(filename)[0]), 
							 'TEXT_SIZE': percentDict['text_size'],
							 'ALL_NOUNS_IN_ALL_WORDS': percentDict['all_noun_in_all_words'],
							 'PRONOUNS_IN_ALL_WORDS': percentDict['pronoun_in_all_words'],
							 'PROPER_NOUNS_IN_ALL_WORDS':  percentDict['proper_noun_in_all_words'],
							 'REGULAR_NOUNS_IN_ALL_NOUNS': percentDict['regular_nouns_in_all_nouns'],
							 'PROPER_NOUNS_IN_ALL_NOUNS': percentDict['proper_noun_in_all_nouns'],
							 'GNE_IN_ALL_WORDS': 0.0,
							 'GNE_IN_ALL_NOUNS': 0.0
								})
		print("\n{0} created a new CSV NOUN DATA ".format(given_file.upper()))
	else: # csv file exists, copy data and re-generate 
		stored_results = [] # store old rows
		with open('plot_percent_data/{0}'.format(output_filename), 'r') as noun_data:
			reader = csv.DictReader(noun_data)
			for row in reader:
				stored_results.append(row) # store previous rows

		with open('plot_percent_data/{0}'.format(output_filename), 'w') as noun_data:
			new_file_to_append = os.path.basename(os.path.splitext(filename)[0])
			to_append = True
			writer = csv.DictWriter(noun_data, fieldnames=fieldnames)
			writer.writeheader() 
			for data_row in stored_results:
				if data_row['FILENAME'] == new_file_to_append:
					to_append = False # updated to an existing row rather than appended
					writer.writerow({'FILENAME':  new_file_to_append, 
									 'TEXT_SIZE': percentDict['text_size'],
									 'ALL_NOUNS_IN_ALL_WORDS': percentDict['all_noun_in_all_words'],
									 'PRONOUNS_IN_ALL_WORDS': percentDict['pronoun_in_all_words'],
									 'PROPER_NOUNS_IN_ALL_WORDS':  percentDict['proper_noun_in_all_words'],
									 'REGULAR_NOUNS_IN_ALL_NOUNS': percentDict['regular_nouns_in_all_nouns'],
									 'PROPER_NOUNS_IN_ALL_NOUNS': percentDict['proper_noun_in_all_nouns'],
									 'GNE_IN_ALL_WORDS': 0.0,
									 'GNE_IN_ALL_NOUNS': 0.0
										})
					print("{0} updated in an existing CSV log".format(given_file.upper()))

				else:
					writer.writerow(data_row)
			if to_append: # if the file wasn't found, append to the end
				# add new data to the end (appended)
				writer.writerow({'FILENAME':  new_file_to_append, 
								 'TEXT_SIZE': percentDict['text_size'],
								 'ALL_NOUNS_IN_ALL_WORDS': percentDict['all_noun_in_all_words'],
								 'PRONOUNS_IN_ALL_WORDS': percentDict['pronoun_in_all_words'],
								 'PROPER_NOUNS_IN_ALL_WORDS':  percentDict['proper_noun_in_all_words'],
								 'REGULAR_NOUNS_IN_ALL_NOUNS': percentDict['regular_nouns_in_all_nouns'],
								 'PROPER_NOUNS_IN_ALL_NOUNS': percentDict['proper_noun_in_all_nouns'],
								 'GNE_IN_ALL_WORDS': 0.0,
								 'GNE_IN_ALL_NOUNS': 0.0
									})
				print("{0} (new) appended to end of CSV NOUN DATA ".format(given_file.upper()))

	# save information as dictionary of dictionary values for graphing purposes {filename: {attributes:}}
	csv_data_results = {} # store old rows
	with open('plot_percent_data/{0}'.format(output_filename), 'r') as noun_data:
		reader = csv.DictReader(noun_data)
		for row in reader:
			csv_data_results[row['FILENAME']] = row # store previous rows
	return csv_data_results

def graphGNEvText(previous_csv_data, percent_ratio_dict, noun_pronoun_dict):
	# add column to nounData csv for gne percentage
	print("ADDING COLUMNS FOR GNE PERCENTAGE TO nounData_allText.csv\n")
	output_filename = "nounData_allText.csv"

	fieldnames = ['FILENAME', 'TEXT_SIZE', 
				  'ALL_NOUNS_IN_ALL_WORDS', 'PRONOUNS_IN_ALL_WORDS',
				  'PROPER_NOUNS_IN_ALL_WORDS', 'REGULAR_NOUNS_IN_ALL_NOUNS',
				  'PROPER_NOUNS_IN_ALL_NOUNS', 'GNE_IN_ALL_WORDS',
				  'GNE_IN_ALL_NOUNS']

	# saved updated csv in alphabetical order
	saved_filenames_in_alpha_order = []
	for key, sub_header in previous_csv_data.iteritems():
		saved_filenames_in_alpha_order.append(sub_header['FILENAME'])
	saved_filenames_in_alpha_order = sorted(saved_filenames_in_alpha_order)
	#print("previous files = {0}".format(saved_filenames_in_alpha_order))

	total_gnes = len(noun_pronoun_dict['found_proper_name_value'])
	gne_in_all_nouns = float(total_gnes) / percent_ratio_dict['nouns_count']
	gne_in_all_words = float(total_gnes) / percent_ratio_dict['text_size']

	with open('plot_percent_data/{0}'.format(output_filename), 'w') as gne_data:
		writer = csv.DictWriter(gne_data, fieldnames=fieldnames)
		writer.writeheader() 
		for previous_file in saved_filenames_in_alpha_order:
			writer.writerow({'FILENAME': previous_file, 
							'TEXT_SIZE': previous_csv_data[previous_file]['TEXT_SIZE'],
							 'ALL_NOUNS_IN_ALL_WORDS': previous_csv_data[previous_file]['ALL_NOUNS_IN_ALL_WORDS'],
							 'PRONOUNS_IN_ALL_WORDS': previous_csv_data[previous_file]['PRONOUNS_IN_ALL_WORDS'],
							 'PROPER_NOUNS_IN_ALL_WORDS':  previous_csv_data[previous_file]['PROPER_NOUNS_IN_ALL_WORDS'],
							 'REGULAR_NOUNS_IN_ALL_NOUNS': previous_csv_data[previous_file]['REGULAR_NOUNS_IN_ALL_NOUNS'],
							 'PROPER_NOUNS_IN_ALL_NOUNS': previous_csv_data[previous_file]['PROPER_NOUNS_IN_ALL_NOUNS'],
							 'GNE_IN_ALL_WORDS': gne_in_all_words,
							 'GNE_IN_ALL_NOUNS': gne_in_all_nouns
							})
	# save information as dictionary of dictionary values for graphing purposes {filename: {attributes:}}
	csv_data_results = {} # store old rows
	with open('plot_percent_data/{0}'.format(output_filename), 'r') as noun_data:
		reader = csv.DictReader(noun_data)
		for row in reader:
			csv_data_results[row['FILENAME']] = row # store previous rows
	return csv_data_results
	
def graphPOSdata(csv_data):
	# scatter plot of pronouns, nouns and word length (updated every run/edit)
	'''
	sample {'ALL_NOUNS_IN_ALL_WORDS': '0.17543859649122806',
	'FILENAME': 'sample', 'REGULAR_NOUNS_IN_ALL_NOUNS': '0.7407407407407407',
	'PROPER_NOUNS_IN_ALL_WORDS': '0.06140350877192982', 
	'PRONOUNS_IN_ALL_WORDS': '0.08771929824561403',
	'TEXT_SIZE': '114', 'PROPER_NOUNS_IN_ALL_NOUNS': '0.17543859649122806'}
	'''
	filenames = []
	text_size = []
	all_nouns_in_all_words = []
	pronouns_in_all_words = []
	regular_nouns_in_all_nouns = []
	proper_nouns_in_all_nouns = []
	gnes_nouns_in_all_nouns = []
	gnes_nouns_in_all_words = []
	for filename, subdict_attributes in csv_data.iteritems(): #store all rows in the same index of different lists
		filenames.append(filename)
		text_size.append(int(subdict_attributes['TEXT_SIZE']))
		all_nouns_in_all_words.append(float(subdict_attributes['ALL_NOUNS_IN_ALL_WORDS']))
		pronouns_in_all_words.append(float(subdict_attributes['PRONOUNS_IN_ALL_WORDS']))
		regular_nouns_in_all_nouns.append(float(subdict_attributes['REGULAR_NOUNS_IN_ALL_NOUNS']))
		proper_nouns_in_all_nouns.append(float(subdict_attributes['PROPER_NOUNS_IN_ALL_NOUNS']))
		gnes_nouns_in_all_nouns.append(float(subdict_attributes['GNE_IN_ALL_NOUNS']))
		gnes_nouns_in_all_words.append(float(subdict_attributes['GNE_IN_ALL_WORDS']))

	## LINE GRAPHS
	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, all_nouns_in_all_words)
	plt.title("POS DATA: Text size and All Nouns in All Words")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], all_nouns_in_all_words[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/all_nouns_in_all_words.png')
	
	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, pronouns_in_all_words)
	plt.title("POS DATA: Text size and Pronouns in All Words")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], pronouns_in_all_words[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/pronouns_in_all_words.png')

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, regular_nouns_in_all_nouns)
	plt.title("POS DATA: Text size and Regular Nouns in All Nouns")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], regular_nouns_in_all_nouns[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/regular_nouns_in_all_nouns.png')

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, proper_nouns_in_all_nouns)
	plt.title("POS DATA: Text size and Pronouns in All Nouns")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], proper_nouns_in_all_nouns[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/proper_nouns_in_all_nouns.png')

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, proper_nouns_in_all_nouns)
	plt.title("POS DATA: Text size and GNES in All Nouns")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], gnes_nouns_in_all_nouns[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/gnes_in_all_nouns.png')

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ax.scatter(text_size, proper_nouns_in_all_nouns)
	plt.title("POS DATA: Text size and GNES in All Words")
	for i, data in enumerate(filenames): # label all dots with text file name
		ax.annotate(data, (text_size[i], gnes_nouns_in_all_words[i]), fontsize=5)
	plt.ylabel("Percentage")
	ax.set_ylim([0.0, 1.0])
	ax.set_xlim(left=0)
	plt.xlabel("File Text Size (words)")
	plt.savefig('plot_percent_data/gnes_in_all_words.png')
	
	#BOXPLOTS
	plt.title("POS DATA: Text size and All Nouns in All Words")
	plt.boxplot(all_nouns_in_all_words)
	plt.savefig('plot_percent_data/all_nouns_in_all_words_box.png')

	plt.title("POS DATA: Text size and Pronouns in All Words")
	plt.boxplot(pronouns_in_all_words)
	plt.savefig('plot_percent_data/pronouns_in_all_words_box.png')

	plt.title("POS DATA: Text size and Regular Nouns in All Nouns")
	plt.boxplot(regular_nouns_in_all_nouns)
	plt.savefig('plot_percent_data/regular_nouns_in_all_nouns_box.png')

	plt.title("POS DATA: Text size and Pronouns in All Nouns")
	plt.boxplot(proper_nouns_in_all_nouns)
	plt.savefig('plot_percent_data/proper_nouns_in_all_nouns_box.png')

	plt.title("POS DATA: Text size and GNES in All Nouns")
	plt.boxplot(gnes_nouns_in_all_nouns)
	plt.savefig('plot_percent_data/gnes_in_all_nouns_box.png')

	plt.title("POS DATA: Text size and GNES in All Words")
	plt.boxplot(gnes_nouns_in_all_words)
	plt.savefig('plot_percent_data/gnes_in_all_words_box.png')

	print("DATA PLOT POS UPDATED")

def plotPolarity(group_polarity, given_file):
	# plot polarity over text by groups (x)
	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	ordered_polarity = sorted(group_polarity.items(), key=lambda x:x[0])

	group_id_x = [x[0] for x in ordered_polarity]
	polarity_y = [x[1] for x in ordered_polarity]

	neg_pol =[]
	pos_pol = []
	for pol in polarity_y:
		if pol <= 0.0:
			neg_pol.append(pol)
			pos_pol.append(np.nan)
		else:
			neg_pol.append(np.nan)
			pos_pol.append(pol)
	
	avg_line = [(float(a)+float(b))/2 for a, b in zip(polarity_y[:], polarity_y[1:])]
	avg_line.append((float(polarity_y[-2])+float(polarity_y[-1]))/2)
	
	ax.scatter(group_id_x, pos_pol, color='red')
	ax.scatter(group_id_x, neg_pol, color='blue')
	ax.plot(group_id_x, avg_line, '--', color='black')
	plt.title("Polarity: {0}".format(given_file.upper()))
	plt.ylabel("Polarity")
	plt.xlabel("Group ID (Sentences)")
	ax.set_xlim(0, len(group_id_x))
	output_file = "{0}.png".format(given_file.upper())
	plt.savefig('sentiment_csv/{0}'.format(output_file))
	print("SENTIMENT PLOT {0} SAVED TO SENTIMENT_CSV".format(output_file))

def plotTagData():
	# plot data related to how long parsing and tagging takes
	time_data_results = {} # store old rows
	with open('plot_percent_data/timedTagging.csv', 'r') as timing_data:
		reader = csv.DictReader(timing_data)
		for row in reader:
			time_data_results[row['FILENAME']] = row # store previous rows
	text_size = []
	time_parsey = []
	time_manualTag = []
	for filename_given, sub_headers in time_data_results.iteritems():
		size_data = sub_headers['TEXT_SIZE']
		if size_data != '':
			text_size.append(size_data)
		else:
			text_size.append(np.nan)
		
		parse_data = sub_headers['PARSEY_TAGGING_TIME_SECONDS']
		if parse_data != '':
			time_parsey.append(parse_data)
		else:
			time_parsey.append(np.nan)
		
		tag_data = sub_headers['MANUAL_TAGGING_TIME_SECONDS']
		if tag_data != '':
			time_manualTag.append(tag_data)
		else:
			time_manualTag.append(np.nan)

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	plt.title("Runtime: Parsey McParseface")
	plt.ylabel("Time (Seconds)")
	plt.xlabel("Text Size (Words)")
	ax.set_xlim(left = 0)
	ax.scatter(text_size, time_parsey)
	plt.savefig('plot_percent_data/runtime_parsey_data.png')

	(fig, ax) = plt.subplots(1, 1, figsize=(16, 16))
	plt.title("Runtime: Manual Tagging")
	plt.ylabel("Time (Seconds)")
	plt.xlabel("Text Size (Words)")
	ax.set_xlim(left = 0)
	ax.scatter(text_size, time_manualTag)
	plt.savefig('plot_percent_data/runtime_manualTag_data.png')

	print("RUNTIME PLOTS UPDATED")
########################################################################
## Output pos into csv
def outputCSVconll(filename, dict_parts_speech, filednames):
	# save conll parser and pos to csv
	'''
	0 - ID (index in sentence), index starts at 1
	1 - FORM (exact word)
	2 - LEMMA (stem of word form)
	3 - UPOSTAG (universal pos tag)
	4 - XPOSTAG (Language-specific part-of-speech tag)
	5 - FEATS (List of morphological features)
	6 - HEAD (Head of the current token, which is either a value of ID or zero (0))
	7 - DEPREL (Universal Stanford dependency relation to the HEAD (root iff HEAD = 0))
	8 - DEPS (List of secondary dependencies)
	9 - MISC (other annotation)
	'''
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	output_filename = "pos_{0}.csv".format(given_file.upper())

	with open('csv_pos/{0}'.format(output_filename), 'w+') as pos_data:
		writer = csv.DictWriter(pos_data, fieldnames=fieldnames)
		writer.writeheader() 
		for i in range(len(dict_parts_speech)):
			sentence_pos_lst = dict_parts_speech[i][1]
			for pos in sentence_pos_lst:
				#print(pos, i)
				writer.writerow({'SENTENCE_INDEX': i, 
								'FORM': pos[1],
								'XPOSTAG': pos[4],
								'UPOSTAG': pos[3],
								'ID': pos[0],
								'SENTENCE_LENGTH': len(dict_parts_speech[i][0].split()),
								'LEMMA': pos[2],
								'FEATS': pos[5],
								'HEAD': pos[6],
								'DEPREL': pos[7],
								'DEPS':pos[8],
								'MISC': pos[9],
								'SENTENCE': dict_parts_speech[i][0],
								'IS_DIALOUGE': isDialogue(dict_parts_speech[i][0])
								})

	print("\nCSV POS output saved as {0}".format(output_filename))

########################################################################
## Parse Arguments, running main

if __name__ == '__main__':
	start_time = datetime.now()
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

	token_sentence_dict = tokenizeSentence(tokens_as_string)
	#for key, value in token_sentence_dict.iteritems():
	#	print("k={0} is quote = {1}".format(value, isDialogue(token_sentence_dict[key])))

	# check to see if file has already been saved in csv, otherwise run script
	given_file = os.path.basename(os.path.splitext(filename)[0]) # return only the filename and not the extension
	print("RUNNING PRE-PROCESSING FOR: {0}".format(given_file.upper()))
	output_filename = "pos_{0}.csv".format(given_file.upper())
	#print(output_filename)
	# create csv_pos and manual tagging directories if they do not exist

	# creating directories if they do not already exist
	if not os.path.isdir('csv_pos'):
		print("creating csv_pos directory")
		os.makedirs('csv_pos')
	if not os.path.isdir('manual_tagging'):
		print("creating manual_tagging directory")
		os.makedirs('manual_tagging')
	if not os.path.isdir('plot_percent_data'):
		print("creating plot_percent_data directory")
		os.makedirs('plot_percent_data')
	if not os.path.isdir('sentiment_csv'):
		print("creating sentiment_csv directory")
		os.makedirs('sentiment_csv')

	csv_local_dir = "{0}/csv_pos/{1}".format(os.getcwd(), output_filename)

	fieldnames = ['SENTENCE_INDEX',
				'FORM',
				'XPOSTAG',
				'UPOSTAG',
				'ID',
				'SENTENCE_LENGTH',
				'LEMMA',
				'FEATS',
				'HEAD',
				'DEPREL',
				'DEPS',
				'MISC',
				'SENTENCE',
				'IS_DIALOUGE'
				]

	# if file has been modified more recently than the associated csv
	file_has_been_modified_recently = False
	if os.path.isfile(csv_local_dir): # if file exists, then check if modified
		file_has_been_modified_recently = os.path.getmtime("{0}/{1}".format(os.getcwd(), filename)) > os.path.getmtime(csv_local_dir)
		#print("file has been modifed = {0}".format(file_has_been_modified_recently))
	# if file does not exist in the csv folder
	if not os.path.isfile(csv_local_dir) or file_has_been_modified_recently: 
		#print("pos needs to be calculated...")
		dict_parts_speech = partsOfSpeech(token_sentence_dict)
		outputCSVconll(filename, dict_parts_speech, fieldnames)

	# create named tuple from csv row
	PosCSV = namedtuple('PosCSV', fieldnames)
	pos_dict = {}
	total_words = 0
	with open(csv_local_dir, "rb") as csv_file:
		csvreader = csv.reader(csv_file)
		next(csvreader) # skip header
		id_count = 0
		for line in csvreader:
			pos_named_tuple = PosCSV._make(line)
			pos_dict[id_count] = pos_named_tuple
			id_count += 1
			if pos_named_tuple.MISC != 'punct' and pos_named_tuple.XPOSTAG != 'POS': # if row isn't puntuation or 's
				total_words += 1
	# index proper nouns
	grouped_named_ent_lst = findProperNamedEntity(pos_dict) # return a list of tuples with elements in order for nnp
	#print("Characters in the text : {0}\n".format(grouped_named_ent_lst))
	#print("Characters in the text (set): {0}\n".format(list(set(x for l in grouped_named_ent_lst.values() for x in l))))
	character_entities_group = groupSimilarEntities(grouped_named_ent_lst)
	#print("Characters in the text (ent): {0}".format(character_entities_group))
	sub_dictionary_one_shot_lookup = lookupSubDictionary(character_entities_group)
	#print("dictionary for one degree of nouns: {0}".format(sub_dictionary_one_shot_lookup))

	global_ent_dict = mostCommonGNE(sub_dictionary_one_shot_lookup)

	# index pronouns
	pronoun_index_dict = findPronouns(pos_dict)
	#print("\n\npronoun index dictionary: {0}".format(pronoun_index_dict))

	# print/display graphs with pos data
	percent_ratio_dict = percentagePos(total_words, pos_dict) # print percentage of nouns/pronouns
	csv_data = saveDatatoCSV(filename, percent_ratio_dict)
	time_data_csv = "plot_percent_data/timedTagging.csv"
	time_plot_data = "plot_percent_data/runtime_parsey_data.png"
	if os.path.getmtime(time_data_csv) > os.path.getmtime(time_plot_data): 
		# checks if csv has been updated more recently than the plot data
		plotTagData()

	# gne hierarchy of names
	over_correct_for_multiple_title = False # a potential option if the text includes lots of titles
	gne_tree = gneHierarchy(character_entities_group[0], over_correct_for_multiple_title)
	loaded_gender_model = loadDTModel() # load model once, then use to predict
	gender_gne = determineGenderName(loaded_gender_model, gne_tree)

	# SET UP FOR MANUAL TESTING (coreference labels calls csv to be tagged by hand for accuracy)
	manual_tag_dir = "manual_tagging/manualTagging_{0}.csv".format(os.path.basename(os.path.splitext(filename)[0]).upper())
	if not os.path.isfile(manual_tag_dir) or file_has_been_modified_recently: # checks csv again to see if it has been updated
		coreferenceLabels(filename, pos_dict, sub_dictionary_one_shot_lookup, global_ent_dict, pronoun_index_dict)

	#for key, value in gne_tree.iteritems():
	#	print("\ngne base name: {0} is {1}\n{2}".format(key, gender_gne[key], value))
	
	# TODO: set up gender trees
	# TODO: visual gender name database classifier
	# TODO: move all imports to top
	# TODO: fix pos data for gnes to run for each row rather than the last text
	# TODO: set up a network with relationships with polarity over time

	# create a dictionary from the manual taggins _p and _n for the value and the index
	noun_pronoun_dict, line_by_line_dict = breakTextPandN(manual_tag_dir, gender_gne, loaded_gender_model)
	
	updated_csv_data = graphGNEvText(csv_data, percent_ratio_dict, noun_pronoun_dict)
	graphPOSdata(updated_csv_data) # graph data

	# identify the characters of interest and condense the trees
	characters_with_sub_names = identifyCharacterOfInterest(noun_pronoun_dict, gne_tree, gender_gne, print_info=True)

	# find and graph all interactions
	# (group_id) : polarity
	group_polarity = interactionsPolarity(characters_with_sub_names, line_by_line_dict, filename)
	plotPolarity(group_polarity, given_file)
	
	#'''
	# GENERATE NETWORKX
	# generate a tree for gne names
	# {Dr Urbino: {'Dr': ['Dr', 'Dr Juvenal Urbino', 'Dr Urbino'], 'Urbino': ['Urbino']} }
	# {Mr Frank Churchill {'Frank': ['Frank', 'Frank Churchill'], 'Churchill': ['Churchill', 'Churchill of Enscombe'], 'Mr': ['Mr', 'Mr Churchill', 'Mr Frank Churchill']}}
	# {Miss Harriet Smith {'Smith': ['Smith'], 'Harriet': ['Harriet', 'Harriet Smith'], 'Miss': ['Miss', 'Miss Harriet Smith', 'Miss Smith']} }

	#generateGNEtree(gne_tree, filename)
	# generate network graphs
	#networkGraphs(gne_tree)

	print("\nPre-processing ran for {0}".format(datetime.now() - start_time))

########################################################################
## TODO: 
	# TODO: find possesive 'you've' and 'my'
	# TODO: check CAPTALIZED WORDS as their lower case counterparts before saving
