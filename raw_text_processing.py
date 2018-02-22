# -*- coding: utf-8 -*-

###########################################################################
# Pre-processing raw text

# Date: November 2017
###########################################################################
import os
import re
import nltk # Natural Language toolkit
from nltk.tokenize import sent_tokenize, word_tokenize # form tokens from words/sentences
import string
import csv
from datetime import datetime
from collections import namedtuple, Counter
from itertools import imap # set up namedtuple
from collections import defaultdict # create dictionary with empty list for values

########################################################################
## READING AND TOKENIZATION OF RAW TEXT (PRE-PROCESSING)

basic_pronouns = "I Me You She He Him It We Us They Them Myself Yourself Himself Herself Itself Themselves My your Her Its Our Their His"
possessive_pronouns = "mine yours his hers ours theirs"
reflexive_pronouns = "myself yourself himself herself itself oneself ourselves yourselves themselves"
relative_pronouns = "that whic who whose whom where when"


def readFile(filename):
	file_remove_extra = []
	with open(filename, "r") as given_file:
		string_words = given_file.read()
		string_words = string_words.replace("\n", " ")
		string_words = string_words.replace(";" , " ")
		string_words = string_words.replace("--", " ")
		string_words = string_words.replace("_", "")
		string_words = string_words.replace("Mr.", "Mr") # period created breaks when spliting
		string_words = string_words.replace("Ms.", "Ms")
		string_words = string_words.replace("Mrs.", "Mrs")
		string_words = string_words.replace("Dr.", "Dr")
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

def findProperNamedEntity(pos_dict):
	# returns {sentence index: [list of all proper nouns grouped]
	# {0: ["Scarlett O'Hara", 'Tarleton'], 1: ['Coast']}
	pos_type_lst = []
	# TODO: EXPAND PROPER NOUNS FOR COMMON WORDS AROUND WORD
	for row, pos_named in pos_dict.iteritems():
		if "NNP" in pos_named.XPOSTAG: #"NN" in pos_named.XPOSTAG or "POS" in pos_named.XPOSTAG or "IN" in pos_named.XPOSTAG or "DT" in pos_named.XPOSTAG:
			pos_type_lst.append((int(pos_named.SENTENCE_INDEX), int(pos_named.ID), pos_named.FORM, int(pos_named.SENTENCE_LENGTH), pos_named.XPOSTAG))
	#print(pos_type_lst)

	total_sentence_indices = list(set([i[0] for i in pos_type_lst]))
	#print(total_sentence_indices)
	sub_sentences = []
	for index in total_sentence_indices:
		# create sub sentences for each sentence [[0], [1])
		sub_sentences.append([x for x in pos_type_lst if x[0] == index])

	from operator import itemgetter # find sequences of consecutive values
	import itertools

	grouped_nouns = {}
	names_lst = []
	sentence_index = []
	for sentence in sub_sentences:
		noun_index = [s_index[1] for s_index in sentence]
		consec_lst = []
		for k, g in itertools.groupby(enumerate(noun_index), lambda x: x[1]-x[0]):
			consec_order = list(map(itemgetter(1), g))
			if len(consec_order) > 0: # if there is more than one noun in an order for a sentence
				consec_lst.append(consec_order)
		#consec_lst = [item for items in consec_lst for item in items]
		for c_l in consec_lst:
			#grouped_nouns.append([x[:3] for x in sentence if x[1] in c_l])
			g_name = [x for x in sentence if x[1] in c_l]
			nnp_in_sentence = False
			for i, v in enumerate(g_name):
				nnp_in_sentence = "NNP" in v
				if nnp_in_sentence: # if the nnp exist in the sub-list, exit and save
					break
			if nnp_in_sentence:
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
	counter_dict = dict(Counter([val for sublist in grouped_nouns_dict.values() for val in sublist]))
	print(grouped_nouns_dict)
	#print(counter_dict)
	print("\n")
	
	names_all = list(set([val for sublist in grouped_nouns_dict.values() for val in sublist])) # is a list of all unquie names in the list
	compare_names_same_format = [val.upper() for val in names_all]
	# loop through to group similar elements
	print(names_all)
	print("\n")
	print(compare_names_same_format)
	print("\n")
	gne_list_of_lists = grouped_nouns_dict.values()
	gne_list_of_lists = list(set([item for sublist in gne_list_of_lists for item in sublist])) # creates a list of unquie names
	print(gne_list_of_lists)
	print("\n")

	import difflib 
	from difflib import SequenceMatcher
	gne_name_group = []
	# find most similar ['Professor', 'Professor Aronnax'], ['Aronnax', 'Mr Aronnax', 'Pierre Aronnax']
	for gne in gne_list_of_lists:
		for g in gne.split():
			compared = difflib.get_close_matches(g, gne_list_of_lists)
			if compared != []:
				gne_name_group.append(compared)
	print(gne_name_group)
	#gne_name_group = list(set(gne_name_group))

	#final_grouping = []
	#for row in gne_name_group:
	#	for i, resrow in enumerate(final_grouping):
	#		if row[0]==resrow[0]:
	#			final_grouping[i] += row[1:]
	#			break
	#	else:
	#		final_grouping.append(row)
	#print(final_grouping)
	final_grouping = []
	words_to_ignore = ["Mr", "Mrs", "Ms"]
	
	for gne in gne_list_of_lists:
		sublist = []
		for i in gne.split():
			for gne_2 in gne_list_of_lists:
				print(i, gne_2)
				if i in gne_2:
					if i != gne_2:
						if i != [] or gne_2 != []:
							if len(i) > 1 and i not in words_to_ignore:
								sublist.append([i, gne_2])
		final_grouping.append(sublist)
	final_grouping = [x for x in final_grouping if x != []]
	print("\nfinalgrouping")
	for i in final_grouping:
		print(i)
	#print(final_grouping)



