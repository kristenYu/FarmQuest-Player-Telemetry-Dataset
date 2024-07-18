import processing_util
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats

def clean_actions_to_type(session_keys, session_num, data):
	cleaned_data = []
	for key in session_keys:
		telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		action_type = []
		for t in telemetry[f"session_{session_num}"]:
			if "Transition:Main" in t: 
				action_type.append("Transition:Main")
			if "Transition:Home" in t:
				action_type.append("Transition:Home")
			if "Transition:QuestBoard" in t:
				action_type.append("Transition:QuestBoard")
			if "Transition:Shop" in t: 
				action_type.append("Transition:Shop")
			if "Interaction:Plant" in t: 
				action_type.append("Plant")
			if "HarvestCrop" in t: 
				action_type.append("HarvestCrop")
			if "Interaction:HarvestMushroom" in t: 
				action_type.append("Harvest")
			if "Interaction:HarvestBerry" in t:
				action_type.append("Harvest")
			if "Interaction:Place" in t: 
				action_type.append("Place")
			if "Interaction:Rotate" in t: 
				action_type.append("Rotate")
			if "Interaction:Pickup" in t:
				action_type.append("Pickup")
			if "Interaction:Cook" in t: 
				action_type.append("Cook")
			if "Shop:Bought" in t:
				action_type.append("Shop:Bought")
			if "Sold" in t:
				action_type.append("Shop:Sold")
			if "Pay" in t:
				action_type.append("Shop:Pay")
			if "Quest:Accept" in t: 
				action_type.append("Quest:Accept")
			if "Quest:Submit" in t: 
				action_type.append("Quest:Submit")
		cleaned_data.append(action_type)
	return cleaned_data

def get_predicted_next_action(ngram_frequency, input_action):
	following_actions = ngram_frequency[input_action]
	total_actions = 0
	for following_action in following_actions:
		total_actions += ngram_frequency[input_action][following_action]
	highest_prob = 0 
	best_action = ""
	for following_action in following_actions:
		prob_next_action = ngram_frequency[input_action][following_action]/total_actions
		if prob_next_action > highest_prob: 
			best_action = following_action
			highest_prob = prob_next_action
	return (best_action, highest_prob)

def count_actions(action_data):
	counted_actions = {}
	for player_action_data in action_data:
		for action in player_action_data:
			if action in counted_actions.keys():
				counted_actions[action] += 1
			else: 
				counted_actions[action] = 1
	return counted_actions

def graph_action_histogram(counted_actions, name):
	counted_actions = dict(sorted(counted_actions.items()))
	br1 = np.arange(len(counted_actions))
	fig = plt.subplots(figsize=(12,8))
	plt.bar(br1, counted_actions.values(), align='center')
	plt.xlabel("Actions", fontsize=25)
	plt.xticks(range(len(counted_actions)), counted_actions.keys(), rotation=60, fontsize=20, ha='right')
	plt.ylabel("Frequency", fontsize=25)
	plt.yticks(fontsize=20)
	plt.title(f"{name} Action Histogram", fontsize=25)

	plt.savefig(f"ngram/{name}_action_histogram.pdf", bbox_inches='tight')


processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);
print("number of participants " + str(len(data)))

valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys = processing_util.get_valid_keys(data)
print(len(valid_keys))

session_1_cleaned_action_data = clean_actions_to_type(valid_keys, 1, data)
session_2_cleaned_action_data = clean_actions_to_type(valid_keys, 2, data)
cleaned_action_data = session_1_cleaned_action_data + session_2_cleaned_action_data

#plot histogram of actions
counted_actions = count_actions(cleaned_action_data)
graph_action_histogram(counted_actions, "total")

session_1_passage_cleaned_action_data = clean_actions_to_type(session_1_passage, 1, data)
session_2_passage_cleaned_action_data = clean_actions_to_type(session_2_passage, 2, data)
passage_cleaned_action_data = session_1_passage_cleaned_action_data + session_2_passage_cleaned_action_data


passage_counted_actions = count_actions(passage_cleaned_action_data)
graph_action_histogram(passage_counted_actions, "passage")

