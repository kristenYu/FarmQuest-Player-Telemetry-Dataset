import processing_util
from scipy.stats import chi2_contingency
from scipy.stats import chisquare
import scipy
import matplotlib.pyplot as plt

def get_list_accepted_quests(session_1_keys, session_2_keys):
	accepted_quests = []
	for key in session_1_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:Accept" in t:
				accepted_quests.append(t.split(";")[0].split(":")[2])
	for key in session_2_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:Accept" in t:
				accepted_quests.append(t.split(";")[0].split(":")[2])
	return accepted_quests

def get_list_presented_quests(session_1_keys, session_2_keys):
	presented_quests = []
	for key in session_1_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:PositionQuest" in t:
				presented_quests.append(t.split(";")[0].split(":")[2])
	for key in session_2_keys: 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:PositionQuest" in t:
				presented_quests.append(t.split(";")[0].split(":")[2])
	return presented_quests


def get_quest_count(quest_list):
	quest_count = {"Place 7 furniture": 0, "Plant 3 lettuce": 0}
	for quest in quest_list:
		if quest in quest_count.keys():
			quest_count[quest] += 1
		else:
			quest_count[quest] = 1
	return quest_count

def chisquare_contingency_analysis(presented_quests, accepted_quests, aid, quest_type):
	if quest_type == "Harvest":
		presented = [presented_quests["Harvest 3 Berries"], presented_quests["Harvest 4 Berry"], presented_quests["Harvest 5 Berries"], presented_quests["Harvest 3 Mushroom"], presented_quests["Harvest 4 Mushroom"], presented_quests["Harvest 5 Mushroom"]]
		accepted  = [accepted_quests["Harvest 3 Berries"], accepted_quests["Harvest 4 Berry"], accepted_quests["Harvest 5 Berries"], accepted_quests["Harvest 3 Mushroom"], accepted_quests["Harvest 4 Mushroom"], accepted_quests["Harvest 5 Mushroom"]]
	if quest_type == "Place":
		presented = [presented_quests["Place 2 furniture"], presented_quests["Place 3 furniture"], presented_quests["Place 4 furniture"], presented_quests["Place 5 furniture"], presented_quests["Place 6 furniture"], presented_quests["Place 7 furniture"]]
		accepted  = [accepted_quests["Place 2 furniture"], accepted_quests["Place 3 furniture"], accepted_quests["Place 4 furniture"], accepted_quests["Place 5 furniture"], accepted_quests["Place 6 furniture"], accepted_quests["Place 7 furniture"]]
	if quest_type == "Cook":
		presented = [presented_quests["Cook 2 berry recipes"], presented_quests["Cook 2 mushroom recipes"], presented_quests["Cook 2 carrot recipes"], presented_quests["Cook 2 lettuce recipes"], presented_quests["Cook 2 green onion recipes"], presented_quests["Cook 2 onion recipes"], presented_quests["Cook 2 potato recipes"], presented_quests["Cook 2 tomato recipes"]]
		accepted = [accepted_quests["Cook 2 berry recipes"], accepted_quests["Cook 2 mushroom recipes"], accepted_quests["Cook 2 carrot recipes"], accepted_quests["Cook 2 lettuce recipes"], accepted_quests["Cook 2 green onion recipes"], accepted_quests["Cook 2 onion recipes"], accepted_quests["Cook 2 potato recipes"], accepted_quests["Cook 2 tomato recipes"]]
	if quest_type == "Plant":
		presented = [presented_quests["Plant 3 carrots"],presented_quests["Plant 3 green onions"], presented_quests["Plant 3 Lettuce"], presented_quests["Plant 3 onions"],presented_quests["Plant 3 potatoes"], presented_quests["Plant 3 tomatoes"]]
		accepted = [accepted_quests["Plant 3 carrots"],accepted_quests["Plant 3 green onions"], accepted_quests["Plant 3 Lettuce"], accepted_quests["Plant 3 onions"],accepted_quests["Plant 3 potatoes"], accepted_quests["Plant 3 tomatoes"]]
	table = [presented, accepted]
	print(table)
	stat, p, dof, expected = chi2_contingency(table)
	print(f"p value of {aid} {quest_type}: " + str(p))


