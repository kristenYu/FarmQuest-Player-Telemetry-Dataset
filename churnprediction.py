import processing_util
import scipy
import statistics as statistics
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge



def get_day_data_from_keys(session_keys, session_num):
	day_data = []
	for key in session_keys:
		telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
		day_telemetry = []
		for t in telemetry[f"session_{session_num}"]:
			if "Event:Day" in t:
				day_telemetry.append(t.split(";")[0].replace("Event:Day", ""))
		if day_telemetry == []:
			day_telemetry.append(1)
		day_data.append(int(day_telemetry[-1]))
	return day_data

def print_average_stdev_sem(session_data, session_num, aid):
	print(f"average number of days based off session {session_num} {aid} data " + str(statistics.mean(session_data)))
	print("stdev " + str(statistics.stdev(session_data)))
	print("SEM " + str(scipy.stats.sem(session_data)))


processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);
print("number of participants " + str(len(data)))

valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys = processing_util.get_valid_keys(data)
print(len(valid_keys))

starting_time = []
ending_time = []

key = valid_keys.pop()
telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))


session_1_day_data = []
session_2_day_data = []
for key in valid_keys:
	telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"))
	day_telemetry = []
	for t in telemetry["session_1"]:
		if "Event:Day" in t:
			day_telemetry.append(t.split(";")[0].replace("Event:Day", ""))
	if day_telemetry == []:
		day_telemetry.append(1)
	session_1_day_data.append(int(day_telemetry[-1]))
	day_telemetry = []
	for t in telemetry["session_2"]:
		if "Event:Day" in t:
			day_telemetry.append(t.split(";")[0].replace("Event:Day", ""))
	session_2_day_data.append(int(day_telemetry[-1]))

print("session 1 vs 2 day data kruskal test: " + str(scipy.stats.kruskal(session_1_day_data, session_2_day_data)))

print_average_stdev_sem(session_1_day_data, 1, "total")
print_average_stdev_sem(session_2_day_data, 2, "total")

session_1_passage_day_data = get_day_data_from_keys(session_1_passage, 1)
session_2_passage_day_data = get_day_data_from_keys(session_2_passage, 2)

print("session 1 vs 2 passage day data kruskal test: " + str(scipy.stats.kruskal(session_1_passage_day_data, session_2_passage_day_data)))
print_average_stdev_sem(session_1_passage_day_data, 1, "passage")
print_average_stdev_sem(session_2_passage_day_data, 2, "passage")

session_1_RLAID_day_data = get_day_data_from_keys(session_1_RLAID, 1)
session_2_RLAID_day_data = get_day_data_from_keys(session_2_RLAID, 2)

print("session 1 vs 2 RLAID day data kruskal test: " + str(scipy.stats.kruskal(session_1_RLAID_day_data, session_2_RLAID_day_data)))
print_average_stdev_sem(session_1_RLAID_day_data, 1, "RLAID")
print_average_stdev_sem(session_2_RLAID_day_data, 2, "RLAID")


session_1_random_day_data = get_day_data_from_keys(session_1_random, 1)
session_2_random_day_data = get_day_data_from_keys(session_2_random, 2)

print("session 1 vs 2 random day data kruskal test: " + str(scipy.stats.kruskal(session_1_random_day_data, session_2_random_day_data)))
print_average_stdev_sem(session_1_random_day_data, 1, "random")
print_average_stdev_sem(session_2_random_day_data, 2, "random")

bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

day_means = [statistics.mean(session_1_passage_day_data), 
			statistics.mean(session_2_passage_day_data),
			statistics.mean(session_1_RLAID_day_data), 
			statistics.mean(session_2_RLAID_day_data),
			statistics.mean(session_1_random_day_data), 
			statistics.mean(session_2_random_day_data),
			]

day_stdev = [statistics.stdev(session_1_passage_day_data),
			 statistics.stdev(session_2_passage_day_data),
			 statistics.stdev(session_1_RLAID_day_data),
			 statistics.stdev(session_2_RLAID_day_data),
			 statistics.stdev(session_1_random_day_data),
			 statistics.stdev(session_2_random_day_data),
			]

br1 = np.arange(len(day_means))
plt.bar(br1, day_means, width = bar_width, yerr=day_stdev)

