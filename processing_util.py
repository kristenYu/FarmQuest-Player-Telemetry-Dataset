import json

#create one json object to read in on the file
def process_json_bulk(): 
	processed_f = open("processed.json", 'w');

	with open('unprocessed.json','r') as file: 
		for line in file:
			if line == "}{\n":

				processed_f.write(",")
			else:
				processed_f.write(line)

	processed_f.close();


#Returns the dictionary of the json that have complete data
def get_only_complete_data(debug): 
	f = open('processed.json', 'r')
	data = json.load(f)
	f.close()

	complete_data = {}
	counter = 0
	for key in data.keys():
		#check if any of the data is empty 
		if data[key]["demographic_data"] == "":
			counter += 1
			continue
		elif data[key]["short_survey_1_data"] == "":
			counter += 1
			continue
		elif data[key]["short_survey_2_data"] == "":
			counter += 1
			continue
		elif data[key]["comparison_data"] == "":
			counter += 1
			continue
		elif data[key]["telemetry_data"] == "":
			counter += 1
			continue
		else:
			complete_data[key] = data[key]
	if(debug):
		print(counter)
		print(len(complete_data))
	return complete_data


def get_valid_keys(data):
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

	valid_keys = data.keys() - excluded_keys
	return valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys


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
		session_telemetry["tutorial"] = complete_telemetry[1:session_locations[2]]
		session_telemetry["session_1"] = complete_telemetry[session_locations[2]:session_locations[3]]
		session_telemetry["session_2"] = complete_telemetry[session_locations[3]:]
	return session_telemetry

def get_small_player_feature_vector(keys, session_num, data):
	feature_data = []
	for key in keys:
		player_features = [0 for x in range(0,4)]
		telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"));
		for t in telemetry[f"session_{session_num}"]: 
			if "Interaction:Plant" in t:
				player_features[0] += 1
			elif "Interaction:Cook" in t:
				player_features[1] += 1
			elif "Interaction:HarvestMushroom" in t:
				player_features[2] += 1
			elif "Interaction:HarvestBerry" in t:
				player_features[2] += 1
			elif "Interaction:Place" in t:
				player_features[3] += 1
		feature_data.append(player_features)
	return feature_data

def get_large_player_feature_vector(keys, session_num, data):
	feature_data = []
	for key in keys:
		player_features = [0 for x in range(0,12)]
		telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"));
		for t in telemetry[f"session_{session_num}"]: 
			if "Interaction:Plant" in t:
				player_features[0] += 1
			elif "Interaction:Cook" in t:
				player_features[1] += 1
			elif "Interaction:HarvestMushroom" in t:
				player_features[2] += 1
			elif "Interaction:HarvestBerry" in t:
				player_features[2] += 1
			elif "Interaction:Place" in t:
				player_features[3] += 1
			elif "Shop:Bought" in t:
				player_features[4] += 1
			elif "Shop:Sold" in t:
				player_features[5] += 1
			elif "Interaction:HarvestCrop" in t:
				player_features[6] += 1
			elif "RotateFurniture" in t:
				player_features[7] += 1
			elif "PickupFurniture" in t:
				player_features[8] += 1
			elif "Shop:TriedBought" in t:
				player_features[9] += 1
			elif "Transition" in t:
				player_features[10] += 1
			elif "Shop:Pay" in t:
				player_features[11] += 1
		feature_data.append(player_features)
	return feature_data


def process_short_survey(survey_data):
	short_survey_structure_dictionary = {"short_survey": 0, "pos_accept":1, "neg_accept":2, "pos_complete":3, "neg_complete":4, "variety":5, "pos_enjoy":6, "neg_enjoy":7, "pos_recommend":8, "neg_recommend":9}
	short_survey = {}
	split_data = survey_data.split('\n')
	short_survey["pos_accept"] = int(split_data[short_survey_structure_dictionary["pos_accept"]].split(":")[-1])
	short_survey["neg_accept"] = int(split_data[short_survey_structure_dictionary["neg_accept"]].split(":")[-1])
	if(split_data[short_survey_structure_dictionary["pos_complete"]].split(":")[-1] == ''):
		short_survey["pos_complete"] = -1
	else:
		short_survey["pos_complete"] = int(split_data[short_survey_structure_dictionary["pos_complete"]].split(":")[-1])
	short_survey["neg_complete"] = int(split_data[short_survey_structure_dictionary["neg_complete"]].split(":")[-1])
	if(split_data[short_survey_structure_dictionary["variety"]].split(":")[-1] == ''):
		short_survey["variety"] = -1
	else:
		short_survey["variety"] = int(split_data[short_survey_structure_dictionary["variety"]].split(":")[-1])
	if(split_data[short_survey_structure_dictionary["pos_enjoy"]].split(":")[-1] == ''):
		short_survey["pos_enjoy"] = -1
	else:
		short_survey["pos_enjoy"] = int(split_data[short_survey_structure_dictionary["pos_enjoy"]].split(":")[-1])
	short_survey["neg_enjoy"] = int(split_data[short_survey_structure_dictionary["neg_enjoy"]].split(":")[-1])
	short_survey["pos_recommend"] = int(split_data[short_survey_structure_dictionary["pos_recommend"]].split(":")[-1])
	short_survey["neg_recommend"] = int(split_data[short_survey_structure_dictionary["neg_recommend"]].split(":")[-1])

	return short_survey



