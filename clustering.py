import processing_util
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy import stats
from sklearn.manifold import TSNE

def graph_player_clusters(session_feature_data, session_num, aid):
	if(not(session_num == 1 or session_num == 2)):
		raise Error("session num must be value one or two")
	scaler = StandardScaler()
	scaled_features = scaler.fit_transform(session_feature_data)
	inertias = []
	if(len(session_feature_data) > 10):
		for i in range(1,11):
			kmeans = KMeans(n_clusters=i)
			kmeans.fit(scaled_features)
			inertias.append(kmeans.inertia_)

		fig = plt.subplots(figsize=(12,8))
		plt.plot(range(1,11), inertias, marker='o')
		plt.title(f"Session {session_num} Elbow Method")
		plt.xlabel('number of clusters')
		plt.ylabel('inertia')
		plt.savefig(f"clustering/session_{session_num}_{aid}_elbow_method.png")

		k1 = KneeLocator(range(1,11), inertias, curve="convex", direction="decreasing")
		print(f"session {session_num} elbow k " + str(k1.elbow))
		kmeans = KMeans(n_clusters=k1.elbow)
		kmeans.fit(scaled_features)
		print(f"session {session_num} {aid} cluster centers:" + str(kmeans.cluster_centers_))
		print(f"session {session_num} {aid} labels: " + str(kmeans.labels_))
	else: 
		for i in range(1, len(session_feature_data) + 1):
			kmeans = KMeans(n_clusters=i)
			kmeans.fit(scaled_features)
			inertias.append(kmeans.inertia_)
		fig = plt.subplots(figsize=(12,8))
		plt.plot(range(1,len(session_feature_data) + 1), inertias, marker='o')
		plt.title(f"Session {session_num} Elbow Method")
		plt.xlabel('number of clusters')
		plt.ylabel('inertia')
		plt.savefig(f"clustering/session_{session_num}_{aid}_elbow_method.png", bbox_inches='tight')

		k1 = KneeLocator(range(1,len(session_feature_data) + 1), inertias, curve="convex", direction="decreasing")
		print(f"session {session_num} elbow k " + str(k1.elbow))
		kmeans = KMeans(n_clusters=k1.elbow)
		kmeans.fit(scaled_features)
		print(f"session {session_num} {aid} cluster centers:" + str(kmeans.cluster_centers_))
		print(f"session {session_num} {aid} labels: " + str(kmeans.labels_))
	

	'''
	tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
	tsne_results = tsne.fit_transform(scaled_features)

	fig = plt.subplots(figsize=(12,8))
	plt.scatter(x=tsne_results[:,0], y=tsne_results[:,1])
	plt.savefig(f"clustering/session_{session_num}_{aid}_tsne.png", bbox_inches='tight')
	'''
	pca = PCA(n_components=2)
	principle_components =pca.fit_transform(scaled_features)
	principleDf = pd.DataFrame(data = principle_components, columns = ["principle component 1", "principle component 2"])

	cluster_centers_pca = pca.fit_transform(kmeans.cluster_centers_)
	cluster_centers = pd.DataFrame(data = cluster_centers_pca, columns = ["cluster center 1", "cluster center 2"])

	fig = plt.subplots(figsize=(12,8))
	colors = ['blue', 'orange', 'red', 'purple']
	plt.scatter(cluster_centers["cluster center 1"], cluster_centers["cluster center 2"],color="black" ,marker="x", s=240)
	for i in range(0, len(kmeans.labels_)):
		plt.scatter(principleDf['principle component 1'][i], principleDf['principle component 2'][i], color = colors[kmeans.labels_[i]], s=240)
	#plt.title(f"Session {session_num} {aid} PCA")
	plt.xlabel("principle component 1", fontsize=35)
	plt.ylabel("principle component 2", fontsize=35)
	plt.xticks(fontsize=25)
	plt.yticks(fontsize=25)
	plt.savefig(f"clustering/session_{session_num}_{aid}_pca.pdf", bbox_inches='tight')
	