def mannwhitneyutest(presented_quests, accepted_quests, aid, quest_type):
	if quest_type == "Harvest":
		presented = [presented_quests["Harvest 3 Berries"], presented_quests["Harvest 4 Berry"], presented_quests["Harvest 5 Berries"], presented_quests["Harvest 3 Mushroom"], presented_quests["Harvest 4 Mushroom"], presented_quests["Harvest 5 Mushroom"]]
		accepted  = [accepted_quests["Harvest 3 Berries"], accepted_quests["Harvest 4 Berry"], accepted_quests["Harvest 5 Berries"], accepted_quests["Harvest 3 Mushroom"], accepted_quests["Harvest 4 Mushroom"], accepted_quests["Harvest 5 Mushroom"]]
	if quest_type == "Place":
		presented = [presented_quests["Place 2 furniture"], presented_quests["Place 3 furniture"], presented_quests["Place 4 furniture"], presented_quests["Place 5 furniture"], presented_quests["Place 6 furniture"], presented_quests["Place 7 furniture"]]
		accepted  = [accepted_quests["Place 2 furniture"], accepted_quests["Place 3 furniture"], accepted_quests["Place 4 furniture"], accepted_quests["Place 5 furniture"], accepted_quests["Place 6 furniture"], accepted_quests["Place 7 furniture"]]
	if quest_type == "Cook":
		presented = [presented_quests["Cook 2 berry recipes"], presented_quests["Cook 2 mushroom recipes"], presented_quests["Cook 2 carrot recipes"], presented_quests["Cook 2 lettuce recipes"], presented_quests["Cook 2 green onion recipes"], presented_quests["Cook 2 onion recipes"], presented_quests["Cook 2 potato recipes"], presented_quests["Cook 2 tomato recipes"]]
		accepted = [accepted_quests["Cook 2 berry recipes"], accepted_quests["Cook 2 mushroom recipes"], accepted_quests["Cook 2 carrot recipes"], accepted_quests["Cook 2 lettuce recipes"], accepted_quests["Cook 2 green onion recipes"], accepted_quests["Cook 2 onion recipes"], accepted_quests["Cook 2 potato recipes"], accepted_quests["Cook 2 tomato recipes"]]
	if quest_type == "Plant":
		presented = [presented_quests["Plant 3 carrots"],presented_quests["Plant 3 green onions"], presented_quests["Plant 3 Lettuce"], presented_quests["Plant 3 onions"],presented_quests["Plant 3 potatoes"], presented_quests["Plant 3 tomatoes"]]
		accepted = [accepted_quests["Plant 3 carrots"],accepted_quests["Plant 3 green onions"], accepted_quests["Plant 3 Lettuce"], accepted_quests["Plant 3 onions"],accepted_quests["Plant 3 potatoes"], accepted_quests["Plant 3 tomatoes"]]
	p = scipy.stats.mannwhitneyu(presented, accepted)
	print(f"mann whitney u test of {aid} {quest_type}: " + str(p))


def get_presented_quests_type_by_player(session_1_keys, session_2_keys, quest_type):
	presented_quests_by_player = []
	for key in session_1_keys:
		presented_quests = []
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:PositionQuest" in t:
				if quest_type in t:
					presented_quests.append(t.split(";")[0].split(":")[2])
		presented_quests_by_player.append(presented_quests)
	for key in session_2_keys:
		presented_quests = [] 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:PositionQuest" in t:
				if quest_type in t:
					presented_quests.append(t.split(";")[0].split(":")[2])
		presented_quests_by_player.append(presented_quests)
	return presented_quests_by_player


def get_accepted_quests_type_by_player(session_1_keys, session_2_keys, quest_type):
	accepted_quests_by_player = []
	for key in session_1_keys:
		accepted_quests = []
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_1"]:
			if "Quest:Accept" in t:
				if quest_type in t:
					accepted_quests.append(t.split(";")[0].split(":")[2])
		accepted_quests_by_player.append(accepted_quests)
	for key in session_2_keys:
		accepted_quests = [] 
		telemetry = telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		for t in telemetry["session_2"]:
			if "Quest:Accept" in t:
				if quest_type in t:
					accepted_quests.append(t.split(";")[0].split(":")[2])
		accepted_quests_by_player.append(accepted_quests)
	return accepted_quests_by_player


def get_presented_accepted_quest_type_count(presented_quests, accepted_quests, quest_type):
	presented_count = []
	for player in presented_quests:
		if quest_type == "Place":
			count_dict = {"Place 2 furniture": 0, "Place 3 furniture": 0, "Place 4 furniture": 0, "Place 5 furniture": 0, "Place 6 furniture": 0, "Place 7 furniture": 0}
		for quest in player: 
			count_dict[quest] += 1
		presented_count.append(count_dict)

	accepted_count = []
	for player in accepted_quests:
		if quest_type == "Place":
			count_dict = {"Place 2 furniture": 0, "Place 3 furniture": 0, "Place 4 furniture": 0, "Place 5 furniture": 0, "Place 6 furniture": 0, "Place 7 furniture": 0}
		for quest in player: 
			count_dict[quest] += 1
		accepted_count.append(count_dict)

	return presented_count, accepted_count

