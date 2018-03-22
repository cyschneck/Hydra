###########################################################################
# Gender classifier and predictor

# Date: January 2017
###########################################################################
import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib # save model to load
###########################################################################

TRAINING_PERCENT = 0.6 #60%
FEATURE_TAGS = ['first_letter', 
				'first_2_letters',
				'first_half',
				'last_half',
				'last_2_letters',
				'last_letter',
				 'length_of_name']
#print(FEATURE_TAGS)

def DT_features(given_name):
	#test_given_name = ['corette', 'corey', 'cori', 'corinne', 'william', 'mason', 'jacob', 'zorro'] #small test
	features_list = []
	name_features = [given_name[0], given_name[:2], given_name[:len(given_name)/2], given_name[len(given_name)/2:], given_name[-2:], given_name[-1:], len(given_name)]
	#[['z', 'zo', 'zo', 'rro', 'ro', 'o', 5], ['z', 'zo', 'zo', 'rro', 'ro', 'o', 5]]
	features_list = dict(zip(FEATURE_TAGS, name_features))
	return features_list

def determine_gender(name_list, loaded_pipeline):
	#return male/female for a given name
	for name in name_list:
		prob_gender = loaded_pipeline.predict_proba(dt([name]))[0]
		gender_is = 'Male' if prob_gender[1] > prob_gender[0] else 'Female'
		print("The name '{0}' is most likely {1}".format(name, gender_is))
		#print(loaded_pipeline.decision_path(DT_features([name])))
		print("Odds: Female ({0}), Male ({1})\n".format(prob_gender[0], prob_gender[1]))
	#return pipeline.predict(DT_features(name))#[0]

if __name__ == '__main__':
	start_time = datetime.now()

	gender_names_data = pd.read_csv('names_gender.csv')
	gender_names_data = gender_names_data.as_matrix()[1:, :]
	print("Size of training set: {0}".format(len(gender_names_data)))

	gender_y = gender_names_data[:, 1]
	dt = np.vectorize(DT_features) #vectorize dt_features function
	names_x = dt(gender_names_data[:, 0]) # generate new list/list array with additional features
	
	#shuffle to create train/test data
	from sklearn.utils import shuffle
	names_x, gender_y = shuffle(names_x, gender_y)

	x_train = names_x[:int(TRAINING_PERCENT * len(names_x))]
	x_test = names_x[int(TRAINING_PERCENT * len(names_x)):]
	y_train = gender_y[:int(TRAINING_PERCENT * len(gender_y))]
	y_test = gender_y[int(TRAINING_PERCENT * len(gender_y)):]

	#classifier
	vectorizer = DictVectorizer()
	dtc = DecisionTreeClassifier(min_samples_leaf=25)
	#global pipeline
	pipeline = Pipeline([('dict', vectorizer), ('dtc', dtc)])
	
	pipeline = pipeline.fit(x_train, y_train) # training

	#Accuracy
	current_saved_model_file = [f for f in os.listdir('.') if 'gender_saved_model' in f][0]
	print("CURRENT FILE: {0}".format(current_saved_model_file))
	current_acc = current_saved_model_file.split('.')[-2]#.split('_')
	current_acc = '0.{0}'.format(current_acc)
	print("CURRENT ACCURACY = {0}".format(current_acc))
	
	print("Accuracy on training: {0}".format(pipeline.score(x_train, y_train)))
	print("Accuracy on testing: {0}".format(pipeline.score(x_test, y_test)))
	if pipeline.score(x_test, y_test) > float(current_acc):
		for old_model in [f for f in os.listdir('.') if 'gender_saved_model' in f]:
			#print(old_model)
			if old_model.endswith(".pkl"):
				os.remove(old_model)
		import pickle
		with open('pipeline_gender_saved_model_{0}.pkl'.format(pipeline.score(x_test, y_test)), 'wb') as model_file:
			pickle.dump(pipeline, model_file)
		print("MODEL INCREASED ACCURACY, SAVED")
	else:
		print("NO CHANGE IN ACCURACY, NOT SAVED")

	updated_saved_model = [f for f in os.listdir('.') if 'pipeline_gender_saved_model' in f][0]
	print("RUNNING MODEL: {0}".format(updated_saved_model))

	pipeline_loaded = joblib.load(updated_saved_model)
	print("\n")
	
	#testing on novel names
	#test_name = ["Nemo"]
	test_name = ["Atticus", "Shevek", "Emma", "Ishamel", "Ldfafadoreli", 'Tars Tarkas', "Dejah", "Mary"]
	determine_gender(test_name, pipeline_loaded)
	print("ran for for {0}\n".format(datetime.now() - start_time))