session_1_RLAID_cleaned_action_data = clean_actions_to_type(session_1_RLAID, 1, data)
session_2_RLAID_cleaned_action_data = clean_actions_to_type(session_2_RLAID, 2, data)
RLAID_cleaned_action_data = session_1_RLAID_cleaned_action_data + session_2_RLAID_cleaned_action_data

RLAID_counted_actions = count_actions(RLAID_cleaned_action_data)
graph_action_histogram(RLAID_counted_actions, "RLAID")

session_1_random_cleaned_action_data = clean_actions_to_type(session_1_random, 1, data)
session_2_random_cleaned_action_data = clean_actions_to_type(session_2_random, 2, data)
random_cleaned_action_data = session_1_random_cleaned_action_data + session_2_random_cleaned_action_data

random_counted_actions = count_actions(random_cleaned_action_data)
graph_action_histogram(random_counted_actions, "random")

print("passage vs RLAID, " + str(scipy.stats.mannwhitneyu(list(passage_counted_actions.values()), list(RLAID_counted_actions.values()))))
print("random vs RLAID, " + str(scipy.stats.mannwhitneyu(list(random_counted_actions.values()), list(RLAID_counted_actions.values()))))
print("passage vs random, " + str(scipy.stats.mannwhitneyu(list(passage_counted_actions.values()), list(random_counted_actions.values()))))


#Next action prediction
unigram_frequency = {}
for action_data in cleaned_action_data:
	for i in range(0, len(action_data)-1):
		if action_data[i] in unigram_frequency.keys():
			if action_data[i+1] in unigram_frequency[action_data[i]].keys():
				unigram_frequency[action_data[i]][action_data[i+1]] += 1
			else:
				unigram_frequency[action_data[i]][action_data[i+1]] = 1
		else: 
			unigram_frequency[action_data[i]] = {action_data[i+1]: 1}

bigram_frequency = {}
for action_data in cleaned_action_data:
	for i in range(0, len(action_data)-2): 
		bigram = action_data[i] + ";" + action_data[i+1]
		if bigram in bigram_frequency.keys():
			if action_data[i+2] in bigram_frequency[bigram].keys():
				bigram_frequency[bigram][action_data[i+2]] += 1
			else:
				bigram_frequency[bigram][action_data[i+2]] = 1
		else:
			bigram_frequency[bigram] = {action_data[i+2]: 1}

trigram_frequency = {}
for action_data in cleaned_action_data: 
	for i in range(0, len(action_data)-3):
		trigram = action_data[i] + ";" + action_data[i+1] + ";" + action_data[i+2]
		if trigram in trigram_frequency.keys():
			if action_data[i+3] in trigram_frequency[trigram].keys():
				trigram_frequency[trigram][action_data[i+3]] += 1
			else:
				trigram_frequency[trigram][action_data[i+3]] = 1
		else:
			trigram_frequency[trigram] = {action_data[i+3]: 1}

#pick 5 random trigrams from the frequency table to generate test data: 
test_actions = []
for i in range(0,5):
	test_actions.append(random.choice(list(trigram_frequency.keys())))


for test_action in test_actions: 
	trigram = test_action
	unigram = test_action.split(";")[-1]
	bigram = test_action.split(";")[-2] + ";" + test_action.split(";")[-1]
	trigram_best_action, trigram_highest_prob = get_predicted_next_action(trigram_frequency, trigram)
	bigram_best_action, bigram_highest_prob = get_predicted_next_action(bigram_frequency, bigram)
	unigram_best_action, unigram_highest_prob = get_predicted_next_action(unigram_frequency, unigram)
	print("Trigram current action: " + str(trigram) + " predicted next action: " + str(trigram_best_action) + " with probability " + str(trigram_highest_prob))
	print("bigram current action: " + str(bigram) + " predicted next action: " + str(bigram_best_action) + " with probability " + str(bigram_highest_prob))
	print("Unigram current action: " + str(unigram) + " predicted next action: " + str(unigram_best_action) + " with probability " + str(unigram_highest_prob))



