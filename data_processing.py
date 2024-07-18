import processing_util
import statistics as statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
import scipy
import csv

def process_demographic_survey(survey_data):
	demographic_structure_dictonary = {"demographic_survey": 0, "current_age": 1, "gender": 2, "cisortrans": 3, "gamer":4, "weeklygames":5, "game_genres":6}
	demographic_survey = {}
	split_data = survey_data.split("\n")
	demographic_survey["current_age"] = split_data[demographic_structure_dictonary["current_age"]].split(":")[-1]
	demographic_survey["gender"] = split_data[demographic_structure_dictonary["gender"]].split(":")[-1]
	demographic_survey["cisortrans"] = split_data[demographic_structure_dictonary["cisortrans"]].split(":")[-1]
	demographic_survey["gamer"] = split_data[demographic_structure_dictonary["gamer"]].split(":")[-1]
	demographic_survey["weeklygames"] = split_data[demographic_structure_dictonary["weeklygames"]].split(":")[-1]
	demographic_survey["game_genres"] = split_data[demographic_structure_dictonary["game_genres"]].split(":")[-1]
	return demographic_survey
	
def get_demograhic_survey_data_accross_keys(valid_keys):
	aggregate_demographic_data = {}
	current_age = {}
	gender = {}
	cisortrans = {}
	gamer = {}
	weeklygames = {}
	game_genres = {}
	counter = 0
	for key in valid_keys:
		counter += 1
		demographic_data = process_demographic_survey(data[key]["demographic_data"])
		if(demographic_data["current_age"] in current_age.keys()):
			current_age[demographic_data["current_age"]] += 1
		else:
			current_age[demographic_data["current_age"]] = 1
		if(demographic_data["gender"] in gender.keys()):
			gender[demographic_data["gender"]] += 1
		else:
			gender[demographic_data["gender"]] = 1
		if(demographic_data["cisortrans"] in cisortrans.keys()):
			cisortrans[demographic_data["cisortrans"]] += 1
		else:
			cisortrans[demographic_data["cisortrans"]] = 1
		if(demographic_data["gamer"] in gamer.keys()):
			gamer[demographic_data["gamer"]] += 1
		else:
			gamer[demographic_data["gamer"]] = 1
		if(demographic_data["weeklygames"] in weeklygames.keys()):
			weeklygames[demographic_data["weeklygames"]] += 1
		else:
			weeklygames[demographic_data["weeklygames"]] = 1
		genre_data = demographic_data["game_genres"].split(",");
		for genre in genre_data:
			if(genre in game_genres.keys()):
				game_genres[genre] += 1
			else:
				game_genres[genre] = 1

	aggregate_demographic_data["current_age"] = current_age
	aggregate_demographic_data["gender"] = gender
	aggregate_demographic_data["cisortrans"] = cisortrans
	aggregate_demographic_data["gamer"] = gamer
	aggregate_demographic_data["weeklygames"] = weeklygames
	aggregate_demographic_data["game_genres"] = game_genres
	return aggregate_demographic_data


#short survey processing

def get_short_survey_data_accross_keys(session_1_keys, session_2_keys):
	session_data = {}
	session_1_pos_accept = []
	session_1_neg_accept = []
	session_1_pos_complete = []
	session_1_neg_complete = []
	session_1_variety = []
	session_1_pos_enjoy = []
	session_1_neg_enjoy = []
	session_1_pos_recommend = []
	session_1_neg_recommend = []

	session_2_pos_accept = []
	session_2_neg_accept = []
	session_2_pos_complete = []
	session_2_neg_complete = []
	session_2_variety = []
	session_2_pos_enjoy = []
	session_2_neg_enjoy = []
	session_2_pos_recommend = []
	session_2_neg_recommend = []

	for key in session_1_keys:
		survey_1_data = processing_util.process_short_survey(data[key]["short_survey_1_data"])
		if(survey_1_data["pos_accept"] != -1):
			session_1_pos_accept.append(survey_1_data["pos_accept"])
		session_1_neg_accept.append(survey_1_data["neg_accept"])
		session_1_pos_complete.append(survey_1_data["pos_complete"])
		session_1_neg_complete.append(survey_1_data["neg_complete"])
		if(survey_1_data["variety"] != -1):
			session_1_variety.append(survey_1_data["variety"])
		session_1_pos_enjoy.append(survey_1_data["pos_enjoy"])
		session_1_neg_enjoy.append(survey_1_data["neg_enjoy"])
		session_1_pos_recommend.append(survey_1_data["pos_recommend"])
		session_1_neg_recommend.append(survey_1_data["neg_recommend"])


	for key in session_2_keys:
		survey_2_data = processing_util.process_short_survey(data[key]["short_survey_2_data"])
		if(survey_2_data["pos_accept"] != -1):
			session_2_pos_accept.append(survey_2_data["pos_accept"])
		session_2_neg_accept.append(survey_2_data["neg_accept"])
		session_2_pos_complete.append(survey_2_data["pos_complete"])
		session_2_neg_complete.append(survey_2_data["neg_complete"])
		if(survey_2_data["variety"] != -1):
			session_2_variety.append(survey_2_data["variety"])
		session_2_pos_enjoy.append(survey_2_data["pos_enjoy"])
		session_2_neg_enjoy.append(survey_2_data["neg_enjoy"])
		session_2_pos_recommend.append(survey_2_data["pos_recommend"])
		session_2_neg_recommend.append(survey_2_data["neg_recommend"])

	session_data["pos_accept"] = session_1_pos_accept + session_2_pos_accept
	session_data["neg_accept"] = session_1_neg_accept + session_2_neg_accept
	session_data["pos_complete"] = session_1_pos_complete + session_2_pos_complete
	session_data["neg_complete"] = session_1_neg_complete + session_2_neg_complete
	session_data["variety"] = session_1_variety + session_2_variety
	session_data["pos_enjoy"] = session_1_pos_enjoy + session_2_pos_enjoy
	session_data["neg_enjoy"] = session_1_neg_enjoy + session_2_neg_enjoy
	session_data["pos_recommend"] = session_1_pos_recommend + session_2_pos_recommend
	session_data["neg_recommend"] = session_1_neg_recommend + session_2_neg_recommend

	return session_data

def process_comparison_survey(survey_data):
	comparison_survey_structure = {"comparison_survey": 0, "first_experience": 1, "second_experience": 2, "first_complete": 3, "second_complete": 4, "first_fun": 5, "second_fun": 6, "fav_activity": 7, "difference": 8}
	comparison_survey = {}
	split_data = survey_data.split('\n')
	if(split_data[comparison_survey_structure["first_experience"]].split(":")[-1] == ''):
		comparison_survey["first_experience"] = -1
	else:
		comparison_survey["first_experience"] = int(split_data[comparison_survey_structure["first_experience"]].split(":")[-1])

	if(split_data[comparison_survey_structure["second_experience"]].split(":")[-1] == ''):
		comparison_survey["second_experience"] = -1
	else:
		comparison_survey["second_experience"] = int(split_data[comparison_survey_structure["second_experience"]].split(":")[-1])

	if(split_data[comparison_survey_structure["first_complete"]].split(":")[-1] == ''):
		comparison_survey["first_complete"] = -1
	else:
		comparison_survey["first_complete"] = int(split_data[comparison_survey_structure["first_complete"]].split(":")[-1])

	if(split_data[comparison_survey_structure["second_complete"]].split(":")[-1] == ''):
		comparison_survey["second_complete"] = -1
	else:
		comparison_survey["second_complete"] = int(split_data[comparison_survey_structure["second_complete"]].split(":")[-1])
	
	if(split_data[comparison_survey_structure["first_fun"]].split(":")[-1] == ''):
		comparison_survey["first_fun"] = -1
	else:
		comparison_survey["first_fun"] = int(split_data[comparison_survey_structure["first_fun"]].split(":")[-1])

	if(split_data[comparison_survey_structure["second_fun"]].split(":")[-1] == ''):
		comparison_survey["second_fun"] = -1
	else:
		comparison_survey["second_fun"] = int(split_data[comparison_survey_structure["second_fun"]].split(":")[-1])
	#short answer questions
	comparison_survey["fav_activity"] = split_data[comparison_survey_structure["fav_activity"]].split(":")[-1]
	comparison_survey["difference"] = split_data[comparison_survey_structure["difference"]].split(":")[-1]

	return comparison_survey

def get_comparison_survey_accross_keys(keys):
	comparison_data = {}
	first_experience = []
	second_experience = []
	first_complete = []
	second_complete = []
	first_fun = []
	second_fun = []
	fav_activity = []
	difference = []
	for key in keys: 
		comparison_survey = process_comparison_survey(data[key]["comparison_data"])
		if(comparison_survey["first_experience"] != -1):
			first_experience.append(comparison_survey["first_experience"])
		if(comparison_survey["second_experience"] != -1):
			second_experience.append(comparison_survey["second_experience"])
		if(comparison_survey["first_complete"] != -1):
			first_complete.append(comparison_survey["first_complete"])
		if(comparison_survey["second_complete"] != -1):
			second_complete.append(comparison_survey["second_complete"])
		if(comparison_survey["first_fun"] != -1):
			first_fun.append(comparison_survey["first_fun"])
		if(comparison_survey["second_fun"] != -1):
			second_fun.append(comparison_survey["second_fun"])
		fav_activity.append(comparison_survey["fav_activity"])
		difference.append(comparison_survey["difference"])
	
	comparison_data["first_experience"] = first_experience
	comparison_data["second_experience"] = second_experience
	comparison_data["first_complete"] = first_complete
	comparison_data["second_complete"] = second_complete
	comparison_data["first_fun"] = first_fun
	comparison_data["second_fun"] = second_fun
	comparison_data["fav_activity"] = fav_activity
	comparison_data["difference"] = difference
	return comparison_data


def split_telemetry_into_session(telemetry):
	session_telemetry = {}
	event_start_index = 0
	session_locations = []
	complete_telemetry = []
	for t in telemetry:
		complete_telemetry.append(t)
		event_start_index += 1
		if "SessionStart" in t:
			session_locations.append(event_start_index-1)

	if(len(session_locations) == 3):			
		session_telemetry["tutorial"] = complete_telemetry[0:session_locations[1]]
		session_telemetry["session_1"] = complete_telemetry[session_locations[1]:session_locations[2]]
		session_telemetry["session_2"] = complete_telemetry[session_locations[2]:]
	elif(len(session_locations) == 4):
		session_telemetry["tutorial"] = complete_telemetry[0:session_locations[1]]
		session_telemetry["session_1"] = complete_telemetry[session_locations[1]:session_locations[2]]
		session_telemetry["session_2"] = complete_telemetry[session_locations[2]:]
	return session_telemetry

def get_all_telemetry_from_sessions(session_1_keys, session_2_keys):
	return_telemetry = []
	for key in session_1_keys:
		telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		return_telemetry += telemetry["session_1"]

	for key in session_2_keys:
		telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		return_telemetry += telemetry["session_2"]

	return return_telemetry

def get_quest_accept_complete_present_single_session(session_keys, session_num):
	presented_quests = []
	accepted_quests = []
	completed_quests = []
	acceptance_rate = []
	completance_rate = [] 
	if(not(session_num == 1 or session_num == 2)):
		raise Exception("session num value must be one or two")

	if(session_num == 1):
		for key in session_keys: 
			total_quests = 0
			accepted_quests_num = 0
			completed_quests_num = 0
			telemetry = telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
			for t in telemetry["session_1"]:
				if "Quest:PositionQuest" in t:
					total_quests += 1
				if "Quest:Accept" in t:
					accepted_quests_num += 1
				if "Quest:Submit" in t:
					completed_quests_num += 1
			presented_quests.append(total_quests)
			accepted_quests.append(accepted_quests_num)
			completed_quests.append(completed_quests_num)
			acceptance_rate.append(accepted_quests_num/total_quests)
			completance_rate.append(completed_quests_num/accepted_quests_num)
		return presented_quests, accepted_quests, completed_quests, acceptance_rate, completance_rate

	if(session_num == 2):
		for key in session_keys: 
			total_quests = 0
			accepted_quests_num = 0
			completed_quests_num = 0
			telemetry = telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
			for t in telemetry["session_2"]:
				if "Quest:PositionQuest" in t:
					total_quests += 1
				if "Quest:Accept" in t:
					accepted_quests_num += 1
				if "Quest:Submit" in t:
					completed_quests_num += 1
			presented_quests.append(total_quests)
			accepted_quests.append(accepted_quests_num)
			completed_quests.append(completed_quests_num)
			acceptance_rate.append(accepted_quests_num/total_quests)
			completance_rate.append(completed_quests_num/accepted_quests_num)
		return presented_quests, accepted_quests, completed_quests, acceptance_rate, completance_rate

