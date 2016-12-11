import sys
import math
from predictor import Predictor, compute_weighted_average, compute_mean, clean_user
import collections
import math
from heapq import heappush, heappop

class Spearman(Predictor):
	def __init__(self):
		self.user_data = None

	def train(self, user_data):
		self.user_data = user_data

	def predict(self, user_num, user_set, num_neighbors):
		#Make sure you hide the training data on the values in the user_set
		print(user_num)
		prediction_set = {}
		user_pre_clean = self.user_data[user_num]
		user_post_clean = clean_user(user_pre_clean)
		#user_post_clean contains all the values for a user not in our prediction set
		similarity_to_user = []
		#generate relevant subset
		for user_v in self.user_data:
			# exclude current user
			if user_v != user_num:
				similarity = self.calculate_spearman_similarity(user_post_clean, self.user_data[user_v])
				similarity_to_user.append((similarity, self.user_data[user_v]))
		similarity_to_user.sort(key=lambda x: x[0], reverse=True)
		for movie in user_set:
			prediction = compute_weighted_average(user_post_clean, similarity_to_user, movie, num_neighbors)
			if prediction > 5.0:
				prediction = 5.0
			elif prediction < 0.5:
				prediction = 0.5
			prediction_set[movie] = prediction
		return collections.OrderedDict(sorted(prediction_set.items()))

	def calculate_spearman_similarity(self, u, v):
		# mean_u = compute_mean_spearman(u)
		# mean_v = compute_mean_spearman(v)
		#generate intersection subset

		intersection = []
		for movie in u:
			if movie in v:
				intersection.append(movie)
		if len(intersection) == 0:
			return 0


		movie_ranks_u = {}
		movie_ranks_v = {}

		index = 0.5

		while index <= 5.0:
			movie_ranks_u[index] = 0
			movie_ranks_v[index] = 0
			index += 0.5

		for movie in intersection:
			movie_ranks_u[u[movie]] += 1
			movie_ranks_v[v[movie]] += 1



		for movie in intersection:
			numerator += (u[movie] - mean_u) * (v[movie] - mean_v)


		#calulate denominator
		denominator = 0.0
		radical1 = 0.0
		radical2 = 0.0
		for movie in intersection:
			radical1 += math.pow(u[movie] - mean_u, 2)
			radical2 += math.pow(v[movie] - mean_v, 2)
		radical1 = math.sqrt(radical1)
		radical2 = math.sqrt(radical2)
		denominator = radical1 * radical2
		if denominator == 0:
			return 0.0
		return numerator / denominator

	def compute_mean_spearman(u):
		sum_u = 0.0
		for movie in u:
			sum_u += u[movie]
		return sum_u / len(u)