def graph_presented_accepted_quest_types(presented_quest_count, accepted_quest_count, aid, quest_type): 
	plt.figure(figsize=(8, 6))
	for player in presented_quest_count:
		plt.plot(player.values(), marker='o', linestyle='-')

	plt.title(f"{aid} presented {quest_type} quests")
	plt.ylabel("Number of Quests")
	plt.xlabel("Quests")
	if quest_type == "Place":
		plt.xticks([0,1,2,3,4,5], ["Place 2 furniture", "Place 3 furniture", "Place 4 furniture", "Place 5 furniture", "Place 6 furniture", "Place 7 furniture"])
	plt.savefig(f"difficulty/{aid}_presented_{quest_type}_count.png", bbox_inches='tight')

	plt.figure(figsize=(8, 6))
	for player in accepted_quest_count:
		plt.plot(player.values(), marker='o', linestyle='-')

	plt.title(f"{aid} accepted {quest_type} quests")
	plt.ylabel("Number of Quests")
	plt.xlabel("Quests")
	if quest_type == "Place":
		plt.xticks([0,1,2,3,4,5], ["Place 2 furniture", "Place 3 furniture", "Place 4 furniture", "Place 5 furniture", "Place 6 furniture", "Place 7 furniture"])
	plt.savefig(f"difficulty/{aid}_accepted_{quest_type}_count.png", bbox_inches='tight')

	plt.figure(figsize=(8, 6))
	for i in range(0, len(presented_quest_count)):
		plt.scatter(presented_quest_count[i].values(), accepted_quest_count[i].values())

	plt.title(f"{aid} accepted vs presented {quest_type} quests")
	plt.ylabel(f"{aid} Accepted Quests")
	plt.xlabel(f"{aid} Presented Quests")
	plt.savefig(f"difficulty/{aid}_accepted_vs_presented_{quest_type}_count.png", bbox_inches='tight')






processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);
print("number of participants " + str(len(data)))

valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys = processing_util.get_valid_keys(data)

passage_accepted_quests = get_list_accepted_quests(session_1_passage, session_2_passage)
RLAID_accepted_quests = get_list_accepted_quests(session_1_RLAID, session_2_RLAID)
random_accepted_quests = get_list_accepted_quests(session_1_random, session_2_random)

passage_presented_quests = get_list_presented_quests(session_1_passage, session_2_passage)
RLAID_presented_quests = get_list_presented_quests(session_1_RLAID, session_2_RLAID)
random_presented_quests = get_list_presented_quests(session_1_random, session_2_random)


passage_accepted_quest_count = get_quest_count(passage_accepted_quests)
RLAID_accepted_quest_count = get_quest_count(RLAID_accepted_quests)
random_accepted_quest_count = get_quest_count(random_accepted_quests)

passage_presented_quest_count = get_quest_count(passage_presented_quests)
RLAID_pressented_quest_count = get_quest_count(RLAID_presented_quests)
random_presented_quest_count = get_quest_count(random_presented_quests)


chisquare_contingency_analysis(passage_accepted_quest_count, passage_presented_quest_count, "passage", "Harvest")
chisquare_contingency_analysis(RLAID_accepted_quest_count, RLAID_pressented_quest_count, "cmab", "Harvest")
chisquare_contingency_analysis(random_accepted_quest_count, random_presented_quest_count, "random", "Harvest")


chisquare_contingency_analysis(passage_accepted_quest_count, passage_presented_quest_count, "passage", "Place")
chisquare_contingency_analysis(RLAID_accepted_quest_count, RLAID_pressented_quest_count, "cmab", "Place")
chisquare_contingency_analysis(random_accepted_quest_count, random_presented_quest_count, "random", "Place")


chisquare_contingency_analysis(passage_accepted_quest_count, passage_presented_quest_count, "passage", "Cook")
chisquare_contingency_analysis(RLAID_accepted_quest_count, RLAID_pressented_quest_count, "cmab", "Cook")
chisquare_contingency_analysis(random_accepted_quest_count, random_presented_quest_count, "random", "Cook")


chisquare_contingency_analysis(passage_accepted_quest_count, passage_presented_quest_count, "passage", "Plant")
chisquare_contingency_analysis(RLAID_accepted_quest_count, RLAID_pressented_quest_count, "cmab", "Plant")
chisquare_contingency_analysis(random_accepted_quest_count, random_presented_quest_count, "random", "Plant")