def get_quest_accept_complete_present(session_1_keys, session_2_keys):
	presented_quests = []
	accepted_quests = []
	completed_quests = []
	acceptance_rate = []
	completance_rate = [] 
	for key in session_1_keys: 
		total_quests = 0
		accepted_quests_num = 0
		completed_quests_num = 0
		telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:PositionQuest" in t:
				total_quests += 1
			if "Quest:Accept" in t:
				accepted_quests_num += 1
			if "Quest:Submit" in t:
				completed_quests_num += 1
		presented_quests.append(total_quests)
		accepted_quests.append(accepted_quests_num)
		completed_quests.append(completed_quests_num)
		acceptance_rate.append(accepted_quests_num/total_quests)
		completance_rate.append(completed_quests_num/accepted_quests_num)

	for key in session_2_keys: 
		total_quests = 0
		accepted_quests_num = 0
		completed_quests_num = 0
		telemetry = telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:PositionQuest" in t:
				total_quests += 1
			if "Quest:Accept" in t:
				accepted_quests_num += 1
			if "Quest:Submit" in t:
				completed_quests_num += 1
		presented_quests.append(total_quests)
		accepted_quests.append(accepted_quests_num)
		completed_quests.append(completed_quests_num)
		acceptance_rate.append(accepted_quests_num/total_quests)
		completance_rate.append(completed_quests_num/accepted_quests_num)
	return presented_quests, accepted_quests, completed_quests, acceptance_rate, completance_rate

def convert_quest_types_to_array(quest_type_dict):
	return_place = []
	return_plant = []
	return_cook = []
	return_harvest = []
	for d in quest_type_dict:
		return_place.append(d["place"])
		return_plant.append(d["plant"])
		return_cook.append(d["cook"])
		return_harvest.append(d["harvest"])
	return return_place, return_plant, return_cook, return_harvest




processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);

csvfile = open("processed_data.csv", "w", newline='')
csvwriter = csv.writer(csvfile)

csvwriter.writerow(["Number of participants", len(data)])
print("number of participants " + str(len(data)))

#Question: Is there an effect on the perception of the AI director based on which session? 
#testing whether there is a difference on the first or second time with the expeierence - need to do MANN U WILCOX tests on all of them
session_1_passage = []
session_1_RLAID = []
session_1_random = []
session_2_passage = []
session_2_RLAID = []
session_2_random = []

passage_then_RLAID_keys = []
passage_then_random_keys = []
RLAID_then_random_keys = []
RLAID_then_passage_keys = []
random_then_passage_keys = []
random_then_RLAID_keys = []
excluded_keys = []
for key in data.keys(): 
	aid_telemetry = []
	starting = []
	telemetry = data[key]["telemetry_data"].split("\n");
	for t in telemetry:
		if "SessionStart" in t:
			starting.append(t)
		if "QuestAlgorithm" in t:
			aid_telemetry.append(t)
	if(len(aid_telemetry) > 3):
		#try to repair the data
		#check for extra tutorial
		starting_locations = []
		for i in range(0, len(telemetry)):
			if "SessionStart" in telemetry[i]:
				starting_locations.append(i)
		#double tutorial
		if(starting_locations[1] - starting_locations[0] < 5):
			aid_telemetry = aid_telemetry[1:]

	if(len(starting) == 3 and len(aid_telemetry) == 2):
		if "Passage" in aid_telemetry[0]:
			session_1_passage.append(key)
		elif "RLAID" in aid_telemetry[0]:
			session_1_RLAID.append(key)
		elif "Random" in aid_telemetry[0]:
			session_1_random.append(key)

		if "Passage" in aid_telemetry[1]:
			session_2_passage.append(key)
		elif "RLAID" in aid_telemetry[1]:
			session_2_RLAID.append(key)
		elif "Random" in aid_telemetry[1]:
			session_2_random.append(key)

		if("Passage" in aid_telemetry[0] and "RLAID" in aid_telemetry[1]):
			passage_then_RLAID_keys.append(key)
		elif("Passage" in aid_telemetry[1] and "RLAID" in aid_telemetry[0]):
			RLAID_then_passage_keys.append(key)
		elif("Passage" in aid_telemetry[0] and "Random" in aid_telemetry[1]):
			passage_then_random_keys.append(key)
		elif("Passage" in aid_telemetry[1] and "Random" in aid_telemetry[0]):
			random_then_passage_keys.append(key)
		elif("Random" in aid_telemetry[0] and "RLAID" in aid_telemetry[1]):
			random_then_RLAID_keys.append(key)
		elif("Random" in aid_telemetry[1] and "RLAID" in aid_telemetry[0]):
			RLAID_then_random_keys.append(key)
	elif(len(aid_telemetry) != 3):
		print(aid_telemetry)
		print(starting_locations)
		excluded_keys.append(key)
		print("aid telem is greater than 3")
		continue
	if(len(aid_telemetry) == 3):
		if "Passage" in aid_telemetry[1]:
			session_1_passage.append(key)
		elif "RLAID" in aid_telemetry[1]:
			session_1_RLAID.append(key)
		elif "Random" in aid_telemetry[1]:
			session_1_random.append(key)

		if "Passage" in aid_telemetry[2]:
			session_2_passage.append(key)
		elif "RLAID" in aid_telemetry[2]:
			session_2_RLAID.append(key)
		elif "Random" in aid_telemetry[2]:
			session_2_random.append(key)

		if("Passage" in aid_telemetry[1] and "RLAID" in aid_telemetry[2]):
			passage_then_RLAID_keys.append(key)
		elif("Passage" in aid_telemetry[2] and "RLAID" in aid_telemetry[1]):
			RLAID_then_passage_keys.append(key)
		elif("Passage" in aid_telemetry[1] and "Random" in aid_telemetry[2]):
			passage_then_random_keys.append(key)
		elif("Passage" in aid_telemetry[2] and "Random" in aid_telemetry[1]):
			random_then_passage_keys.append(key)
		elif("Random" in aid_telemetry[1] and "RLAID" in aid_telemetry[2]):
			random_then_RLAID_keys.append(key)
		elif("Random" in aid_telemetry[2] and "RLAID" in aid_telemetry[1]):
			RLAID_then_random_keys.append(key)

	aid_telemetry.clear()


session_passage = session_1_passage + session_2_passage
session_RLAID = session_1_RLAID + session_2_RLAID
session_random = session_1_random + session_2_random

csvwriter.writerow(["number of participants with passage first", len(session_1_passage)])
csvwriter.writerow(["number of participants with passage second", len(session_2_passage)])
csvwriter.writerow(["number of participants with RLAID first", len(session_1_RLAID)])
csvwriter.writerow(["number of participants with RLAID second", len(session_2_RLAID)])
csvwriter.writerow(["number of participants with random first", len(session_1_random)])
csvwriter.writerow(["number of participants with random second", len(session_2_random)])
print("number of participants with passage first " + str(len(session_1_passage)))
print("number of participants with passage second " + str(len(session_2_passage)))
print("number of participants with RLAID first " + str(len(session_1_RLAID)))
print("number of participants with RLAID second " + str(len(session_2_RLAID)))
print("number of participants with random first " + str(len(session_1_random)))
print("number of participants with random second " + str(len(session_2_random)))

csvwriter.writerow(["number of participants with passage", len(session_passage)])
csvwriter.writerow(["number of participants with RLAID", len(session_RLAID)])
csvwriter.writerow(["number of participants with random", len(session_random)])
print("number of participants with passage " + str(len(session_passage)))
print("number of participants with RLAID " + str(len(session_RLAID)))
print("number of participants with random " + str(len(session_random)))

#process demographic data 
valid_keys = data.keys() - excluded_keys

csvwriter.writerow(["number of valid keys", len(valid_keys)])
print("number of valid keys " + str(len(valid_keys)))
demographic_survey_data = get_demograhic_survey_data_accross_keys(valid_keys)
fields = demographic_survey_data.keys()
csvdictwriter = csv.DictWriter(csvfile, fieldnames=fields)
csvdictwriter.writeheader()
csvdictwriter.writerow(demographic_survey_data)
print(demographic_survey_data)

#process short survey data
#check that the order doesn't matter
session_1_passage_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_passage, data)
session_2_passage_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_passage, data)
session_1_RLAID_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_RLAID, data)
session_2_RLAID_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_RLAID, data)
session_1_random_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_random, data)
session_2_random_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_random, data)

csvwriter.writerow(["Passage session 1 vs 2 kruskal test  pos accept", scipy.stats.kruskal(session_1_passage_survey_data["pos_accept"], session_2_passage_survey_data["pos_accept"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  neg accept", scipy.stats.kruskal(session_1_passage_survey_data["neg_accept"], session_2_passage_survey_data["neg_accept"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  pos complete", scipy.stats.kruskal(session_1_passage_survey_data["pos_complete"], session_2_passage_survey_data["pos_complete"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  neg complete", scipy.stats.kruskal(session_1_passage_survey_data["neg_complete"], session_2_passage_survey_data["neg_complete"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  variety", scipy.stats.kruskal(session_1_passage_survey_data["variety"], session_2_passage_survey_data["variety"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  pos enjoy", scipy.stats.kruskal(session_1_passage_survey_data["pos_enjoy"], session_2_passage_survey_data["pos_enjoy"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  neg enjoy", scipy.stats.kruskal(session_1_passage_survey_data["neg_enjoy"], session_2_passage_survey_data["neg_enjoy"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  pos recommned", scipy.stats.kruskal(session_1_passage_survey_data["pos_recommend"], session_2_passage_survey_data["pos_recommend"])])
csvwriter.writerow(["Passage session 1 vs 2 kruskal test  neg complete", scipy.stats.kruskal(session_1_passage_survey_data["neg_recommend"], session_2_passage_survey_data["neg_recommend"])])
print("Passage session 1 vs 2 kruskal test  pos accept")
print(scipy.stats.kruskal(session_1_passage_survey_data["pos_accept"], session_2_passage_survey_data["pos_accept"]))
print("Passage session 1 vs 2 kruskal test  neg accept")
print(scipy.stats.kruskal(session_1_passage_survey_data["neg_accept"], session_2_passage_survey_data["neg_accept"]))
print("Passage session 1 vs 2 kruskal test  pos complete")
print(scipy.stats.kruskal(session_1_passage_survey_data["pos_complete"], session_2_passage_survey_data["pos_complete"]))
print("Passage session 1 vs 2 kruskal test  neg complete")
print(scipy.stats.kruskal(session_1_passage_survey_data["neg_complete"], session_2_passage_survey_data["neg_complete"]))
print("Passage session 1 vs 2 kruskal test  variety")
print(scipy.stats.kruskal(session_1_passage_survey_data["variety"], session_2_passage_survey_data["variety"]))
print("Passage session 1 vs 2 kruskal test  pos enjoy")
print(scipy.stats.kruskal(session_1_passage_survey_data["pos_enjoy"], session_2_passage_survey_data["pos_enjoy"]))
print("Passage session 1 vs 2 kruskal test  neg enjoy")
print(scipy.stats.kruskal(session_1_passage_survey_data["neg_enjoy"], session_2_passage_survey_data["neg_enjoy"]))
print("Passage session 1 vs 2 kruskal test  pos recommned")
print(scipy.stats.kruskal(session_1_passage_survey_data["pos_recommend"], session_2_passage_survey_data["pos_recommend"]))
print("Passage session 1 vs 2 kruskal test  neg complete")
print(scipy.stats.kruskal(session_1_passage_survey_data["neg_recommend"], session_2_passage_survey_data["neg_recommend"]))

csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  pos accept", scipy.stats.kruskal(session_1_RLAID_survey_data["pos_accept"], session_2_RLAID_survey_data["pos_accept"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  neg accept", scipy.stats.kruskal(session_1_RLAID_survey_data["neg_accept"], session_2_RLAID_survey_data["neg_accept"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  pos complete", scipy.stats.kruskal(session_1_RLAID_survey_data["pos_complete"], session_2_RLAID_survey_data["pos_complete"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  neg complete", scipy.stats.kruskal(session_1_RLAID_survey_data["neg_complete"], session_2_RLAID_survey_data["neg_complete"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  variety", scipy.stats.kruskal(session_1_RLAID_survey_data["variety"], session_2_RLAID_survey_data["variety"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  pos enjoy", scipy.stats.kruskal(session_1_RLAID_survey_data["pos_enjoy"], session_2_RLAID_survey_data["pos_enjoy"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  neg enjoy", scipy.stats.kruskal(session_1_RLAID_survey_data["neg_enjoy"], session_2_RLAID_survey_data["neg_enjoy"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  pos recommned", scipy.stats.kruskal(session_1_RLAID_survey_data["pos_recommend"], session_2_RLAID_survey_data["pos_recommend"])])
csvwriter.writerow(["RLAID session 1 vs 2 kruskal test  neg complete",scipy.stats.kruskal(session_1_RLAID_survey_data["neg_recommend"], session_2_RLAID_survey_data["neg_recommend"])])
print("RLAID session 1 vs 2 kruskal test  pos accept")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["pos_accept"], session_2_RLAID_survey_data["pos_accept"]))
print("RLAID session 1 vs 2 kruskal test  neg accept")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["neg_accept"], session_2_RLAID_survey_data["neg_accept"]))
print("RLAID session 1 vs 2 kruskal test  pos complete")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["pos_complete"], session_2_RLAID_survey_data["pos_complete"]))
print("RLAID session 1 vs 2 kruskal test  neg complete")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["neg_complete"], session_2_RLAID_survey_data["neg_complete"]))
print("RLAID session 1 vs 2 kruskal test  variety")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["variety"], session_2_RLAID_survey_data["variety"]))
print("RLAID session 1 vs 2 kruskal test  pos enjoy")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["pos_enjoy"], session_2_RLAID_survey_data["pos_enjoy"]))
print("RLAID session 1 vs 2 kruskal test  neg enjoy")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["neg_enjoy"], session_2_RLAID_survey_data["neg_enjoy"]))
print("RLAID session 1 vs 2 kruskal test  pos recommned")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["pos_recommend"], session_2_RLAID_survey_data["pos_recommend"]))
print("RLAID session 1 vs 2 kruskal test  neg complete")
print(scipy.stats.kruskal(session_1_RLAID_survey_data["neg_recommend"], session_2_RLAID_survey_data["neg_recommend"]))

