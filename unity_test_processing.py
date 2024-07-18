import processing_util

file = open('Salience\\randomQuestAIDLog.txt')
lines = file.readlines()

quest_type_positions = {"place_left": 0, "place_middle": 0, "place_right": 0, "plant_left":0, "plant_middle":0, "plant_right":0,
							"cook_left":0, "cook_middle":0, "cook_right":0, "harvest_left":0, "harvest_middle":0, "harvest_right":0}
for line in lines: 
	line = line.strip()
	quest_position = line.split(":")[2]
	quest_name = line.split(":")[1]
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

print(quest_type_positions)