def get_session_2_short_survey_data_accross_keys(session_2_keys, data):
	session_data = {}
	session_2_pos_accept = []
	session_2_neg_accept = []
	session_2_pos_complete = []
	session_2_neg_complete = []
	session_2_variety = []
	session_2_pos_enjoy = []
	session_2_neg_enjoy = []
	session_2_pos_recommend = []
	session_2_neg_recommend = []

	for key in session_2_keys:
		survey_2_data = process_short_survey(data[key]["short_survey_2_data"])
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

	session_data["pos_accept"] = session_2_pos_accept
	session_data["neg_accept"] = session_2_neg_accept
	session_data["pos_complete"] = session_2_pos_complete
	session_data["neg_complete"] = session_2_neg_complete
	session_data["variety"] = session_2_variety
	session_data["pos_enjoy"] = session_2_pos_enjoy
	session_data["neg_enjoy"] = session_2_neg_enjoy
	session_data["pos_recommend"] = session_2_pos_recommend
	session_data["neg_recommend"] = session_2_neg_recommend

	return session_data


def get_session_1_short_survey_data_accross_keys(session_1_keys, data):
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

	for key in session_1_keys:
		survey_1_data = process_short_survey(data[key]["short_survey_1_data"])
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

	session_data["pos_accept"] = session_1_pos_accept
	session_data["neg_accept"] = session_1_neg_accept
	session_data["pos_complete"] = session_1_pos_complete
	session_data["neg_complete"] = session_1_neg_complete
	session_data["variety"] = session_1_variety 
	session_data["pos_enjoy"] = session_1_pos_enjoy
	session_data["neg_enjoy"] = session_1_neg_enjoy
	session_data["pos_recommend"] = session_1_pos_recommend 
	session_data["neg_recommend"] = session_1_neg_recommend

	return session_data


def get_quest_type_count_for_each_player(session_1_keys, session_2_keys, data):
	total_presented_quest_types = []
	total_accepted_quest_types = []
	total_completed_quest_types = []
	for key in session_1_keys: 
		presented_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
		accepted_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
		completed_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
		telemetry = telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:PositionQuest" in t:
				if "Place" in t:
					presented_quest_types["place"] += 1
				elif "Plant" in t:
					presented_quest_types["plant"] += 1
				elif "Cook" in t:
					presented_quest_types["cook"] += 1
				elif "Harvest" in t:
					presented_quest_types["harvest"] += 1
			if "Quest:Accept" in t:
				if "Place" in t:
					accepted_quest_types["place"] += 1
				elif "Plant" in t:
					accepted_quest_types["plant"] += 1
				elif "Cook" in t:
					accepted_quest_types["cook"] += 1
				elif "Harvest" in t:
					accepted_quest_types["harvest"] += 1
			if "Quest:Submit" in t:
				if "Place" in t:
					completed_quest_types["place"] += 1
				elif "Plant" in t:
					completed_quest_types["plant"] += 1
				elif "Cook" in t:
					completed_quest_types["cook"] += 1
				elif "Harvest" in t:
					completed_quest_types["harvest"] += 1
		total_presented_quest_types.append(presented_quest_types)
		total_accepted_quest_types.append(accepted_quest_types)
		total_completed_quest_types.append(completed_quest_types)

		for key in session_2_keys: 
			presented_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
			accepted_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
			completed_quest_types = {"place": 0, "plant": 0, "cook":0, "harvest": 0}
			telemetry = telemetry = split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
			for t in telemetry["session_2"]:
				if "Quest:PositionQuest" in t:
					if "Place" in t:
						presented_quest_types["place"] += 1
					elif "Plant" in t:
						presented_quest_types["plant"] += 1
					elif "Cook" in t:
						presented_quest_types["cook"] += 1
					elif "Harvest" in t:
						presented_quest_types["harvest"] += 1
				if "Quest:Accept" in t:
					if "Place" in t:
						accepted_quest_types["place"] += 1
					elif "Plant" in t:
						accepted_quest_types["plant"] += 1
					elif "Cook" in t:
						accepted_quest_types["cook"] += 1
					elif "Harvest" in t:
						accepted_quest_types["harvest"] += 1
				if "Quest:Submit" in t:
					if "Place" in t:
						completed_quest_types["place"] += 1
					elif "Plant" in t:
						completed_quest_types["plant"] += 1
					elif "Cook" in t:
						completed_quest_types["cook"] += 1
					elif "Harvest" in t:
						completed_quest_types["harvest"] += 1
			total_presented_quest_types.append(presented_quest_types)
			total_accepted_quest_types.append(accepted_quest_types)
			total_completed_quest_types.append(completed_quest_types)
	return total_presented_quest_types, total_accepted_quest_types, total_completed_quest_types