csvwriter.writerow(["random session 1 vs 2 kruskal test  pos accept", scipy.stats.kruskal(session_1_random_survey_data["pos_accept"], session_2_random_survey_data["pos_accept"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  neg accept", scipy.stats.kruskal(session_1_random_survey_data["neg_accept"], session_2_random_survey_data["neg_accept"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  pos complete", scipy.stats.kruskal(session_1_random_survey_data["pos_complete"], session_2_random_survey_data["pos_complete"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  neg complete", scipy.stats.kruskal(session_1_random_survey_data["neg_complete"], session_2_random_survey_data["neg_complete"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  variety", scipy.stats.kruskal(session_1_random_survey_data["variety"], session_2_random_survey_data["variety"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  pos enjoy", scipy.stats.kruskal(session_1_random_survey_data["pos_enjoy"], session_2_random_survey_data["pos_enjoy"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  neg enjoy",scipy.stats.kruskal(session_1_random_survey_data["neg_enjoy"], session_2_random_survey_data["neg_enjoy"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  pos recommned", scipy.stats.kruskal(session_1_random_survey_data["pos_recommend"], session_2_random_survey_data["pos_recommend"])])
csvwriter.writerow(["random session 1 vs 2 kruskal test  neg recommend", scipy.stats.kruskal(session_1_random_survey_data["neg_recommend"], session_2_random_survey_data["neg_recommend"])])
print("random session 1 vs 2 kruskal test  pos accept")
print(scipy.stats.kruskal(session_1_random_survey_data["pos_accept"], session_2_random_survey_data["pos_accept"]))
print("random session 1 vs 2 kruskal test  neg accept")
print(scipy.stats.kruskal(session_1_random_survey_data["neg_accept"], session_2_random_survey_data["neg_accept"]))
print("random session 1 vs 2 kruskal test  pos complete")
print(scipy.stats.kruskal(session_1_random_survey_data["pos_complete"], session_2_random_survey_data["pos_complete"]))
print("random session 1 vs 2 kruskal test  neg complete")
print(scipy.stats.kruskal(session_1_random_survey_data["neg_complete"], session_2_random_survey_data["neg_complete"]))
print("random session 1 vs 2 kruskal test  variety")
print(scipy.stats.kruskal(session_1_random_survey_data["variety"], session_2_random_survey_data["variety"]))
print("random session 1 vs 2 kruskal test  pos enjoy")
print(scipy.stats.kruskal(session_1_random_survey_data["pos_enjoy"], session_2_random_survey_data["pos_enjoy"]))
print("random session 1 vs 2 kruskal test  neg enjoy")
print(scipy.stats.kruskal(session_1_random_survey_data["neg_enjoy"], session_2_random_survey_data["neg_enjoy"]))
print("random session 1 vs 2 kruskal test  pos recommned")
print(scipy.stats.kruskal(session_1_random_survey_data["pos_recommend"], session_2_random_survey_data["pos_recommend"]))
print("random session 1 vs 2 kruskal test  neg recommend")
print(scipy.stats.kruskal(session_1_random_survey_data["neg_recommend"], session_2_random_survey_data["neg_recommend"]))

#combined survey data
session_passage_survey_data = get_short_survey_data_accross_keys(session_1_passage, session_2_passage)
session_RLAID_survey_data = get_short_survey_data_accross_keys(session_1_RLAID, session_2_RLAID)
session_random_survey_data = get_short_survey_data_accross_keys(session_1_random, session_2_random)


session_1_passage_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_passage, data)
session_2_passage_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_passage, data)
session_1_RLAID_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_RLAID, data)
session_2_RLAID_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_RLAID, data)
session_1_random_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_random, data)
session_2_random_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_random, data)


print("Average session 1 random pos enjoy: " + str(statistics.mean(session_1_random_survey_data["pos_enjoy"])))
print("Average session 2 random pos enjoy: " + str(statistics.mean(session_2_random_survey_data["pos_enjoy"])))

print("Median session 1 random pos enjoy: " + str(statistics.median(session_1_random_survey_data["pos_enjoy"])))
print("Median session 2 random pos enjoy: " + str(statistics.median(session_2_random_survey_data["pos_enjoy"])))


print("passage session 1 vs 2 pos enjoy mannwhitneyu greater hypothesis: " + str(scipy.stats.mannwhitneyu(session_1_passage_survey_data["pos_enjoy"], session_2_passage_survey_data["pos_enjoy"], alternative="greater")))
print("RLAID session 1 vs 2 pos enjoy mannwhitneyu greater hypothesis: " + str(scipy.stats.mannwhitneyu(session_1_RLAID_survey_data["pos_enjoy"], session_2_RLAID_survey_data["pos_enjoy"], alternative="greater")))
print("random session 1 vs 2 pos enjoy mannwhitneyu greater hypothesis: " + str(scipy.stats.mannwhitneyu(session_1_random_survey_data["pos_enjoy"], session_2_random_survey_data["pos_enjoy"], alternative="greater")))

csvwriter.writerow(["Passage Median Short Survey Pos Accept", statistics.median(session_passage_survey_data["pos_accept"])])
csvwriter.writerow(["Passage Median Short Survey neg Accept", statistics.median(session_passage_survey_data["neg_accept"])])
csvwriter.writerow(["Passage Median Short Survey Pos complete", statistics.median(session_passage_survey_data["pos_complete"])])
csvwriter.writerow(["Passage Median Short Survey neg complete", statistics.median(session_passage_survey_data["neg_complete"])])
csvwriter.writerow(["Passage Median Short Survey variety", statistics.median(session_passage_survey_data["variety"])])
csvwriter.writerow(["Passage Median Short Survey Pos enjoy", statistics.median(session_passage_survey_data["pos_enjoy"])])
csvwriter.writerow(["Passage Median Short Survey neg enjoy", statistics.median(session_passage_survey_data["neg_enjoy"])])
csvwriter.writerow(["Passage Median Short Survey Pos recommend", statistics.median(session_passage_survey_data["pos_recommend"])])
csvwriter.writerow(["Passage Median Short Survey neg recommend", statistics.median(session_passage_survey_data["neg_recommend"])])

csvwriter.writerow(["RLAID Median Short Survey Pos Accept", statistics.median(session_RLAID_survey_data["pos_accept"])])
csvwriter.writerow(["RLAID Median Short Survey neg Accept", statistics.median(session_RLAID_survey_data["neg_accept"])])
csvwriter.writerow(["RLAID Median Short Survey Pos complete", statistics.median(session_RLAID_survey_data["pos_complete"])])
csvwriter.writerow(["RLAID Median Short Survey neg complete", statistics.median(session_RLAID_survey_data["neg_complete"])])
csvwriter.writerow(["RLAID Median Short Survey variety", statistics.median(session_RLAID_survey_data["variety"])])
csvwriter.writerow(["RLAID Median Short Survey Pos enjoy", statistics.median(session_RLAID_survey_data["pos_enjoy"])])
csvwriter.writerow(["RLAID Median Short Survey neg enjoy", statistics.median(session_RLAID_survey_data["neg_enjoy"])])
csvwriter.writerow(["RLAID Median Short Survey Pos recommend", statistics.median(session_RLAID_survey_data["pos_recommend"])])
csvwriter.writerow(["RLAID Median Short Survey neg recommend", statistics.median(session_RLAID_survey_data["neg_recommend"])])

csvwriter.writerow(["random Median Short Survey Pos Accept", statistics.median(session_random_survey_data["pos_accept"])])
csvwriter.writerow(["random Median Short Survey neg Accept", statistics.median(session_random_survey_data["neg_accept"])])
csvwriter.writerow(["random Median Short Survey Pos complete", statistics.median(session_random_survey_data["pos_complete"])])
csvwriter.writerow(["random Median Short Survey neg complete", statistics.median(session_random_survey_data["neg_complete"])])
csvwriter.writerow(["random Median Short Survey variety", statistics.median(session_random_survey_data["variety"])])
csvwriter.writerow(["random Median Short Survey Pos enjoy", statistics.median(session_random_survey_data["pos_enjoy"])])
csvwriter.writerow(["random Median Short Survey neg enjoy", statistics.median(session_random_survey_data["neg_enjoy"])])
csvwriter.writerow(["random Median Short Survey Pos recommend", statistics.median(session_random_survey_data["pos_recommend"])])
csvwriter.writerow(["random Median Short Survey neg recommend", statistics.median(session_random_survey_data["neg_recommend"])])


bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_medians = [statistics.median(session_passage_survey_data["pos_accept"]), 
				   statistics.median(session_passage_survey_data["neg_accept"]),
				   statistics.median(session_passage_survey_data["pos_complete"]),
				   statistics.median(session_passage_survey_data["neg_complete"]), 
				   statistics.median(session_passage_survey_data["variety"]),
				   statistics.median(session_passage_survey_data["pos_enjoy"]),
				   statistics.median(session_passage_survey_data["neg_enjoy"]), 
				   statistics.median(session_passage_survey_data["pos_recommend"]), 
				   statistics.median(session_passage_survey_data["neg_recommend"])]

RLAID_medians = [statistics.median(session_RLAID_survey_data["pos_accept"]), 
				   statistics.median(session_RLAID_survey_data["neg_accept"]),
				   statistics.median(session_RLAID_survey_data["pos_complete"]),
				   statistics.median(session_RLAID_survey_data["neg_complete"]), 
				   statistics.median(session_RLAID_survey_data["variety"]),
				   statistics.median(session_RLAID_survey_data["pos_enjoy"]),
				   statistics.median(session_RLAID_survey_data["neg_enjoy"]), 
				   statistics.median(session_RLAID_survey_data["pos_recommend"]), 
				   statistics.median(session_RLAID_survey_data["neg_recommend"])]

random_medians = [statistics.median(session_random_survey_data["pos_accept"]), 
				   statistics.median(session_random_survey_data["neg_accept"]),
				   statistics.median(session_random_survey_data["pos_complete"]),
				   statistics.median(session_random_survey_data["neg_complete"]), 
				   statistics.median(session_random_survey_data["variety"]),
				   statistics.median(session_random_survey_data["pos_enjoy"]),
				   statistics.median(session_random_survey_data["neg_enjoy"]), 
				   statistics.median(session_random_survey_data["pos_recommend"]), 
				   statistics.median(session_random_survey_data["neg_recommend"])]


br1 = np.arange(len(passage_medians))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_medians, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, RLAID_medians, width = bar_width, label = 'RLAID')
plt.bar(br3, random_medians, width = bar_width, label = 'Random')

plt.title('Short Survey Median Answers', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Median Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_medians))], ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'])

plt.legend()
plt.savefig('short_survey/short_survey_median.png', bbox_inches='tight')


bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_means = [statistics.mean(session_passage_survey_data["pos_accept"]), 
				   statistics.mean(session_passage_survey_data["neg_accept"]),
				   statistics.mean(session_passage_survey_data["pos_complete"]),
				   statistics.mean(session_passage_survey_data["neg_complete"]), 
				   statistics.mean(session_passage_survey_data["variety"]),
				   statistics.mean(session_passage_survey_data["pos_enjoy"]),
				   statistics.mean(session_passage_survey_data["neg_enjoy"]), 
				   statistics.mean(session_passage_survey_data["pos_recommend"]), 
				   statistics.mean(session_passage_survey_data["neg_recommend"])]

passage_stdev = [statistics.stdev(session_passage_survey_data["pos_accept"]), 
				   statistics.stdev(session_passage_survey_data["neg_accept"]),
				   statistics.stdev(session_passage_survey_data["pos_complete"]),
				   statistics.stdev(session_passage_survey_data["neg_complete"]), 
				   statistics.stdev(session_passage_survey_data["variety"]),
				   statistics.stdev(session_passage_survey_data["pos_enjoy"]),
				   statistics.stdev(session_passage_survey_data["neg_enjoy"]), 
				   statistics.stdev(session_passage_survey_data["pos_recommend"]), 
				   statistics.stdev(session_passage_survey_data["neg_recommend"])]

RLAID_means = [statistics.mean(session_RLAID_survey_data["pos_accept"]), 
				   statistics.mean(session_RLAID_survey_data["neg_accept"]),
				   statistics.mean(session_RLAID_survey_data["pos_complete"]),
				   statistics.mean(session_RLAID_survey_data["neg_complete"]), 
				   statistics.mean(session_RLAID_survey_data["variety"]),
				   statistics.mean(session_RLAID_survey_data["pos_enjoy"]),
				   statistics.mean(session_RLAID_survey_data["neg_enjoy"]), 
				   statistics.mean(session_RLAID_survey_data["pos_recommend"]), 
				   statistics.mean(session_RLAID_survey_data["neg_recommend"])]

RLAID_stdev = [statistics.stdev(session_RLAID_survey_data["pos_accept"]), 
				   statistics.stdev(session_RLAID_survey_data["neg_accept"]),
				   statistics.stdev(session_RLAID_survey_data["pos_complete"]),
				   statistics.stdev(session_RLAID_survey_data["neg_complete"]), 
				   statistics.stdev(session_RLAID_survey_data["variety"]),
				   statistics.stdev(session_RLAID_survey_data["pos_enjoy"]),
				   statistics.stdev(session_RLAID_survey_data["neg_enjoy"]), 
				   statistics.stdev(session_RLAID_survey_data["pos_recommend"]), 
				   statistics.stdev(session_RLAID_survey_data["neg_recommend"])]

random_means = [statistics.mean(session_random_survey_data["pos_accept"]), 
				   statistics.mean(session_random_survey_data["neg_accept"]),
				   statistics.mean(session_random_survey_data["pos_complete"]),
				   statistics.mean(session_random_survey_data["neg_complete"]), 
				   statistics.mean(session_random_survey_data["variety"]),
				   statistics.mean(session_random_survey_data["pos_enjoy"]),
				   statistics.mean(session_random_survey_data["neg_enjoy"]), 
				   statistics.mean(session_random_survey_data["pos_recommend"]), 
				   statistics.mean(session_random_survey_data["neg_recommend"])]

random_stdev = [statistics.stdev(session_random_survey_data["pos_accept"]), 
				   statistics.stdev(session_random_survey_data["neg_accept"]),
				   statistics.stdev(session_random_survey_data["pos_complete"]),
				   statistics.stdev(session_random_survey_data["neg_complete"]), 
				   statistics.stdev(session_random_survey_data["variety"]),
				   statistics.stdev(session_random_survey_data["pos_enjoy"]),
				   statistics.stdev(session_random_survey_data["neg_enjoy"]), 
				   statistics.stdev(session_random_survey_data["pos_recommend"]), 
				   statistics.stdev(session_random_survey_data["neg_recommend"])]

br1 = np.arange(len(passage_means))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_means, width = bar_width, yerr=passage_stdev, label = 'PaSSAGE')
plt.bar(br2, RLAID_means, width = bar_width, yerr=RLAID_stdev, label = 'RLAID')
plt.bar(br3, random_means, width = bar_width, yerr=random_stdev, label = 'Random')