plt.title('Mean Number of Days In Game', fontweight = 'bold', fontsize = 15)
plt.xlabel('Session and AI Director', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Number of days', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(day_means))], ['passage session 1', 'passage session 2 ', 'RLAID session 1', 'RLAID session 2', 'random session 1', 'random session 2'])

plt.savefig('churn/day_mean_by_session_aid.png', bbox_inches='tight')

session_passage_day_data = session_1_passage_day_data + session_2_passage_day_data
session_RLAID_day_data = session_1_RLAID_day_data + session_2_RLAID_day_data

print_average_stdev_sem(session_passage_day_data, "passage", 0)
print_average_stdev_sem(session_RLAID_day_data, "RLAID", 0)

bar_width = 0.25
fig = plt.subplots(figsize=(12,8))

day_means = [statistics.mean(session_passage_day_data), 
			statistics.mean(session_RLAID_day_data), 
			statistics.mean(session_1_random_day_data), 
			statistics.mean(session_2_random_day_data),
			]

day_stdev = [statistics.stdev(session_passage_day_data),
			 statistics.stdev(session_RLAID_day_data),
			 statistics.stdev(session_1_random_day_data),
			 statistics.stdev(session_2_random_day_data),
			]

br1 = np.arange(len(day_means))
plt.bar(br1, day_means, width = bar_width, yerr=day_stdev)

plt.title('Mean Number of Days In Game', fontweight = 'bold', fontsize = 15)
plt.xlabel('Session and AI Director', fontweight = 'bold', fontsize = 15)
plt.ylabel('Mean Number of days', fontweight = 'bold', fontsize = 15)
plt.xticks([r+bar_width for r in range(len(day_means))], ['passage session', 'RLAID session', 'random session 1', 'random session 2'])

plt.savefig('churn/day_mean_combined_aid.png', bbox_inches='tight')


#statistical tests for difference
print("passage session 1 vs passage session 2 mann whitney u" + str(scipy.stats.mannwhitneyu(session_1_passage_day_data, session_2_passage_day_data)))
print("passage session 1 vs RLAID session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_passage_day_data, session_1_RLAID_day_data)))
print("passage session 1 vs RLAID session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_passage_day_data, session_2_RLAID_day_data)))
print("passage session 1 vs random session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_passage_day_data, session_1_random_day_data)))
print("passage session 1 vs random session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_passage_day_data, session_2_random_day_data)))

print("passage session 2 vs RLAID session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_passage_day_data, session_1_RLAID_day_data)))  
print("passage session 2 vs RLAID session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_passage_day_data, session_2_RLAID_day_data)))
print("passage session 2 vs random session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_passage_day_data, session_1_random_day_data)))
print("passage session 2 vs random session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_passage_day_data, session_2_random_day_data)))

print("RLAID session 1 vs RLAID session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_RLAID_day_data, session_2_RLAID_day_data)))
print("RLAID session 1  vs random session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_RLAID_day_data, session_1_random_day_data)))
print("RLAID session 1  vs random session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_RLAID_day_data, session_2_random_day_data)))

print("RLAID session 2  vs random session 1 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_RLAID_day_data, session_1_random_day_data)))
print("RLAID session 2  vs random session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_2_RLAID_day_data, session_2_random_day_data)))

print("random session 1  vs random session 2 mann whitney u " + str(scipy.stats.mannwhitneyu(session_1_random_day_data, session_2_random_day_data)))
print("random session 1  vs random session 2 mann whitney u alternate greater " + str(scipy.stats.mannwhitneyu(session_1_random_day_data, session_2_random_day_data, alternative="greater")))


#look at see if we can collapse session 1's and session 2's into each other 
print("session 1 passage vs RLAID day data kruskal test: " + str(scipy.stats.kruskal(session_1_passage_day_data, session_1_RLAID_day_data)))
print("session 1 random vs RLAID day data kruskal test: " + str(scipy.stats.kruskal(session_1_random_day_data, session_1_RLAID_day_data)))
print("session 1 passage vs random day data kruskal test: " + str(scipy.stats.kruskal(session_1_passage_day_data, session_1_random_day_data)))

print("session 2 passage vs RLAID day data kruskal test: " + str(scipy.stats.kruskal(session_2_passage_day_data, session_2_RLAID_day_data)))
print("session 2 random vs RLAID day data kruskal test: " + str(scipy.stats.kruskal(session_2_random_day_data, session_2_RLAID_day_data)))
print("session 2 passage vs random day data kruskal test: " + str(scipy.stats.kruskal(session_2_passage_day_data, session_2_random_day_data)))


print("passage vs RLAID day data mann whitney u " + (str(scipy.stats.mannwhitneyu(session_passage_day_data, session_RLAID_day_data))))
print("passage vs random session 1 day data mann whitney u " + (str(scipy.stats.mannwhitneyu(session_passage_day_data, session_1_random_day_data))))
print("passage vs random session 2 day data mann whitney u " + (str(scipy.stats.mannwhitneyu(session_passage_day_data, session_2_random_day_data))))

print("RLAID vs random session 1 day data mann whitney u " + (str(scipy.stats.mannwhitneyu(session_RLAID_day_data, session_1_random_day_data))))
print("RLAID vs random session 2 day data mann whitney u " + (str(scipy.stats.mannwhitneyu(session_RLAID_day_data, session_2_random_day_data))))

session_1_keys = session_1_passage + session_1_RLAID + session_1_random
session_2_keys = session_2_passage + session_2_RLAID + session_2_random
total_keys = session_1_keys + session_2_keys


session_1_feature_data = processing_util.get_small_player_feature_vector(session_1_keys, 1, data)
session_2_feature_data = processing_util.get_small_player_feature_vector(session_2_keys, 2, data)
total_small_feature_data = session_1_feature_data + session_2_feature_data

session_1_large_feature_data = processing_util.get_large_player_feature_vector(session_1_keys, 1, data)
session_2_large_feature_data = processing_util.get_large_player_feature_vector(session_2_keys, 2, data)
total_large_feature_data = session_1_large_feature_data + session_2_large_feature_data

session_1_day_data = get_day_data_from_keys(session_1_keys, 1)
session_2_day_data = get_day_data_from_keys(session_2_keys, 2)
total_day_data = session_1_day_data + session_2_day_data

#Classifier
small_feature_data_train, small_feature_data_test, day_data_train, day_data_test = train_test_split(total_small_feature_data, total_day_data, test_size=0.2, shuffle=True)
model = SVC(C=1, kernel='linear', tol=0.001)
model.fit(small_feature_data_train, day_data_train)
pred_train = model.predict(small_feature_data_train)

print(confusion_matrix(day_data_train, pred_train))
print(classification_report(day_data_train, pred_train))
print("small feature train accuracy score: " + str(accuracy_score(day_data_train, pred_train)))

pred = model.predict(small_feature_data_test)

print(confusion_matrix(day_data_test, pred))
print(classification_report(day_data_test, pred))
print("small test accuracy score: " + str(accuracy_score(day_data_test, pred)))

large_feature_data_train, large_feature_data_test, day_data_train, day_data_test = train_test_split(total_large_feature_data, total_day_data, test_size=0.2, shuffle=True)
model = SVC(C=1, kernel='linear', tol=0.001)
model.fit(large_feature_data_train, day_data_train)
pred_train = model.predict(large_feature_data_train)
print(confusion_matrix(day_data_train, pred_train))
print(classification_report(day_data_train, pred_train))
print("large feature train accuracy score: " + str(accuracy_score(day_data_train, pred_train)))

pred = model.predict(large_feature_data_test)

print(confusion_matrix(day_data_test, pred))
print(classification_report(day_data_test, pred))
print("large test accuracy score: " + str(accuracy_score(day_data_test, pred)))


#Linear Regression
linear_regression = LinearRegression()
linear_regression.fit(total_small_feature_data, total_day_data)
print("small feature linear regression score: " + str(linear_regression.score(total_small_feature_data, total_day_data)))

linear_regression.fit(total_large_feature_data, total_day_data)
print("large feature linear regression score: " + str(linear_regression.score(total_large_feature_data, total_day_data)))
print("large feature linear regression coefficients: " + str(linear_regression.coef_))


for i in range(0, 3):
	sample = random.randint(0, len(total_large_feature_data))
	print(linear_regression.predict(np.reshape(np.array(total_large_feature_data[sample]), (1,-1))))
	print(total_day_data[sample])



#Ridge Regression
ridge_regression = Ridge()
ridge_regression.fit(total_small_feature_data, total_day_data)
print("small feature ridge regression score " + str(ridge_regression.score(total_small_feature_data, total_day_data)))

ridge_regression.fit(total_large_feature_data, total_day_data)
print("large feature ridge regression score " + str(ridge_regression.score(total_large_feature_data, total_day_data)))


#pearson test for length of day
session_1_passage_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_passage, data)
session_2_passage_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_passage, data)
session_1_RLAID_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_RLAID, data)
session_2_RLAID_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_RLAID, data)
session_1_random_survey_data = processing_util.get_session_1_short_survey_data_accross_keys(session_1_random, data)
session_2_random_survey_data = processing_util.get_session_2_short_survey_data_accross_keys(session_2_random, data)


print(statistics.mean(session_1_passage_survey_data["pos_enjoy"]))

print("pearson r session 1 passage pos enjoy vs days" + str(scipy.stats.pearsonr(session_1_passage_survey_data["pos_enjoy"], session_1_passage_day_data)))
print("pearson r session 1 passage pos enjoy vs days" + str(scipy.stats.pearsonr(session_2_passage_survey_data["pos_enjoy"], session_2_passage_day_data)))
print("pearson r session 1 random pos enjoy vs days" + str(scipy.stats.pearsonr(session_1_random_survey_data["pos_enjoy"], session_1_random_day_data)))
print("pearson r session 1 random pos enjoy vs days" + str(scipy.stats.pearsonr(session_2_random_survey_data["pos_enjoy"], session_2_random_day_data)))
print("pearson r session 1 RLAID pos enjoy vs days" + str(scipy.stats.pearsonr(session_1_RLAID_survey_data["pos_enjoy"], session_1_RLAID_day_data)))
print("pearson r session 1 RLAID pos enjoy vs days" + str(scipy.stats.pearsonr(session_2_RLAID_survey_data["pos_enjoy"], session_2_RLAID_day_data)))



fig = plt.subplots(figsize=(12,8))
plt.scatter(session_1_passage_survey_data["pos_enjoy"], session_1_passage_day_data)
plt.savefig('churn/posenjoy_day_correlation.png', bbox_inches='tight')