#create player vectors
processing_util.process_json_bulk()
data = processing_util.get_only_complete_data(False);
print("number of participants " + str(len(data)))

valid_keys, session_1_passage, session_1_RLAID, session_1_random, session_2_passage, session_2_RLAID, session_2_random, passage_then_RLAID_keys, passage_then_random_keys, RLAID_then_random_keys, RLAID_then_passage_keys, random_then_passage_keys, random_then_RLAID_keys = processing_util.get_valid_keys(data)

session_1_feature_data = []
session_2_feature_data = []
total_feature_data = []
for key in valid_keys:
	#plant, harvest, cook, place
	player_features = [0 for x in range(0,4)]
	telemetry = processing_util.split_telemetry_into_session(data[key]["telemetry_data"].split("\n"));
	for t in telemetry["session_1"]: 
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
	session_1_feature_data.append(player_features)
	player_features = [0 for x in range(0,4)]
	total_feature_data.append(player_features)
	for t in telemetry["session_2"]:
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
	session_2_feature_data.append(player_features)
	total_feature_data.append(player_features)

#session data comparison -> they are not the same
print("session 1 feature data vs session 2 feature data kruskal test " + str(scipy.stats.kruskal(session_1_feature_data, session_2_feature_data)))


#total feature data
graph_player_clusters(session_1_feature_data, 1, "total")
graph_player_clusters(session_2_feature_data, 2, "total")

session_1_passage_feature_data = processing_util.get_small_player_feature_vector(session_1_passage, 1, data)
session_2_passage_feature_data = processing_util.get_small_player_feature_vector(session_2_passage, 2, data)
print("session 1 vs 2 passage feature data kruskal test" + str(scipy.stats.kruskal(session_1_passage_feature_data, session_2_passage_feature_data)))
graph_player_clusters(session_1_passage_feature_data, 1, "passage")
graph_player_clusters(session_2_passage_feature_data, 2, "passage")

session_1_RLAID_feature_data = processing_util.get_small_player_feature_vector(session_1_RLAID, 1, data)
session_2_RLAID_feature_data = processing_util.get_small_player_feature_vector(session_2_RLAID, 2, data)
print("session 1 vs 2 RLAID feature data kruskal test" + str(scipy.stats.kruskal(session_1_RLAID_feature_data, session_2_RLAID_feature_data)))
graph_player_clusters(session_1_RLAID_feature_data, 1, "RLAID")
graph_player_clusters(session_2_RLAID_feature_data, 2, "RLAID")

session_1_random_feature_data = processing_util.get_small_player_feature_vector(session_1_random, 1, data)
session_2_random_feature_data = processing_util.get_small_player_feature_vector(session_2_random, 2, data)
print("session 1 vs 2 random feature data kruskal test" + str(scipy.stats.kruskal(session_1_random_feature_data, session_2_random_feature_data)))
graph_player_clusters(session_1_random_feature_data, 1, "random")
graph_player_clusters(session_2_random_feature_data, 2, "random")


#check and see if the session is the contributing factor 
print("session 1 passage vs RLAID" + str(scipy.stats.kruskal(session_1_passage_feature_data, session_1_RLAID_feature_data)))
print("session 1 random vs RLAID" + str(scipy.stats.kruskal(session_1_random_feature_data, session_1_RLAID_feature_data)))
print("session 1 random vs passage" + str(scipy.stats.kruskal(session_1_random_feature_data, session_1_passage_feature_data)))

print("session 2 passage vs RLAID" + str(scipy.stats.kruskal(session_2_passage_feature_data, session_2_RLAID_feature_data)))
print("session 2 random vs RLAID" + str(scipy.stats.kruskal(session_2_random_feature_data, session_2_RLAID_feature_data)))
print("session 2 random vs passage" + str(scipy.stats.kruskal(session_2_random_feature_data, session_2_passage_feature_data)))