plt.title('Short Survey Mean Answers', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_medians))], ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'])

plt.legend()
plt.savefig('short_survey/short_survey_mean.png', bbox_inches='tight')

print("correlation tests: ")
print("Passage correlation pos vs neg accept")
print(scipy.stats.pearsonr(session_passage_survey_data["pos_accept"], session_passage_survey_data["neg_accept"]))
print("Passage correlation pos vs neg complete")
print(scipy.stats.pearsonr(session_passage_survey_data["pos_complete"], session_passage_survey_data["neg_complete"]))
print("Passage correlation pos vs neg enjoy")
print(scipy.stats.pearsonr(session_passage_survey_data["pos_enjoy"], session_passage_survey_data["neg_enjoy"]))
print("Passage correlation pos vs neg recommend")
print(scipy.stats.pearsonr(session_passage_survey_data["pos_recommend"], session_passage_survey_data["neg_recommend"]))

print("RLAID correlation pos vs neg accept")
print(scipy.stats.pearsonr(session_RLAID_survey_data["pos_accept"], session_RLAID_survey_data["neg_accept"]))
print("RLAID correlation pos vs neg complete")
print(scipy.stats.pearsonr(session_RLAID_survey_data["pos_complete"], session_RLAID_survey_data["neg_complete"]))
print("RLAID correlation pos vs neg enjoy")
print(scipy.stats.pearsonr(session_RLAID_survey_data["pos_enjoy"], session_RLAID_survey_data["neg_enjoy"]))
print("RLAID correlation pos vs neg recommend")
print(scipy.stats.pearsonr(session_RLAID_survey_data["pos_recommend"], session_RLAID_survey_data["neg_recommend"]))

print("random correlation pos vs neg accept")
print(scipy.stats.pearsonr(session_random_survey_data["pos_accept"], session_random_survey_data["neg_accept"]))
print("random correlation pos vs neg complete")
print(scipy.stats.pearsonr(session_random_survey_data["pos_complete"], session_random_survey_data["neg_complete"]))
print("random correlation pos vs neg enjoy")
print(scipy.stats.pearsonr(session_random_survey_data["pos_enjoy"], session_random_survey_data["neg_enjoy"]))
print("random correlation pos vs neg recommend")
print(scipy.stats.pearsonr(session_random_survey_data["pos_recommend"], session_random_survey_data["neg_recommend"]))



