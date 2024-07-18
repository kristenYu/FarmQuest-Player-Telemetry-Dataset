import csv
import processing_util
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chisquare

def get_quest_type_positions(session_1_keys, session_2_keys):
	quest_type_positions = {"place_left": 0, "place_middle": 0, "place_right": 0, "plant_left":0, "plant_middle":0, "plant_right":0,
							"cook_left":0, "cook_middle":0, "cook_right":0, "harvest_left":0, "harvest_middle":0, "harvest_right":0}
	for key in session_1_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:PositionQuest" in t: 
				quest_position = t.split(":")[3].split(";")[0]
				quest_name = t.split(":")[2]
				if "Place" in quest_name:
					if quest_position == "Left":
						quest_type_positions["place_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["place_middle"]  += 1
					elif quest_position == "Right":
						quest_type_positions["place_right"]  += 1 
				if "Plant" in quest_name:
					if quest_position == "Left":
						quest_type_positions["plant_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["plant_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["plant_right"] += 1
				if "Cook" in quest_name:
					if quest_position == "Left":
						quest_type_positions["cook_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["cook_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["cook_right"] += 1
				if "Harvest" in quest_name:
					if quest_position == "Left":
						quest_type_positions["harvest_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["harvest_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["harvest_right"] += 1

	for key in session_2_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:PositionQuest" in t: 
				quest_position = t.split(":")[3].split(";")[0]
				quest_name = t.split(":")[2]
				if "Place" in quest_name:
					if quest_position == "Left":
						quest_type_positions["place_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["place_middle"]  += 1
					elif quest_position == "Right":
						quest_type_positions["place_right"]  += 1 
				if "Plant" in quest_name:
					if quest_position == "Left":
						quest_type_positions["plant_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["plant_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["plant_right"] += 1
				if "Cook" in quest_name:
					if quest_position == "Left":
						quest_type_positions["cook_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["cook_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["cook_right"] += 1
				if "Harvest" in quest_name:
					if quest_position == "Left":
						quest_type_positions["harvest_left"] += 1
					elif quest_position == "Middle":
						quest_type_positions["harvest_middle"] += 1
					elif quest_position == "Right":
						quest_type_positions["harvest_right"] += 1

	return quest_type_positions

def get_accepted_quest_positions(session_1_keys, session_2_keys):
	presented_quests = []
	accepted_quests = []
	accepted_quest_associated_index_array = []
	presented_quests_index = 0
	for key in session_1_keys: 
		start_index = 0
		telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"));
		for t in telemetry["session_1"]:
			start_index += 1
			if "Quest:PositionQuest" in t:
				presented_quests.append(t)
				presented_quests_index += 1
			elif "Quest:Accept" in t:
				#gets only the quest name from the accepted quest
				accepted_quests.append((t.split(":")[2]).split(";")[0])
				accepted_quest_associated_index_array.append(presented_quests_index-1)

	for key in session_2_keys: 
		start_index = 0
		telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"));
		for t in telemetry["session_2"]:
			start_index += 1
			if "Quest:PositionQuest" in t:
				presented_quests.append(t)
				presented_quests_index += 1
			elif "Quest:Accept" in t:
				#gets only the quest name from the accepted quest
				accepted_quests.append((t.split(":")[2]).split(";")[0])
				accepted_quest_associated_index_array.append(presented_quests_index-1)

	accepted_quest_positions = []
	for i in range(0, len(presented_quests)):
		for j in range(0, len(accepted_quest_associated_index_array)):
			if i == accepted_quest_associated_index_array[j]:
				if accepted_quests[j] in presented_quests[i-2]:
					accepted_quest_positions.append(presented_quests[i-2].split(":")[3].split(";")[0])
				elif accepted_quests[j] in presented_quests[i-1]:
					accepted_quest_positions.append(presented_quests[i-1].split(":")[3].split(";")[0])
				elif accepted_quests[j] in presented_quests[i]:
					accepted_quest_positions.append(presented_quests[i].split(":")[3].split(";")[0])

	accepted_quest_position_count = {"place_left": 0, "place_middle": 0, "place_right": 0, "plant_left":0, "plant_middle":0, "plant_right":0,
							"cook_left":0, "cook_middle":0, "cook_right":0, "harvest_left":0, "harvest_middle":0, "harvest_right":0}

	for i in range(0, len(accepted_quests)):
		if "Place" in accepted_quests[i]:
			if accepted_quest_positions[i] == "Left":
				accepted_quest_position_count["place_left"] += 1
			elif accepted_quest_positions[i] == "Middle":
				accepted_quest_position_count["place_middle"] += 1
			elif accepted_quest_positions[i] == "Right":
				accepted_quest_position_count["place_right"] += 1
		if "Plant" in accepted_quests[i]:
			if accepted_quest_positions[i] == "Left":
				accepted_quest_position_count["plant_left"] += 1
			elif accepted_quest_positions[i] == "Middle":
				accepted_quest_position_count["plant_middle"] += 1
			elif accepted_quest_positions[i] == "Right":
				accepted_quest_position_count["plant_right"] += 1
		if "Cook" in accepted_quests[i]:
			if accepted_quest_positions[i] == "Left":
				accepted_quest_position_count["cook_left"] += 1
			elif accepted_quest_positions[i] == "Middle":
				accepted_quest_position_count["cook_middle"] += 1
			elif accepted_quest_positions[i] == "Right":
				accepted_quest_position_count["cook_right"] += 1
		if "Harvest" in accepted_quests[i]:
			if accepted_quest_positions[i] == "Left":
				accepted_quest_position_count["harvest_left"] += 1
			elif accepted_quest_positions[i] == "Middle":
				accepted_quest_position_count["harvest_middle"] += 1
			elif accepted_quest_positions[i] == "Right":
				accepted_quest_position_count["harvest_right"] += 1
	return accepted_quest_position_count


def graph_presented(quest_type_positions, aid):
	bar_width = 0.25
	fig = plt.subplots(figsize=(12,8))

	qt_position_left = [quest_type_positions["plant_left"],
						quest_type_positions["place_left"],
						quest_type_positions["cook_left"],
						quest_type_positions["harvest_left"]]

	qt_position_middle = [quest_type_positions["plant_middle"],
						quest_type_positions["place_middle"],
						quest_type_positions["cook_middle"],
						quest_type_positions["harvest_middle"]]

	qt_position_right = [quest_type_positions["plant_right"],
						quest_type_positions["place_right"],
						quest_type_positions["cook_right"],
						quest_type_positions["harvest_right"]]


	br1 = np.arange(len(qt_position_left))
	br2 = [x + bar_width for x in br1]
	br3 = [x + bar_width for x in br2]

	plt.bar(br1, qt_position_left, width = bar_width, label = 'left')
	plt.bar(br2, qt_position_middle, width = bar_width, label = 'middle')
	plt.bar(br3, qt_position_right, width = bar_width, label = 'right')

	plt.title(f'{aid} Presented Quest Positions by Quest Type', fontweight = 'bold', fontsize = 15)
	plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
	plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
	plt.xticks([r+bar_width for r in range(len(qt_position_right))], ['plant', 'place', 'cook', 'harvest'])

	plt.legend()
	plt.savefig(f'salience/{aid}_presented_quests_positions_by_type.png', bbox_inches='tight')


def graph_accepted(qt_accepted_positions, aid):
	bar_width = 0.25
	fig = plt.subplots(figsize=(12,8))

	qt_position_left = [qt_accepted_positions["plant_left"],
						qt_accepted_positions["place_left"],
						qt_accepted_positions["cook_left"],
						qt_accepted_positions["harvest_left"]]

	qt_position_middle = [qt_accepted_positions["plant_middle"],
						qt_accepted_positions["place_middle"],
						qt_accepted_positions["cook_middle"],
						qt_accepted_positions["harvest_middle"]]

	qt_position_right = [qt_accepted_positions["plant_right"],
						qt_accepted_positions["place_right"],
						qt_accepted_positions["cook_right"],
						qt_accepted_positions["harvest_right"]]


	br1 = np.arange(len(qt_position_left))
	br2 = [x + bar_width for x in br1]
	br3 = [x + bar_width for x in br2]

	plt.bar(br1, qt_position_left, width = bar_width, label = 'left')
	plt.bar(br2, qt_position_middle, width = bar_width, label = 'middle')
	plt.bar(br3, qt_position_right, width = bar_width, label = 'right')

	plt.title(f'{aid} Accepted Quest Positions by Quest Type', fontweight = 'bold', fontsize = 15)
	plt.xlabel('Quest Type', fontweight = 'bold', fontsize = 15)
	plt.ylabel('Number of Quests', fontweight = 'bold', fontsize = 15)
	plt.xticks([r+bar_width for r in range(len(qt_position_right))], ['plant', 'place', 'cook', 'harvest'])

	plt.legend()
	plt.savefig(f'salience/{aid}_accepted_quests_positions_by_type.png', bbox_inches='tight')

def get_percentage_dict(qt_positions):
	percentage_dict = {"place_left": 0, "place_middle": 0, "place_right": 0, "plant_left":0, "plant_middle":0, "plant_right":0,
								"cook_left":0, "cook_middle":0, "cook_right":0, "harvest_left":0, "harvest_middle":0, "harvest_right":0}
	place_total = qt_positions["place_left"] + qt_positions["place_middle"] + qt_positions["place_right"]
	plant_total = qt_positions["plant_left"] + qt_positions["plant_middle"] + qt_positions["plant_right"]
	cook_total = qt_positions["cook_left"] + qt_positions["cook_middle"] + qt_positions["cook_right"]
	harvest_total = qt_positions["harvest_left"] + qt_positions["harvest_middle"] + qt_positions["harvest_right"]
	for key in percentage_dict.keys(): 
		if "place" in key:
			percentage_dict[key] = qt_positions[key]/place_total
		elif "plant" in key: 
			percentage_dict[key] = qt_positions[key]/plant_total
		elif "cook" in key: 
			percentage_dict[key] = qt_positions[key]/cook_total
		elif "harvest" in key: 
			percentage_dict[key] = qt_positions[key]/harvest_total
	return percentage_dict


def chisquare_contingency_analysis(quest_type_positions, qt_accepted_positions, aid, quest_type):
	presented = [quest_type_positions[f"{quest_type}_left"], quest_type_positions[f"{quest_type}_middle"], quest_type_positions[f"{quest_type}_right"]]
	accepted = [qt_accepted_positions[f"{quest_type}_left"], qt_accepted_positions[f"{quest_type}_middle"], qt_accepted_positions[f"{quest_type}_right"]]
	table = [presented, accepted]
	print(table)
	stat, p, dof, expected = chi2_contingency(table)
	print(f"p value of {aid} {quest_type}: " + str(p))




processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);
print("number of participants " + str(len(data)))

valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys = processing_util.get_valid_keys(data)
csvfile = open("salience_data.csv", "w", newline='')
csvwriter = csv.writer(csvfile)

random_quest_type_positions = get_quest_type_positions(session_1_random, session_2_random)
csvwriter.writerow(random_quest_type_positions)
print(random_quest_type_positions)
graph_presented(random_quest_type_positions, "random")
random_qt_accepted_positions = get_accepted_quest_positions(session_1_random, session_2_random)
print(random_qt_accepted_positions)
graph_accepted(random_qt_accepted_positions, "random")


passage_quest_type_positions = get_quest_type_positions(session_1_passage, session_2_passage)
csvwriter.writerow(passage_quest_type_positions)
print(passage_quest_type_positions)
graph_presented(passage_quest_type_positions, "passage")
passage_qt_accepted_positions = get_accepted_quest_positions(session_1_passage, session_2_passage)
print(passage_qt_accepted_positions)
graph_accepted(passage_qt_accepted_positions, "passage")


RLAID_quest_type_positions = get_quest_type_positions(session_1_RLAID, session_2_RLAID)
csvwriter.writerow(passage_quest_type_positions)
print(RLAID_quest_type_positions)
graph_presented(RLAID_quest_type_positions, "CMAB")
RLAID_qt_accepted_positions = get_accepted_quest_positions(session_1_RLAID, session_2_RLAID)
print(RLAID_qt_accepted_positions)
graph_accepted(RLAID_qt_accepted_positions, "CMAB")



#get percentages
random_presented_percentage_dict = get_percentage_dict(random_quest_type_positions)
random_accepted_percentage_dict = get_percentage_dict(random_qt_accepted_positions)
print("random presented percentage: " + str(random_presented_percentage_dict))
print("random accepted percentage: " + str(random_accepted_percentage_dict))
passage_presented_percentage_dict = get_percentage_dict(passage_quest_type_positions)
passage_accepted_percentage_dict = get_percentage_dict(passage_qt_accepted_positions)
print("passage presented percentage: " + str(passage_presented_percentage_dict))
print("passage accepted percentage: " + str(passage_accepted_percentage_dict))
RLAID_presented_percentage_dict = get_percentage_dict(RLAID_quest_type_positions)
RLAID_accepted_percentage_dict = get_percentage_dict(RLAID_qt_accepted_positions)
print("RLAID presented percentage: " + str(RLAID_presented_percentage_dict))
print("RLAID accepted percentage: " + str(RLAID_accepted_percentage_dict))


#chi squares analysis 
chisquare_contingency_analysis(random_quest_type_positions, random_qt_accepted_positions, "random", "place")
chisquare_contingency_analysis(random_quest_type_positions, random_qt_accepted_positions, "random", "plant")
chisquare_contingency_analysis(random_quest_type_positions, random_qt_accepted_positions, "random", "cook")
chisquare_contingency_analysis(random_quest_type_positions, random_qt_accepted_positions, "random", "harvest")

chisquare_contingency_analysis(passage_quest_type_positions, passage_qt_accepted_positions, "passage", "place")
chisquare_contingency_analysis(passage_quest_type_positions, passage_qt_accepted_positions, "passage", "plant")
chisquare_contingency_analysis(passage_quest_type_positions, passage_qt_accepted_positions, "passage", "cook")
chisquare_contingency_analysis(passage_quest_type_positions, passage_qt_accepted_positions, "passage", "harvest")

chisquare_contingency_analysis(RLAID_quest_type_positions, RLAID_qt_accepted_positions, "CMAB", "place")
chisquare_contingency_analysis(RLAID_quest_type_positions, RLAID_qt_accepted_positions, "CMAB", "plant")
chisquare_contingency_analysis(RLAID_quest_type_positions, RLAID_qt_accepted_positions, "CMAB", "cook")
chisquare_contingency_analysis(RLAID_quest_type_positions, RLAID_qt_accepted_positions, "CMAB", "harvest")