########################################################################
# data anaylsis
def percentagePos(total_words, csv_dict):
	# prints the percentage of the text that is pronouns vs. nouns
	pronouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("PRP")
	pronoun_percentage = float(pronouns_count)/float(total_words)
	print("percent pronouns = {0:.3f}% of all text".format(pronoun_percentage*100.0))

	proper_nouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNP") # proper noun singular
	proper_nouns_count += [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNPS") # proper noun plural: spaniards
	print("percent proper nouns = {0:.3f}% of all text".format((float(proper_nouns_count)/float(total_words))*100))

	nouns_count = [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NN") # nouns: ship, language
	nouns_count += [pos.XPOSTAG for _, pos in csv_dict.iteritems()].count("NNS") # plurla noun: limbs
	print("percent nouns = {0:.3f}% of all text".format((float(nouns_count)/float(total_words))*100))

	nouns_ratio= [pos.UPOSTAG for _, pos in csv_dict.iteritems()].count("NOUN")
	print("proper nouns make up {0:.3f}% of all nouns".format((float(proper_nouns_count)/float(nouns_ratio))*100))
	print("regular nouns make up {0:.3f}% of all nouns".format((float(nouns_count)/float(nouns_ratio))*100))

	#verbs_count = [pos.UPOSTAG for _, pos in csv_dict.iteritems()].count("VERB")
	#print("percent verbs = {0:.3f}%".format((float(nouns_count)/float(total_words))*100))

	#print(set([pos.XPOSTAG for _, pos in csv_dict.iteritems()])) # unquie tags
	noun_tags = []
	for row_num, pos in csv_dict.iteritems():
		if pos.UPOSTAG == "NOUN":
			noun_tags.append(pos.XPOSTAG)
	#print(set(noun_tags))


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
	output_filename = "pos_{0}.csv".format(given_file.upper())
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

	grouped_named_ent_lst = findProperNamedEntity(pos_dict) # return a list of tuples with elements in order for nnp
	print("Characters in the text: {0}\n".format(list(set(x for l in grouped_named_ent_lst.values() for x in l))))
	#grouped_named_ent_lst = commonSurrouding(grouped_named_ent_lst) # updated
	shared_ent = groupSimilarEntities(grouped_named_ent_lst)
	#print(shared_ent)
	

	#percentagePos(total_words, pos_dict) # print percentage of nouns/pronouns

	# TODO: debug dialouge for "words" said person "words again"
	# TODO: use percentagePos to generate normalized graphs for size of text vs. # of nouns/pronouns

	#TODO Next: import local file to predict male/female (he/she) with a given list of names
	#x number of sentences around to find proper noun
	#from sklearn.externals import joblib # save model to load
	#loaded_gender_model = joblib.load('name_preprocessing/gender_saved_model_0.853992787223.sav')
	#test_name = ["Nemo"]
	#print(loaded_gender_model.score(test_name))
	#run gender tag once on the entire text, tag male/female and use for predictions
	# TODO: predict gender with probailities to allow for abiguity

	print("\nPre-processing ran for {0}".format(datetime.now() - start_time))