#run stats test on likert data 
print("Passage vs RLAID  pos acceptance " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_accept"], session_RLAID_survey_data["pos_accept"])))
print("random vs RLAID  pos acceptance " + str(scipy.stats.mannwhitneyu(session_random_survey_data["pos_accept"], session_RLAID_survey_data["pos_accept"])))
print("Passage vs random  pos acceptance " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_accept"], session_random_survey_data["pos_accept"])))

print("Passage vs RLAID  neg acceptance " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_accept"], session_RLAID_survey_data["neg_accept"])))
print("random vs RLAID  neg acceptance " + str(scipy.stats.mannwhitneyu(session_random_survey_data["neg_accept"], session_RLAID_survey_data["neg_accept"])))
print("Passage vs random  neg acceptance " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_accept"], session_random_survey_data["neg_accept"])))

print("Passage vs RLAID  pos complete " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_complete"], session_RLAID_survey_data["pos_complete"])))
print("random vs RLAID  pos complete " + str(scipy.stats.mannwhitneyu(session_random_survey_data["pos_complete"], session_RLAID_survey_data["pos_complete"])))
print("Passage vs random  pos complete " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_complete"], session_random_survey_data["pos_complete"])))

print("Passage vs RLAID  neg complete " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_complete"], session_RLAID_survey_data["neg_complete"])))
print("random vs RLAID  neg complete " + str(scipy.stats.mannwhitneyu(session_random_survey_data["neg_complete"], session_RLAID_survey_data["neg_complete"])))
print("Passage vs random  neg complete " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_complete"], session_random_survey_data["neg_complete"])))

print("Passage vs RLAID  variety " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["variety"], session_RLAID_survey_data["variety"])))
print("random vs RLAID  variety " + str(scipy.stats.mannwhitneyu(session_random_survey_data["variety"], session_RLAID_survey_data["variety"])))
print("Passage vs random  variety " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["variety"], session_random_survey_data["variety"])))

print("Passage vs RLAID  pos enjoy " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_enjoy"], session_RLAID_survey_data["pos_enjoy"])))
print("random vs RLAID  pos enjoy " + str(scipy.stats.mannwhitneyu(session_random_survey_data["pos_enjoy"], session_RLAID_survey_data["pos_enjoy"])))
print("Passage vs random  pos enjoy " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_enjoy"], session_random_survey_data["pos_enjoy"])))

print("Passage vs RLAID  neg enjoy " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_enjoy"], session_RLAID_survey_data["neg_enjoy"])))
print("random vs RLAID  neg enjoy " + str(scipy.stats.mannwhitneyu(session_random_survey_data["neg_enjoy"], session_RLAID_survey_data["neg_enjoy"])))
print("Passage vs random  neg enjoy " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_enjoy"], session_random_survey_data["neg_enjoy"])))

print("Passage vs RLAID  pos recommend " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_recommend"], session_RLAID_survey_data["pos_recommend"])))
print("random vs RLAID  pos recommend " + str(scipy.stats.mannwhitneyu(session_random_survey_data["pos_recommend"], session_RLAID_survey_data["pos_recommend"])))
print("Passage vs random  pos recommend " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["pos_recommend"], session_random_survey_data["pos_recommend"])))

print("Passage vs RLAID  neg recommend " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_recommend"], session_RLAID_survey_data["neg_recommend"])))
print("random vs RLAID  neg recommend " + str(scipy.stats.mannwhitneyu(session_random_survey_data["neg_recommend"], session_RLAID_survey_data["neg_recommend"])))
print("Passage vs random  neg recommend " + str(scipy.stats.mannwhitneyu(session_passage_survey_data["neg_recommend"], session_random_survey_data["neg_recommend"])))



#get overview data 
passage_telemetry = get_all_telemetry_from_sessions(session_1_passage, session_2_passage)
RLAID_telemetry = get_all_telemetry_from_sessions(session_1_RLAID, session_2_RLAID)
random_telemetry = get_all_telemetry_from_sessions(session_1_random, session_2_random)

passage_presented_quests_telem = []
passage_accepted_quests_telem = []
passage_completed_quests_telem = []
passage_total_quests = 0
passage_accepted_quests = 0
passage_completed_quests = 0
for t in passage_telemetry:
	if "Quest:PositionQuest" in t:
		passage_presented_quests_telem.append(t)
		passage_total_quests += 1
	if "Quest:Accept" in t:
		passage_accepted_quests_telem.append(t)
		passage_accepted_quests += 1
	if "Quest:Submit" in t:
		passage_completed_quests_telem.append(t)
		passage_completed_quests += 1

RLAID_presented_quests_telem = []
RLAID_accepted_quests_telem = []
RLAID_completed_quests_telem = []
RLAID_total_quests = 0
RLAID_accepted_quests = 0
RLAID_completed_quests = 0
for t in RLAID_telemetry:
	if "Quest:PositionQuest" in t:
		RLAID_presented_quests_telem.append(t)
		RLAID_total_quests += 1
	if "Quest:Accept" in t:
		RLAID_accepted_quests_telem.append(t)
		RLAID_accepted_quests += 1
	if "Quest:Submit" in t:
		RLAID_completed_quests_telem.append(t)
		RLAID_completed_quests += 1

random_presented_quests_telem = []
random_accepted_quests_telem = []
random_completed_quests_telem = []
random_total_quests = 0
random_accepted_quests = 0
random_completed_quests = 0
for t in random_telemetry:
	if "Quest:PositionQuest" in t:
		random_presented_quests_telem.append(t)
		random_total_quests += 1
	if "Quest:Accept" in t:
		random_accepted_quests_telem.append(t)
		random_accepted_quests += 1
	if "Quest:Submit" in t:
		random_completed_quests_telem.append(t)
		random_completed_quests += 1

passage_presented_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in passage_presented_quests_telem:
	if "Place" in quest: 
		passage_presented_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		passage_presented_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		passage_presented_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		passage_presented_quest_type_count["harvest"] += 1

passage_accepted_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in passage_accepted_quests_telem:
	if "Place" in quest: 
		passage_accepted_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		passage_accepted_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		passage_accepted_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		passage_accepted_quest_type_count["harvest"] += 1

passage_completed_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in passage_completed_quests_telem:
	if "Place" in quest: 
		passage_completed_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		passage_completed_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		passage_completed_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		passage_completed_quest_type_count["harvest"] += 1

RLAID_presented_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in RLAID_presented_quests_telem:
	if "Place" in quest: 
		RLAID_presented_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		RLAID_presented_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		RLAID_presented_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		RLAID_presented_quest_type_count["harvest"] += 1

RLAID_accepted_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in RLAID_accepted_quests_telem:
	if "Place" in quest: 
		RLAID_accepted_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		RLAID_accepted_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		RLAID_accepted_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		RLAID_accepted_quest_type_count["harvest"] += 1

RLAID_completed_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in RLAID_completed_quests_telem:
	if "Place" in quest: 
		RLAID_completed_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		RLAID_completed_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		RLAID_completed_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		RLAID_completed_quest_type_count["harvest"] += 1

random_presented_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in random_presented_quests_telem:
	if "Place" in quest: 
		random_presented_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		random_presented_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		random_presented_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		random_presented_quest_type_count["harvest"] += 1

random_accepted_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in random_accepted_quests_telem:
	if "Place" in quest: 
		random_accepted_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		random_accepted_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		random_accepted_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		random_accepted_quest_type_count["harvest"] += 1

random_completed_quest_type_count = {"place":0, "plant":0, "cook":0, "harvest":0}
for quest in random_completed_quests_telem:
	if "Place" in quest: 
		random_completed_quest_type_count["place"] += 1
	elif "Plant" in quest: 
		random_completed_quest_type_count["plant"] += 1
	elif "Cook" in quest:
		random_completed_quest_type_count["cook"] += 1 
	elif "Harvest" in quest: 
		random_completed_quest_type_count["harvest"] += 1

bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_presented_quest_types = [passage_presented_quest_type_count["place"],
								passage_presented_quest_type_count["plant"],
								passage_presented_quest_type_count["cook"],
								passage_presented_quest_type_count["harvest"]]

RLAID_presented_quest_types = [RLAID_presented_quest_type_count["place"],
							   RLAID_presented_quest_type_count["plant"],
							   RLAID_presented_quest_type_count["cook"],
							   RLAID_presented_quest_type_count["harvest"]]

random_presented_quest_types = [random_presented_quest_type_count["place"],
							   random_presented_quest_type_count["plant"],
							   random_presented_quest_type_count["cook"],
							   random_presented_quest_type_count["harvest"]]

br1 = np.arange(len(passage_presented_quest_types))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_presented_quest_types, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, RLAID_presented_quest_types, width = bar_width, label = 'RLAID')
plt.bar(br3, random_presented_quest_types, width = bar_width, label = 'Random')

plt.title('Presented Quest Types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_presented_quest_types))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/presented_quests.png', bbox_inches='tight')

bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_accepted_quest_types = [passage_accepted_quest_type_count["place"],
								passage_accepted_quest_type_count["plant"],
								passage_accepted_quest_type_count["cook"],
								passage_accepted_quest_type_count["harvest"]]

RLAID_accepted_quest_types = [RLAID_accepted_quest_type_count["place"],
							   RLAID_accepted_quest_type_count["plant"],
							   RLAID_accepted_quest_type_count["cook"],
							   RLAID_accepted_quest_type_count["harvest"]]

random_accepted_quest_types = [random_accepted_quest_type_count["place"],
							   random_accepted_quest_type_count["plant"],
							   random_accepted_quest_type_count["cook"],
							   random_accepted_quest_type_count["harvest"]]

br1 = np.arange(len(passage_accepted_quest_types))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_accepted_quest_types, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, RLAID_accepted_quest_types, width = bar_width, label = 'RLAID')
plt.bar(br3, random_accepted_quest_types, width = bar_width, label = 'Random')

plt.title('Accepted Quest Types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_accepted_quest_types))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/accepted_quests.png', bbox_inches='tight')

bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_completed_quest_types = [passage_completed_quest_type_count["place"],
								passage_completed_quest_type_count["plant"],
								passage_completed_quest_type_count["cook"],
								passage_completed_quest_type_count["harvest"]]

RLAID_completed_quest_types = [RLAID_completed_quest_type_count["place"],
							   RLAID_completed_quest_type_count["plant"],
							   RLAID_completed_quest_type_count["cook"],
							   RLAID_completed_quest_type_count["harvest"]]

random_completed_quest_types = [random_completed_quest_type_count["place"],
							   random_completed_quest_type_count["plant"],
							   random_completed_quest_type_count["cook"],
							   random_completed_quest_type_count["harvest"]]

br1 = np.arange(len(passage_completed_quest_types))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_completed_quest_types, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, RLAID_completed_quest_types, width = bar_width, label = 'RLAID')
plt.bar(br3, random_completed_quest_types, width = bar_width, label = 'Random')

plt.title('Completed Quest Types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_completed_quest_types))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/completed_quests.png', bbox_inches='tight')

passage_presented_quest_types, passage_accepted_quest_types, passage_completed_quest_types = processing_util.get_quest_type_count_for_each_player(session_1_passage, session_2_passage, data)
RLAID_presented_quest_types, RLAID_accepted_quest_types, RLAID_completed_quest_types = processing_util.get_quest_type_count_for_each_player(session_1_RLAID, session_2_RLAID, data)
random_presented_quest_types, random_accepted_quest_types, random_completed_quest_types = processing_util.get_quest_type_count_for_each_player(session_1_random, session_2_random, data)

passage_presented_place, passage_presented_plant, passage_presented_cook, passage_presented_harvest = convert_quest_types_to_array(passage_presented_quest_types)
RLAID_presented_place, RLAID_presented_plant, RLAID_presented_cook, RLAID_presented_harvest = convert_quest_types_to_array(RLAID_presented_quest_types)
random_presented_place, random_presented_plant, random_presented_cook, random_presented_harvest = convert_quest_types_to_array(random_presented_quest_types)


bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_presented_qt_count = [statistics.mean(passage_presented_place),
							  statistics.mean(passage_presented_plant),
							  statistics.mean(passage_presented_cook),
							  statistics.mean(passage_presented_harvest)]

passage_presented_qt_stdev = [statistics.stdev(passage_presented_place),
							  statistics.stdev(passage_presented_plant),
							  statistics.stdev(passage_presented_cook),
							  statistics.stdev(passage_presented_harvest)]

RLAID_presented_qt_count = [statistics.mean(RLAID_presented_place),
							  statistics.mean(RLAID_presented_plant),
							  statistics.mean(RLAID_presented_cook),
							  statistics.mean(RLAID_presented_harvest)]

RLAID_presented_qt_stdev = [statistics.stdev(RLAID_presented_place),
							  statistics.stdev(RLAID_presented_plant),
							  statistics.stdev(RLAID_presented_cook),
							  statistics.stdev(RLAID_presented_harvest)]

random_presented_qt_count = [statistics.mean(random_presented_place),
							  statistics.mean(random_presented_plant),
							  statistics.mean(random_presented_cook),
							  statistics.mean(random_presented_harvest)]

random_presented_qt_stdev = [statistics.stdev(random_presented_place),
							  statistics.stdev(random_presented_plant),
							  statistics.stdev(random_presented_cook),
							  statistics.stdev(random_presented_harvest)]


br1 = np.arange(len(passage_presented_qt_count))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_presented_qt_count, width = bar_width, yerr=passage_presented_qt_stdev, label = 'PaSSAGE')
plt.bar(br2, RLAID_presented_qt_count, width = bar_width,yerr=RLAID_presented_qt_stdev, label = 'RLAID')
plt.bar(br3, random_presented_qt_count, width = bar_width, yerr=random_presented_qt_stdev, label = 'Random')

plt.title('Per player average presented quest types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_presented_qt_count))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/per_player_average_presented_quest_types.png', bbox_inches='tight')

csvwriter.writerow(["passage average presented place", statistics.mean(passage_presented_place), "stdev", statistics.stdev(passage_presented_place), "SEM", stats.sem(passage_presented_place)])
csvwriter.writerow(["passage average presented plant", statistics.mean(passage_presented_plant), "stdev", statistics.stdev(passage_presented_plant), "SEM", stats.sem(passage_presented_plant)])
csvwriter.writerow(["passage average presented cook", statistics.mean(passage_presented_cook), "stdev", statistics.stdev(passage_presented_cook), "SEM", stats.sem(passage_presented_cook)])
csvwriter.writerow(["passage average presented harvest", statistics.mean(passage_presented_harvest), "stdev", statistics.stdev(passage_presented_harvest), "SEM", stats.sem(passage_presented_harvest)])

csvwriter.writerow(["RLAID average presented place", statistics.mean(RLAID_presented_place), "stdev", statistics.stdev(RLAID_presented_place), "SEM", stats.sem(RLAID_presented_place)])
csvwriter.writerow(["RLAID average presented plant", statistics.mean(RLAID_presented_plant), "stdev", statistics.stdev(RLAID_presented_plant), "SEM", stats.sem(RLAID_presented_plant)])
csvwriter.writerow(["RLAID average presented cook", statistics.mean(RLAID_presented_cook), "stdev", statistics.stdev(RLAID_presented_cook), "SEM", stats.sem(RLAID_presented_cook)])
csvwriter.writerow(["RLAID average presented harvest", statistics.mean(RLAID_presented_harvest), "stdev", statistics.stdev(RLAID_presented_harvest), "SEM", stats.sem(RLAID_presented_harvest)])

csvwriter.writerow(["random average presented place", statistics.mean(random_presented_place), "stdev", statistics.stdev(random_presented_place), "SEM", stats.sem(random_presented_place)])
csvwriter.writerow(["random average presented plant", statistics.mean(random_presented_plant), "stdev", statistics.stdev(random_presented_plant), "SEM", stats.sem(random_presented_plant)])
csvwriter.writerow(["random average presented cook", statistics.mean(random_presented_cook), "stdev", statistics.stdev(random_presented_cook), "SEM", stats.sem(random_presented_cook)])
csvwriter.writerow(["random average presented harvest", statistics.mean(random_presented_harvest), "stdev", statistics.stdev(random_presented_harvest), "SEM", stats.sem(random_presented_harvest)])

passage_accepted_place, passage_accepted_plant, passage_accepted_cook, passage_accepted_harvest = convert_quest_types_to_array(passage_accepted_quest_types)
RLAID_accepted_place, RLAID_accepted_plant, RLAID_accepted_cook, RLAID_accepted_harvest = convert_quest_types_to_array(RLAID_accepted_quest_types)
random_accepted_place, random_accepted_plant, random_accepted_cook, random_accepted_harvest = convert_quest_types_to_array(random_accepted_quest_types)
	 
bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_accepted_qt_count = [statistics.mean(passage_accepted_place),
							  statistics.mean(passage_accepted_plant),
							  statistics.mean(passage_accepted_cook),
							  statistics.mean(passage_accepted_harvest)]

passage_accepted_qt_stdev = [statistics.stdev(passage_accepted_place),
							  statistics.stdev(passage_accepted_plant),
							  statistics.stdev(passage_accepted_cook),
							  statistics.stdev(passage_accepted_harvest)]

RLAID_accepted_qt_count = [statistics.mean(RLAID_accepted_place),
							  statistics.mean(RLAID_accepted_plant),
							  statistics.mean(RLAID_accepted_cook),
							  statistics.mean(RLAID_accepted_harvest)]

RLAID_accepted_qt_stdev = [statistics.stdev(RLAID_accepted_place),
							  statistics.stdev(RLAID_accepted_plant),
							  statistics.stdev(RLAID_accepted_cook),
							  statistics.stdev(RLAID_accepted_harvest)]

random_accepted_qt_count = [statistics.mean(random_accepted_place),
							  statistics.mean(random_accepted_plant),
							  statistics.mean(random_accepted_cook),
							  statistics.mean(random_accepted_harvest)]

random_accepted_qt_stdev = [statistics.stdev(random_accepted_place),
							  statistics.stdev(random_accepted_plant),
							  statistics.stdev(random_accepted_cook),
							  statistics.stdev(random_accepted_harvest)]


br1 = np.arange(len(passage_accepted_qt_count))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_accepted_qt_count, width = bar_width, yerr=passage_accepted_qt_stdev, label = 'PaSSAGE')
plt.bar(br2, RLAID_accepted_qt_count, width = bar_width,yerr=RLAID_accepted_qt_stdev, label = 'RLAID')
plt.bar(br3, random_accepted_qt_count, width = bar_width, yerr=random_accepted_qt_stdev, label = 'Random')

plt.title('Per player average accepted quest types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(passage_accepted_qt_count))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/per_player_average_accepted_quest_types.png', bbox_inches='tight')

csvwriter.writerow(["passage average accepted place", statistics.mean(passage_accepted_place), "stdev", statistics.stdev(passage_accepted_place), "SEM", stats.sem(passage_accepted_place)])
csvwriter.writerow(["passage average accepted plant", statistics.mean(passage_accepted_plant), "stdev", statistics.stdev(passage_accepted_plant), "SEM", stats.sem(passage_accepted_plant)])
csvwriter.writerow(["passage average accepted cook", statistics.mean(passage_accepted_cook), "stdev", statistics.stdev(passage_accepted_cook), "SEM", stats.sem(passage_accepted_cook)])
csvwriter.writerow(["passage average accepted harvest", statistics.mean(passage_accepted_harvest), "stdev", statistics.stdev(passage_accepted_harvest), "SEM", stats.sem(passage_accepted_harvest)])

csvwriter.writerow(["RLAID average accepted place", statistics.mean(RLAID_accepted_place), "stdev", statistics.stdev(RLAID_accepted_place), "SEM", stats.sem(RLAID_accepted_place)])
csvwriter.writerow(["RLAID average accepted plant", statistics.mean(RLAID_accepted_plant), "stdev", statistics.stdev(RLAID_accepted_plant), "SEM", stats.sem(RLAID_accepted_plant)])
csvwriter.writerow(["RLAID average accepted cook", statistics.mean(RLAID_accepted_cook), "stdev", statistics.stdev(RLAID_accepted_cook), "SEM", stats.sem(RLAID_accepted_cook)])
csvwriter.writerow(["RLAID average accepted harvest", statistics.mean(RLAID_accepted_harvest), "stdev", statistics.stdev(RLAID_accepted_harvest), "SEM", stats.sem(RLAID_accepted_harvest)])

csvwriter.writerow(["random average accepted place", statistics.mean(random_accepted_place), "stdev", statistics.stdev(random_accepted_place), "SEM", stats.sem(random_accepted_place)])
csvwriter.writerow(["random average accepted plant", statistics.mean(random_accepted_plant), "stdev", statistics.stdev(random_accepted_plant), "SEM", stats.sem(random_accepted_plant)])
csvwriter.writerow(["random average accepted cook", statistics.mean(random_accepted_cook), "stdev", statistics.stdev(random_accepted_cook), "SEM", stats.sem(random_accepted_cook)])
csvwriter.writerow(["random average presented harvest", statistics.mean(random_accepted_harvest), "stdev", statistics.stdev(random_accepted_harvest), "SEM", stats.sem(random_accepted_harvest)])

passage_completed_place, passage_completed_plant, passage_completed_cook, passage_completed_harvest = convert_quest_types_to_array(passage_completed_quest_types)
RLAID_completed_place, RLAID_completed_plant, RLAID_completed_cook, RLAID_completed_harvest = convert_quest_types_to_array(RLAID_completed_quest_types)
random_completed_place, random_completed_plant, random_completed_cook, random_completed_harvest = convert_quest_types_to_array(random_completed_quest_types)
	 
bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

passage_completed_qt_count = [statistics.mean(passage_completed_place),
							  statistics.mean(passage_completed_plant),
							  statistics.mean(passage_completed_cook),
							  statistics.mean(passage_completed_harvest)]

passage_completed_qt_stdev = [statistics.stdev(passage_completed_place),
							  statistics.stdev(passage_completed_plant),
							  statistics.stdev(passage_completed_cook),
							  statistics.stdev(passage_completed_harvest)]

RLAID_completed_qt_count = [statistics.mean(RLAID_completed_place),
							  statistics.mean(RLAID_completed_plant),
							  statistics.mean(RLAID_completed_cook),
							  statistics.mean(RLAID_completed_harvest)]

RLAID_completed_qt_stdev = [statistics.stdev(RLAID_completed_place),
							  statistics.stdev(RLAID_completed_plant),
							  statistics.stdev(RLAID_completed_cook),
							  statistics.stdev(RLAID_completed_harvest)]

random_completed_qt_count = [statistics.mean(random_completed_place),
							  statistics.mean(random_completed_plant),
							  statistics.mean(random_completed_cook),
							  statistics.mean(random_completed_harvest)]

random_completed_qt_stdev = [statistics.stdev(random_completed_place),
							  statistics.stdev(random_completed_plant),
							  statistics.stdev(random_completed_cook),
							  statistics.stdev(random_completed_harvest)]


br1 = np.arange(len(passage_completed_qt_count))
br2 = [x + bar_width for x in br1]
br3 = [x + bar_width for x in br2]

plt.bar(br1, passage_completed_qt_count, width = bar_width, yerr=passage_completed_qt_stdev, label = 'PaSSAGE')
plt.bar(br2, RLAID_completed_qt_count, width = bar_width,yerr=RLAID_completed_qt_stdev, label = 'RLAID')
plt.bar(br3, random_completed_qt_count, width = bar_width, yerr=random_completed_qt_stdev, label = 'Random')

plt.title('Per player average completed quest types', fontweight = 'bold', fontsize = 15)
plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(random_completed_qt_count))], ['place', 'plant', 'cook', 'harvest'])