#----------------------------------------
#look into passage place as a statistically significant result 
passage_presented_place_quests = get_presented_quests_type_by_player(session_1_passage, session_2_passage, "Place")
passage_accepted_place_quests = get_accepted_quests_type_by_player(session_1_passage, session_2_passage, "Place")
RLAID_presented_place_quests = get_presented_quests_type_by_player(session_1_RLAID, session_2_RLAID, "Place")
RLAID_accepted_place_quests = get_accepted_quests_type_by_player(session_1_RLAID, session_2_RLAID, "Place")
random_presented_place_quests = get_presented_quests_type_by_player(session_1_random, session_2_random, "Place")
random_accepted_place_quests = get_accepted_quests_type_by_player(session_1_random, session_2_random, "Place")

passage_presented_place_count, passage_accepted_place_count = get_presented_accepted_quest_type_count(passage_presented_place_quests, passage_accepted_place_quests, "Place")
RLAID_presented_place_count, RLAID_accepted_place_count = get_presented_accepted_quest_type_count(RLAID_presented_place_quests, RLAID_accepted_place_quests, "Place")
random_presented_place_count, random_accepted_place_count = get_presented_accepted_quest_type_count(random_presented_place_quests, random_accepted_place_quests, "Place")

graph_presented_accepted_quest_types(passage_presented_place_count, passage_accepted_place_count, "PaSSAGE", "Place")
graph_presented_accepted_quest_types(RLAID_presented_place_count, RLAID_accepted_place_count, "RLAID", "Place")
graph_presented_accepted_quest_types(random_presented_place_count, random_accepted_place_count, "random", "Place")


#-------------------------------------------------------------------------------------------------
#look into random cook as an outlier

random_presented_cook_quests = get_presented_quests_type_by_player(session_1_random, session_2_random, "Cook")
random_accepted_cook_quests = get_accepted_quests_type_by_player(session_1_random, session_2_random, "Cook")

random_presented_cook_count = []
for player in random_presented_cook_quests:
	cook_count_dict = {"Cook 2 berry recipes":0, "Cook 2 mushroom recipes":0, "Cook 2 carrot recipes":0, "Cook 2 lettuce recipes":0,"Cook 2 green onion recipes":0,"Cook 2 onion recipes": 0, "Cook 2 potato recipes": 0, "Cook 2 tomato recipes": 0}
	for quest in player: 
		cook_count_dict[quest] += 1
	random_presented_cook_count.append(cook_count_dict)

random_accepted_cook_count = []
for player in random_accepted_cook_quests:
	cook_count_dict = {"Cook 2 berry recipes":0, "Cook 2 mushroom recipes":0, "Cook 2 carrot recipes":0, "Cook 2 lettuce recipes":0,"Cook 2 green onion recipes":0,"Cook 2 onion recipes": 0, "Cook 2 potato recipes": 0, "Cook 2 tomato recipes": 0}
	for quest in player: 
		cook_count_dict[quest] += 1
	random_accepted_cook_count.append(cook_count_dict)


plt.figure(figsize=(8, 6))
for player in random_presented_cook_count:
	plt.plot(player.values(), marker='o', linestyle='-')

plt.title("random presented cook quests")
plt.ylabel("Number of Quests")
plt.xlabel("Quests")
plt.xticks([0,1,2,3,4,5,6,7], ["Cook 2 berry recipes", "Cook 2 mushroom recipes", "Cook 2 carrot recipes", "Cook 2 lettuce recipes","Cook 2 green onion recipes","Cook 2 onion recipes", "Cook 2 potato recipes", "Cook 2 tomato recipes"], rotation=20)
plt.savefig(f"difficulty/random_presented_cook_count.png", bbox_inches='tight')

plt.figure(figsize=(8, 6))
for player in random_accepted_cook_count:
	plt.plot(player.values(), marker='o', linestyle='-')

plt.title("random accepted cook quests")
plt.ylabel("Number of Quests")
plt.xlabel("Quests")
plt.xticks([0,1,2,3,4,5,6,7], ["Cook 2 berry recipes", "Cook 2 mushroom recipes", "Cook 2 carrot recipes", "Cook 2 lettuce recipes","Cook 2 green onion recipes","Cook 2 onion recipes", "Cook 2 potato recipes", "Cook 2 tomato recipes"], rotation=20)
plt.savefig(f"difficulty/random_accepted_cook_count.png", bbox_inches='tight')

plt.figure(figsize=(8, 6))
for i in range(0, len(random_presented_cook_count)):
	plt.scatter(random_presented_cook_count[i].values(), random_accepted_cook_count[i].values())

plt.title("random accepted vs presented cook quests")
plt.ylabel("Random Accepted Quests")
plt.xlabel("Random Presented Quests")
plt.savefig(f"difficulty/random_accepted_vs_presented_cook_count.png", bbox_inches='tight')