plt.legend()
plt.savefig('quests/per_player_average_completed_quest_types.png', bbox_inches='tight')

csvwriter.writerow(["passage average completed place", statistics.mean(passage_completed_place), "stdev", statistics.stdev(passage_completed_place), "SEM", stats.sem(passage_completed_place)])
csvwriter.writerow(["passage average completed plant", statistics.mean(passage_completed_plant), "stdev", statistics.stdev(passage_completed_plant), "SEM", stats.sem(passage_completed_plant)])
csvwriter.writerow(["passage average completed cook", statistics.mean(passage_completed_cook), "stdev", statistics.stdev(passage_completed_cook), "SEM", stats.sem(passage_completed_cook)])
csvwriter.writerow(["passage average completed harvest", statistics.mean(passage_completed_harvest), "stdev", statistics.stdev(passage_completed_harvest), "SEM", stats.sem(passage_completed_harvest)])

csvwriter.writerow(["RLAID average completed place", statistics.mean(RLAID_completed_place), "stdev", statistics.stdev(RLAID_completed_place), "SEM", stats.sem(RLAID_completed_place)])
csvwriter.writerow(["RLAID average completed plant", statistics.mean(RLAID_completed_plant), "stdev", statistics.stdev(RLAID_completed_plant), "SEM", stats.sem(RLAID_completed_plant)])
csvwriter.writerow(["RLAID average completed cook", statistics.mean(RLAID_completed_cook), "stdev", statistics.stdev(RLAID_completed_cook), "SEM", stats.sem(RLAID_completed_cook)])
csvwriter.writerow(["RLAID average completed harvest", statistics.mean(RLAID_completed_harvest), "stdev", statistics.stdev(RLAID_completed_harvest), "SEM", stats.sem(RLAID_completed_harvest)])

csvwriter.writerow(["random average completed place", statistics.mean(random_completed_place), "stdev", statistics.stdev(random_completed_place), "SEM", stats.sem(random_completed_place)])
csvwriter.writerow(["random average completed plant", statistics.mean(random_completed_plant), "stdev", statistics.stdev(random_completed_plant), "SEM", stats.sem(random_completed_plant)])
csvwriter.writerow(["random average completed cook", statistics.mean(random_completed_cook), "stdev", statistics.stdev(random_completed_cook), "SEM", stats.sem(random_completed_cook)])
csvwriter.writerow(["random average completed harvest", statistics.mean(random_completed_harvest), "stdev", statistics.stdev(random_completed_harvest), "SEM", stats.sem(random_completed_harvest)])



print("passage total quests " + str(passage_total_quests))
print("passage accepted quests " + str(passage_accepted_quests))
print("passage completed quests " + str(passage_completed_quests))
print("RLAID total quests " + str(RLAID_total_quests))
print("RLAID accepted quests " + str(RLAID_accepted_quests))
print("RLAID completeed quests" + str(RLAID_completed_quests))
print("random total quests " + str(random_total_quests))
print("random accepted quests " + str(random_accepted_quests))
print("random accepted quests " + str (random_completed_quests))

#get acceptance and completancen rate of each player

passage_session_1_presented_quests, passage_session_1_accepted_quests, passage_session_1_completed_quests, passage_session_1_acceptance_rate, passage_session_1_completance_rate = get_quest_accept_complete_present_single_session(session_1_passage, 1)
passage_session_2_presented_quests, passage_session_2_accepted_quests, passage_session_2_completed_quests, passage_session_2_acceptance_rate, passage_session_2_completance_rate = get_quest_accept_complete_present_single_session(session_2_passage, 2)
RLAID_session_1_presented_quests, RLAID_session_1_accepted_quests, RLAID_session_1_completed_quests, RLAID_session_1_acceptance_rate, RLAID_session_1_completance_rate = get_quest_accept_complete_present_single_session(session_1_RLAID, 1)
RLAID_session_2_presented_quests, RLAID_session_2_accepted_quests, RLAID_session_2_completed_quests, RLAID_session_2_acceptance_rate, RLAID_session_2_completance_rate = get_quest_accept_complete_present_single_session(session_2_RLAID, 2)
random_session_1_presented_quests, random_session_1_accepted_quests, random_session_1_completed_quests, random_session_1_acceptance_rate, random_session_1_completance_rate = get_quest_accept_complete_present_single_session(session_1_random, 1)
random_session_2_presented_quests, random_session_2_accepted_quests, random_session_2_completed_quests, random_session_2_acceptance_rate, random_session_2_completance_rate = get_quest_accept_complete_present_single_session(session_2_random, 2)

csvwriter.writerow(["passage session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(passage_session_1_presented_quests, passage_session_2_presented_quests)])
print("passage session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(passage_session_1_presented_quests, passage_session_2_presented_quests))
csvwriter.writerow(["passage session 1 vs 2 accepted quests kruskal test", scipy.stats.kruskal(passage_session_1_accepted_quests, passage_session_2_accepted_quests)])
print("passage session 1 vs 2 accepted quests kruskal test")
print(scipy.stats.kruskal(passage_session_1_accepted_quests, passage_session_2_accepted_quests))
csvwriter.writerow(["passage session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(passage_session_1_presented_quests, passage_session_2_presented_quests)])
print("passage session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(passage_session_1_presented_quests, passage_session_2_presented_quests))
csvwriter.writerow(["passage session 1 vs 2 acceptance rate kruskal test", scipy.stats.kruskal(passage_session_1_acceptance_rate, passage_session_2_acceptance_rate)])
print("passage session 1 vs 2 acceptance rate kruskal test")
print(scipy.stats.kruskal(passage_session_1_acceptance_rate, passage_session_2_acceptance_rate))
csvwriter.writerow(["passage session 1 vs 2 completance rate kruskal test", scipy.stats.kruskal(passage_session_1_completance_rate, passage_session_2_completance_rate)])
print("passage session 1 vs 2 completance rate kruskal test")
print(scipy.stats.kruskal(passage_session_1_completance_rate, passage_session_2_completance_rate))

csvwriter.writerow(["RLAID session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(RLAID_session_1_presented_quests, RLAID_session_2_presented_quests)])
print("RLAID session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(RLAID_session_1_presented_quests, RLAID_session_2_presented_quests))
csvwriter.writerow(["RLAID session 1 vs 2 accepted quests kruskal test", scipy.stats.kruskal(RLAID_session_1_accepted_quests, RLAID_session_2_accepted_quests)])
print("RLAID session 1 vs 2 accepted quests kruskal test")
print(scipy.stats.kruskal(RLAID_session_1_accepted_quests, RLAID_session_2_accepted_quests))
csvwriter.writerow(["RLAID session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(RLAID_session_1_presented_quests, RLAID_session_2_presented_quests)])
print("RLAID session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(RLAID_session_1_presented_quests, RLAID_session_2_presented_quests))
csvwriter.writerow(["RLAID session 1 vs 2 acceptance rate kruskal test", scipy.stats.kruskal(RLAID_session_1_acceptance_rate, RLAID_session_2_acceptance_rate)])
print("RLAID session 1 vs 2 acceptance rate kruskal test")
print(scipy.stats.kruskal(RLAID_session_1_acceptance_rate, RLAID_session_2_acceptance_rate))
csvwriter.writerow(["RLAID session 1 vs 2 completance rate kruskal test", scipy.stats.kruskal(RLAID_session_1_completance_rate, RLAID_session_2_completance_rate)])
print("RLAID session 1 vs 2 completance rate kruskal test")
print(scipy.stats.kruskal(RLAID_session_1_completance_rate, RLAID_session_2_completance_rate))

csvwriter.writerow(["random session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(random_session_1_presented_quests, random_session_2_presented_quests)])
print("random session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(random_session_1_presented_quests, random_session_2_presented_quests))
csvwriter.writerow(["random session 1 vs 2 accepted quests kruskal test", scipy.stats.kruskal(random_session_1_accepted_quests, random_session_2_accepted_quests)])
print("random session 1 vs 2 accepted quests kruskal test")
print(scipy.stats.kruskal(random_session_1_accepted_quests, random_session_2_accepted_quests))
csvwriter.writerow(["random session 1 vs 2 presented quests kruskal test", scipy.stats.kruskal(random_session_1_presented_quests, random_session_2_presented_quests)])
print("random session 1 vs 2 presented quests kruskal test")
print(scipy.stats.kruskal(random_session_1_presented_quests, random_session_2_presented_quests))
csvwriter.writerow(["random session 1 vs 2 acceptance rate kruskal test", scipy.stats.kruskal(random_session_1_acceptance_rate, random_session_2_acceptance_rate)])
print("random session 1 vs 2 acceptance rate kruskal test")
print(scipy.stats.kruskal(random_session_1_acceptance_rate, random_session_2_acceptance_rate))
csvwriter.writerow(["random session 1 vs 2 completance rate kruskal test", scipy.stats.kruskal(random_session_1_completance_rate, random_session_2_completance_rate)])
print("random session 1 vs 2 completance rate kruskal test")
print(scipy.stats.kruskal(random_session_1_completance_rate, random_session_2_completance_rate))


passage_presented_quests, passage_accepted_quests, passage_completed_quests, passage_acceptance_rate, passage_completance_rate = get_quest_accept_complete_present(session_1_passage, session_2_passage)
RLAID_presented_quests, RLAID_accepted_quests, RLAID_completed_quests, RLAID_acceptance_rate, RLAID_completance_rate = get_quest_accept_complete_present(session_1_RLAID, session_2_RLAID)
random_presented_quests, random_accepted_quests, random_completed_quests, random_acceptance_rate, random_completance_rate = get_quest_accept_complete_present(session_1_random, session_2_random)

fig = plt.subplots(figsize=(12,8))
plt.title("Presented Quests")
ax = plt.subplot(111)
ax.boxplot([passage_presented_quests, RLAID_presented_quests, random_presented_quests])
ax.set_xticklabels(["PaSSAGE", "CMAB", "Random"])
ax.set_xlabel("AI Director")
ax.set_ylabel('Quests')
plt.savefig('quests/boxplot_presented_quests.png', bbox_inches='tight')

fig = plt.subplots(figsize=(12,8))
plt.title("Accepted Quests")
ax = plt.subplot(111)
ax.boxplot([passage_accepted_quests, RLAID_accepted_quests, random_accepted_quests])
ax.set_xticklabels(["PaSSAGE", "CMAB", "Random"])
ax.set_xlabel("AI Director")
ax.set_ylabel('Quests')
plt.savefig('quests/boxplot_accepted_quests.png', bbox_inches='tight')

fig = plt.subplots(figsize=(12,8))
plt.scatter(passage_presented_quests, passage_accepted_quests)
plt.title("Presented vs Accepted Quests Passage")
plt.xlabel("presented quests")
plt.ylabel("accepted quests")
plt.savefig('quests/scatter_passage_quests.png', bbox_inches='tight')

fig = plt.subplots(figsize=(12,8))
plt.scatter(RLAID_presented_quests, RLAID_accepted_quests)
plt.title("Presented vs Accepted Quests CMAB")
plt.xlabel("presented quests")
plt.ylabel("accepted quests")
plt.savefig('quests/scatter_cmab_quests.png', bbox_inches='tight')

fig = plt.subplots(figsize=(12,8))
plt.scatter(random_presented_quests, random_accepted_quests)
plt.title("Presented vs Accepted Quests Random")
plt.xlabel("presented quests")
plt.ylabel("accepted quests")
plt.savefig('quests/scatter_random_quests.png', bbox_inches='tight')

passage_res = scipy.stats.linregress(passage_presented_quests, passage_accepted_quests)
print(f"Passage Std error lin regression: {passage_res.rvalue**2:.6f}")

RLAID_res = scipy.stats.linregress(RLAID_presented_quests, RLAID_accepted_quests)
print(f"CMAB Std error lin regression: {RLAID_res.rvalue**2:.6f}")

random_res = scipy.stats.linregress(random_presented_quests, random_accepted_quests)
print(f"Random Std error lin regression: {random_res.rvalue**2:.6f}")

passage_fit = np.polyfit(np.log(passage_presented_quests), passage_accepted_quests, 1)
print(passage_fit)


print("passage average presented quests " + str(statistics.mean(passage_presented_quests)))
print("stdev " + str(statistics.stdev(passage_presented_quests)))
print("sem " + str(stats.sem(passage_presented_quests)))
print("passage average accepted quests " + str(statistics.mean(passage_accepted_quests)))
print("stdev " + str(statistics.stdev(passage_accepted_quests)))
print("sem " + str(stats.sem(passage_accepted_quests)))
print("passage average completed quests " + str(statistics.mean(passage_completed_quests)))
print("stdev " + str(statistics.stdev(passage_completed_quests)))
print("sem " + str(stats.sem(passage_completed_quests)))
print("passage average acceptance rate " + str(statistics.mean(passage_acceptance_rate)))
print("stdev " + str(statistics.stdev(passage_acceptance_rate)))
print("sem " + str(stats.sem(passage_acceptance_rate)))
print("passage average completance rate " + str(statistics.mean(passage_completance_rate)))
print("stdev " + str(statistics.stdev(passage_completance_rate)))
print("sem " + str(stats.sem(passage_completance_rate)))

print("RLAID average presented quests " + str(statistics.mean(RLAID_presented_quests)))
print("stdev " + str(statistics.stdev(RLAID_presented_quests)))
print("sem " + str(stats.sem(RLAID_presented_quests)))
print("RLAID average accepted quests " + str(statistics.mean(RLAID_accepted_quests)))
print("stdev " + str(statistics.stdev(RLAID_accepted_quests)))
print("sem " + str(stats.sem(RLAID_accepted_quests)))
print("RLAID average completed quests " + str(statistics.mean(RLAID_completed_quests)))
print("stdev " + str(statistics.stdev(RLAID_completed_quests)))
print("sem " + str(stats.sem(RLAID_completed_quests)))
print("RLAID average acceptance rate " + str(statistics.mean(RLAID_acceptance_rate)))
print("stdev " + str(statistics.stdev(RLAID_acceptance_rate)))
print("sem " + str(stats.sem(RLAID_acceptance_rate)))
print("RLAID average completance rate " + str(statistics.mean(RLAID_completance_rate)))
print("stdev " + str(statistics.stdev(RLAID_completance_rate)))
print("sem " + str(stats.sem(RLAID_completance_rate)))

print("random average presented quests " + str(statistics.mean(random_presented_quests)))
print("stdev " + str(statistics.stdev(random_presented_quests)))
print("sem " + str(stats.sem(random_presented_quests)))
print("random average accepted quests " + str(statistics.mean(random_accepted_quests)))
print("stdev " + str(statistics.stdev(random_accepted_quests)))
print("sem " + str(stats.sem(random_accepted_quests)))
print("random average completed quests " + str(statistics.mean(random_completed_quests)))
print("stdev " + str(statistics.stdev(random_completed_quests)))
print("sem " + str(stats.sem(random_completed_quests)))
print("random average acceptance rate " + str(statistics.mean(random_acceptance_rate)))
print("stdev " + str(statistics.stdev(random_acceptance_rate)))
print("sem " + str(stats.sem(random_acceptance_rate)))
print("random average completance rate " + str(statistics.mean(random_completance_rate)))
print("stdev " + str(statistics.stdev(random_completance_rate)))
print("sem " + str(stats.sem(random_completance_rate)))

print("Passage vs RLAID presented " + str(scipy.stats.mannwhitneyu(passage_presented_quests, RLAID_presented_quests)))
print("random vs RLAID presented " + str(scipy.stats.mannwhitneyu(random_presented_quests, RLAID_presented_quests)))
print("Passage vs random presented " + str(scipy.stats.mannwhitneyu(passage_presented_quests, random_presented_quests)))

print("Passage vs RLAID accepted quests " + str(scipy.stats.mannwhitneyu(passage_accepted_quests, RLAID_accepted_quests)))
print("random vs RLAID accepted quests " + str(scipy.stats.mannwhitneyu(random_accepted_quests, RLAID_accepted_quests)))
print("Passage vs random accepted quests " + str(scipy.stats.mannwhitneyu(passage_accepted_quests, random_accepted_quests)))

print("Passage vs RLAID completed quests " + str(scipy.stats.mannwhitneyu(passage_completed_quests, RLAID_completed_quests)))
print("random vs RLAID completed quests " + str(scipy.stats.mannwhitneyu(random_completed_quests, RLAID_completed_quests)))
print("Passage vs random completed quests " + str(scipy.stats.mannwhitneyu(passage_completed_quests, random_completed_quests)))

print("Passage vs RLAID acceptance " + str(scipy.stats.mannwhitneyu(passage_acceptance_rate, RLAID_acceptance_rate)))
print("random vs RLAID acceptance " + str(scipy.stats.mannwhitneyu(random_acceptance_rate, RLAID_acceptance_rate)))
print("Passage vs random acceptance " + str(scipy.stats.mannwhitneyu(passage_acceptance_rate, random_acceptance_rate)))

print("Passage vs RLAID completance " + str(scipy.stats.mannwhitneyu(passage_completance_rate, RLAID_completance_rate)))
print("random vs RLAID completance " + str(scipy.stats.mannwhitneyu(random_completance_rate, RLAID_completance_rate)))
print("Passage vs random completance " + str(scipy.stats.mannwhitneyu(passage_completance_rate, random_completance_rate)))




print("passage then random " + str(len(passage_then_random_keys)))
print("passage then RLAID " + str(len(passage_then_RLAID_keys)))
print("RLAID then passage " + str(len(RLAID_then_passage_keys)))
print("RLAID then random " + str(len(RLAID_then_random_keys)))
print("random then passage " + str(len(random_then_passage_keys)))
print("random then RLAID " + str(len(random_then_RLAID_keys)))


passage_then_random = get_comparison_survey_accross_keys(passage_then_random_keys)
passage_then_RLAID = get_comparison_survey_accross_keys(passage_then_RLAID_keys)
RLAID_then_passage = get_comparison_survey_accross_keys(RLAID_then_passage_keys)
RLAID_then_random = get_comparison_survey_accross_keys(RLAID_then_random_keys)
random_then_passage = get_comparison_survey_accross_keys(random_then_passage_keys)
random_then_RLAID = get_comparison_survey_accross_keys(random_then_RLAID_keys)


print("Passage vs random Passage session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(passage_then_random["first_experience"], random_then_passage["second_experience"]))
print("Passage vs random Passage session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(passage_then_random["first_complete"], random_then_passage["second_complete"]))
print("Passage vs random Passage session 1 vs 2 kruskal test fun")
print(scipy.stats.kruskal(passage_then_random["first_fun"], random_then_passage["second_fun"]))
print("Passage vs random random session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(passage_then_random["second_experience"], random_then_passage["first_experience"]))
print("Passage vs random random session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(passage_then_random["second_complete"], random_then_passage["first_complete"]))
print("Passage vs random random session 1 vs 2 v test fun")
print(scipy.stats.kruskal(passage_then_random["second_fun"], random_then_passage["first_fun"]))

print("Passage vs RLAID Passage session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(passage_then_RLAID["first_experience"], RLAID_then_passage["second_experience"]))
print("Passage vs RLAID Passage session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(passage_then_RLAID["first_complete"], RLAID_then_passage["second_complete"]))
print("Passage vs RLAID Passage session 1 vs 2 kruskal test fun")
print(scipy.stats.kruskal(passage_then_RLAID["first_fun"], RLAID_then_passage["second_fun"]))
print("Passage vs RLAID RLAID session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(passage_then_RLAID["second_experience"], RLAID_then_passage["first_experience"]))
print("Passage vs RLAID RLAID session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(passage_then_RLAID["second_complete"], RLAID_then_passage["first_complete"]))
print("Passage vs RLAID RLAID session 1 vs 2 kruskal test fun")
print(scipy.stats.kruskal(passage_then_RLAID["second_fun"], RLAID_then_passage["first_fun"]))

print("random vs RLAID RLAID session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(RLAID_then_random["first_experience"], random_then_RLAID["second_experience"]))
print("random vs RLAID RLAID session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(RLAID_then_random["first_complete"], random_then_RLAID["second_complete"]))
print("random vs RLAID RLAID session 1 vs 2 kruskal test fun")
print(scipy.stats.kruskal(RLAID_then_random["first_fun"], random_then_RLAID["second_fun"]))
print("random vs RLAID random session 1 vs 2 kruskal test experience")
print(scipy.stats.kruskal(RLAID_then_random["second_experience"], random_then_RLAID["first_experience"]))
print("random vs RLAID random session 1 vs 2 kruskal test complete")
print(scipy.stats.kruskal(RLAID_then_random["second_complete"], random_then_RLAID["first_complete"]))
print("random vs RLAID random session 1 vs 2 kruskal test fun")
print(scipy.stats.kruskal(RLAID_then_random["second_fun"], random_then_RLAID["first_fun"]))

passage_vs_random = {}
passage_vs_random["passage_experience"] = passage_then_random["first_experience"] + random_then_passage["second_experience"]
passage_vs_random["random_experience"] = passage_then_random["second_experience"] + random_then_passage["first_experience"]
passage_vs_random["passage_complete"] =  passage_then_random["first_complete"] + random_then_passage["second_complete"]
passage_vs_random["random_complete"] = passage_then_random["second_complete"] + random_then_passage["first_complete"]
passage_vs_random["passage_fun"] =  passage_then_random["first_fun"] + random_then_passage["second_fun"]
passage_vs_random["random_fun"] = passage_then_random["second_fun"] + random_then_passage["first_fun"]

print("random vs passage comparison results")
print(passage_vs_random)

passage_vs_RLAID = {}
passage_vs_RLAID["passage_experience"] = passage_then_RLAID["first_experience"] + RLAID_then_passage["second_experience"]
passage_vs_RLAID["RLAID_experience"] = passage_then_RLAID["second_experience"] + RLAID_then_passage["first_experience"]
passage_vs_RLAID["passage_complete"] =  passage_then_RLAID["first_complete"] + RLAID_then_passage["second_complete"]
passage_vs_RLAID["RLAID_complete"] = passage_then_RLAID["second_complete"] + RLAID_then_passage["first_complete"]
passage_vs_RLAID["passage_fun"] =  passage_then_RLAID["first_fun"] + RLAID_then_passage["second_fun"]
passage_vs_RLAID["RLAID_fun"] = passage_then_RLAID["second_fun"] + RLAID_then_passage["first_fun"]

print("random vs RLAID comparison results")
print(passage_vs_RLAID)

RLAID_vs_random = {}
RLAID_vs_random["RLAID_experience"] = RLAID_then_random["first_experience"] + random_then_RLAID["second_experience"]
RLAID_vs_random["random_experience"] = RLAID_then_random["second_experience"] + random_then_RLAID["first_experience"]
RLAID_vs_random["RLAID_complete"] =  RLAID_then_random["first_complete"] + random_then_RLAID["second_complete"]
RLAID_vs_random["random_complete"] = RLAID_then_random["second_complete"] + random_then_RLAID["first_complete"]
RLAID_vs_random["RLAID_fun"] =  RLAID_then_random["first_fun"] + random_then_RLAID["second_fun"]
RLAID_vs_random["random_fun"] = RLAID_then_random["second_fun"] + random_then_RLAID["first_fun"]

print("random vs RLAID comparison results")
print(RLAID_vs_random)

pvr_passage_means = [statistics.mean(passage_vs_random["passage_experience"]), 
						   statistics.mean(passage_vs_random["passage_complete"]), 
						   statistics.mean(passage_vs_random["passage_fun"]), 
						   ]

pvr_passage_stdev = [statistics.stdev(passage_vs_random["passage_experience"]), 
						   statistics.stdev(passage_vs_random["passage_complete"]), 
						   statistics.stdev(passage_vs_random["passage_fun"]), 
						   ]

pvr_random_means = [statistics.mean(passage_vs_random["random_experience"]),
						   statistics.mean(passage_vs_random["random_complete"]), 
						   statistics.mean(passage_vs_random["random_fun"]),
						   ]

pvr_random_stdev = [statistics.stdev(passage_vs_random["random_experience"]),
						   statistics.stdev(passage_vs_random["random_complete"]), 
						   statistics.stdev(passage_vs_random["random_fun"]),
						   ]
fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(pvr_passage_means))
br2 = [x + bar_width for x in br1]

plt.bar(br1, pvr_passage_means, width = bar_width, yerr=pvr_passage_stdev, label = 'PaSSAGE')
plt.bar(br2, pvr_random_means, width = bar_width, yerr=pvr_random_stdev, label = 'Random')

plt.title('Passage vs Random Direct Comparison', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(pvr_passage_means))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/passage_vs_random_mean.png', bbox_inches='tight')

print("Passage vs random experience " + str(scipy.stats.mannwhitneyu(passage_vs_random["passage_experience"], passage_vs_random["random_experience"])))
print("Passage vs random complete " + str(scipy.stats.mannwhitneyu(passage_vs_random["passage_complete"], passage_vs_random["random_complete"])))
print("Passage vs random fun " + str(scipy.stats.mannwhitneyu(passage_vs_random["passage_fun"], passage_vs_random["random_fun"])))

pvr_passage_medians = [statistics.median(passage_vs_random["passage_experience"]), 
						   statistics.median(passage_vs_random["passage_complete"]), 
						   statistics.median(passage_vs_random["passage_fun"]), 
						   ]

pvr_random_medians = [statistics.median(passage_vs_random["random_experience"]),
						   statistics.median(passage_vs_random["random_complete"]), 
						   statistics.median(passage_vs_random["random_fun"]),
						   ]

fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(pvr_passage_medians))
br2 = [x + bar_width for x in br1]

plt.bar(br1, pvr_passage_medians, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, pvr_random_medians, width = bar_width, label = 'Random')

plt.title('Passage vs Random Direct Comparison Median', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Median Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(pvr_passage_means))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/passage_vs_random_median.png', bbox_inches='tight')


pvR_passage_means = [statistics.mean(passage_vs_RLAID["passage_experience"]), 
						   statistics.mean(passage_vs_RLAID["passage_complete"]), 
						   statistics.mean(passage_vs_RLAID["passage_fun"]), 
						   ]

pvR_passage_stdev = [statistics.stdev(passage_vs_RLAID["passage_experience"]), 
						   statistics.stdev(passage_vs_RLAID["passage_complete"]), 
						   statistics.stdev(passage_vs_RLAID["passage_fun"]), 
						   ]

pvR_RLAID_means = [statistics.mean(passage_vs_RLAID["RLAID_experience"]),
						   statistics.mean(passage_vs_RLAID["RLAID_complete"]), 
						   statistics.mean(passage_vs_RLAID["RLAID_fun"]),
						   ]

pvR_RLAID_stdev = [statistics.stdev(passage_vs_RLAID["RLAID_experience"]),
						   statistics.stdev(passage_vs_RLAID["RLAID_complete"]), 
						   statistics.stdev(passage_vs_RLAID["RLAID_fun"]),
						   ]
fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(pvR_passage_means))
br2 = [x + bar_width for x in br1]

plt.bar(br1, pvR_passage_means, width = bar_width, yerr=pvR_passage_stdev, label = 'PaSSAGE')
plt.bar(br2, pvR_RLAID_means, width = bar_width, yerr=pvR_RLAID_stdev, label = 'Nightingale')

plt.title('Passage vs CMAB Direct Comparison', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(pvr_passage_means))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/passage_vs_RLAID_mean.png', bbox_inches='tight')

print("Passage vs RLAID experience " + str(scipy.stats.mannwhitneyu(passage_vs_RLAID["passage_experience"], passage_vs_RLAID["RLAID_experience"])))
print("Passage vs RLAID complete " + str(scipy.stats.mannwhitneyu(passage_vs_RLAID["passage_complete"], passage_vs_RLAID["RLAID_complete"])))
print("Passage vs  fun " + str(scipy.stats.mannwhitneyu(passage_vs_RLAID["passage_fun"], passage_vs_RLAID["RLAID_fun"])))

pvR_passage_median = [statistics.median(passage_vs_RLAID["passage_experience"]), 
						   statistics.median(passage_vs_RLAID["passage_complete"]), 
						   statistics.median(passage_vs_RLAID["passage_fun"]), 
						   ]

pvR_RLAID_median = [statistics.median(passage_vs_RLAID["RLAID_experience"]),
						   statistics.median(passage_vs_RLAID["RLAID_complete"]), 
						   statistics.median(passage_vs_RLAID["RLAID_fun"]),
						   ]

fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(pvR_passage_median))
br2 = [x + bar_width for x in br1]

plt.bar(br1, pvR_passage_median, width = bar_width, label = 'PaSSAGE')
plt.bar(br2, pvR_RLAID_median, width = bar_width, label = 'CMAB')

plt.title('Passage vs CMAB Direct Comparison Median', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(pvR_passage_median))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/passage_vs_RLAID_median.png', bbox_inches='tight')


rvR_random_means = [statistics.mean(RLAID_vs_random["random_experience"]), 
						   statistics.mean(RLAID_vs_random["random_complete"]), 
						   statistics.mean(RLAID_vs_random["random_fun"]), 
						   ]

rvR_random_stdev = [statistics.stdev(RLAID_vs_random["random_experience"]), 
						   statistics.stdev(RLAID_vs_random["random_complete"]), 
						   statistics.stdev(RLAID_vs_random["random_fun"]), 
						   ]

rvR_RLAID_means = [statistics.mean(RLAID_vs_random["RLAID_experience"]),
						   statistics.mean(RLAID_vs_random["RLAID_complete"]), 
						   statistics.mean(RLAID_vs_random["RLAID_fun"]),
						   ]

rvR_RLAID_stdev = [statistics.stdev(RLAID_vs_random["RLAID_experience"]),
						   statistics.stdev(RLAID_vs_random["RLAID_complete"]), 
						   statistics.stdev(RLAID_vs_random["RLAID_fun"]),
						   ]
fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(rvR_random_means))
br2 = [x + bar_width for x in br1]

plt.bar(br1, rvR_random_means, width = bar_width, yerr=rvR_random_stdev, label = 'random')
plt.bar(br2, rvR_RLAID_means, width = bar_width, yerr=rvR_RLAID_stdev, label = 'Nightingale')

plt.title('Random vs CMAB Direct Comparison', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(pvr_passage_means))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/random_vs_RLAID_mean.png', bbox_inches='tight')

print("random vs RLAID experience " + str(scipy.stats.mannwhitneyu(RLAID_vs_random["random_experience"], RLAID_vs_random["RLAID_experience"])))
print("random vs RLAID complete " + str(scipy.stats.mannwhitneyu(RLAID_vs_random["random_complete"], RLAID_vs_random["RLAID_complete"])))
print("random vs RLAID fun " + str(scipy.stats.mannwhitneyu(RLAID_vs_random["random_fun"], RLAID_vs_random["RLAID_fun"])))

rvR_random_medians = [statistics.median(RLAID_vs_random["random_experience"]), 
						   statistics.median(RLAID_vs_random["random_complete"]), 
						   statistics.median(RLAID_vs_random["random_fun"]), 
						   ]

rvR_RLAID_medians = [statistics.median(RLAID_vs_random["RLAID_experience"]),
						   statistics.median(RLAID_vs_random["RLAID_complete"]), 
						   statistics.median(RLAID_vs_random["RLAID_fun"]),
						   ]

fig = plt.subplots(figsize=(12,8))

br1 = np.arange(len(rvR_random_medians))
br2 = [x + bar_width for x in br1]

plt.bar(br1, rvR_random_medians, width = bar_width, label = 'random')
plt.bar(br2, rvR_RLAID_medians, width = bar_width, label = 'CMAB')

plt.title('Random vs CMAB Direct Comparison', fontweight = 'bold', fontsize = 15)
plt.xlabel('Survey Question', fontweight = 'bold', fontsize = 15)
plt.ylabel('Median Likert Value', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(rvR_random_medians))], ['Experience', 'Completion', 'Fun'])

plt.legend()
plt.savefig('comparison_survey/random_vs_RLAID_median.png', bbox_inches='tight')


print("Passage passage vs random experience median" + str(statistics.median(passage_vs_random["passage_experience"])))
print("Passage passage vs random complete median" + str(statistics.median(passage_vs_random["passage_complete"])))
print("Passage passage vs random fun median" + str(statistics.median(passage_vs_random["passage_fun"])))

print("random passage vs random experience median" + str(statistics.median(passage_vs_random["random_experience"])))
print("random passage vs random complete median" + str(statistics.median(passage_vs_random["random_complete"])))
print("random passage vs random fun median" + str(statistics.median(passage_vs_random["random_fun"])))

print("Passage passage vs RLAID experience median" + str(statistics.median(passage_vs_RLAID["passage_experience"])))
print("Passage passage vs RLAID complete median" + str(statistics.median(passage_vs_RLAID["passage_complete"])))
print("Passage passage vs RLAID fun median" + str(statistics.median(passage_vs_RLAID["passage_fun"])))

print("RLAID passage vs RLAID experience median" + str(statistics.median(passage_vs_RLAID["RLAID_experience"])))
print("RLAID passage vs RLAID complete median" + str(statistics.median(passage_vs_RLAID["RLAID_complete"])))
print("RLAID passage vs RLAID fun median" + str(statistics.median(passage_vs_RLAID["RLAID_fun"])))

print("random random vs RLAID experience median" + str(statistics.median(RLAID_vs_random["random_experience"])))
print("random random vs RLAID complete median" + str(statistics.median(RLAID_vs_random["random_complete"])))
print("random random vs RLAID fun median" + str(statistics.median(RLAID_vs_random["random_fun"])))

print("RLAID random vs RLAID experience median" + str(statistics.median(RLAID_vs_random["RLAID_experience"])))
print("RLAID random vs RLAID complete median" + str(statistics.median(RLAID_vs_random["RLAID_complete"])))
print("RLAID random vs RLAID fun median" + str(statistics.median(RLAID_vs_random["RLAID_fun"])))




print("Passage Passage vs Random Experience SEM " + str(scipy.stats.sem(passage_vs_random["passage_experience"])))
print("Random Passage vs Random Experience SEM " + str(scipy.stats.sem(passage_vs_random["random_experience"])))
print("Passage Passage vs Random Completion SEM " + str(scipy.stats.sem(passage_vs_random["passage_complete"])))
print("Random Passage vs Random Completion SEM " + str(scipy.stats.sem(passage_vs_random["random_complete"])))
print("Passage Passage vs Random fun SEM " + str(scipy.stats.sem(passage_vs_random["passage_fun"])))
print("Random Passage vs Random fun SEM " + str(scipy.stats.sem(passage_vs_random["random_fun"])))

print("Passage Passage vs RLAID Experience SEM " + str(scipy.stats.sem(passage_vs_RLAID["passage_experience"])))
print("RLAID Passage vs RLAID Experience SEM " + str(scipy.stats.sem(passage_vs_RLAID["RLAID_experience"])))
print("Passage Passage vs RLAID Completion SEM " + str(scipy.stats.sem(passage_vs_RLAID["passage_complete"])))
print("RLAID Passage vs RLAID Completion SEM " + str(scipy.stats.sem(passage_vs_RLAID["RLAID_complete"])))
print("Passage Passage vs RLAID fun SEM " + str(scipy.stats.sem(passage_vs_RLAID["passage_fun"])))
print("RLAID Passage vs RLAID fun SEM " + str(scipy.stats.sem(passage_vs_RLAID["RLAID_fun"])))

print("RLAID RLAID vs Random Experience SEM " + str(scipy.stats.sem(RLAID_vs_random["RLAID_experience"])))
print("Random RLAID vs Random Experience SEM " + str(scipy.stats.sem(RLAID_vs_random["random_experience"])))
print("Passage RLAID vs Random Completion SEM " + str(scipy.stats.sem(RLAID_vs_random["RLAID_complete"])))
print("RLAID RLAID vs Random Completion SEM " + str(scipy.stats.sem(RLAID_vs_random["random_complete"])))
print("RLAID RLAID vs Random fun SEM " + str(scipy.stats.sem(RLAID_vs_random["RLAID_fun"])))
print("Random RLAID vs Random fun SEM " + str(scipy.stats.sem(RLAID_vs_random["random_fun"])))


'''
passage_then_random = get_comparison_survey_accross_keys(passage_then_random_keys)
passage_then_RLAID = get_comparison_survey_accross_keys(passage_then_RLAID_keys)
RLAID_then_passage = get_comparison_survey_accross_keys(RLAID_then_passage_keys)
RLAID_then_random = get_comparison_survey_accross_keys(RLAID_then_random_keys)
random_then_passage = get_comparison_survey_accross_keys(random_then_passage_keys)
random_then_RLAID = get_comparison_survey_accross_keys(random_then_RLAID_keys)
'''

#short answer questions
print("passage then random fav activity ") 
print(passage_then_random["fav_activity"])
print("passage then RLAID fav activity ") 
print( passage_then_RLAID["fav_activity"])
print("RLAID then passage fav activity ") 
print(RLAID_then_passage["fav_activity"])
print("RLAID then random fav activity ") 
print(RLAID_then_random["fav_activity"])
print("random then passage fav activity ") 
print(random_then_passage["fav_activity"])
print("random then RLAID fav activity ") 
print(random_then_RLAID["fav_activity"])

print("passage then random difference ") 
print(passage_then_random["difference"])
print("passage then RLAID difference ") 
print(passage_then_RLAID["difference"])
print("RLAID then passage difference ")
print(RLAID_then_passage["difference"]) 
print("RLAID then random difference ") 
print(RLAID_then_random["difference"])
print("random then passage difference ") 
print(random_then_passage["difference"])
print("random then RLAID difference ")
print(random_then_RLAID["difference"]) 


csvfile.close()