"""
config.py

File thuc hien thuat toan LSH
"""


import re
import random
import time
import operator
import config

class LSH():
	def __init__(self, K, p, r, nn, items):
		self.nextPrime = config.nextPrime
		self.maxID = config.maxID
		self.K = K
		self.p = p
		self.r = r
		self.coeffA=[]
		self.coeffB=[]
		self.num_nearest_neighbors = nn
		self.num_items = 0
		self.items = items		# danh sach co phan tu thu i la tap hop cac user thich item thu i
		self.cluster = {} 		# cac item co tap r ma bam giong nhau duoc bam vao cung 1 cum
						# khoa cua moi cum la tap r gia tri la gia tri bam cua tung ham bam doi voi mot item,
						# neu cac item co tap r gia tri giong nhau thi tuc la cung khoa, va duoc bam vao cung 1 cum
		self.hash = {} 			# moi item se co mot tap gom p khoa, ung voi p cum
		self.similarity = {} 		# danh sach co phan tu thu i la danh sach cac item tuong tu item thu i

	# chon ra K gia tri ngau nhien
	def pick_random_coeffs(self, K):
		randList = []
		while K > 0:
			randIndex = random.randint(1, self.maxID)
			while randIndex in randList:
				randIndex = random.randint(1, self.maxID)
			randList.append(randIndex)
			K = K - 1
		return randList

	# chon ra ho K ham bam
	def pick_family_MIH_functions(self):
		self.coeffA = self.pick_random_coeffs(self.K)
		self.coeffB = self.pick_random_coeffs(self.K)

	def locality_senstive_hashing(self, item_id):
		self.num_items += 1
		# print "Item: ", item_id
		self.hash[item_id] = self.minHash(item_id)
		if len(self.cluster) == 0:
			p=0
			for key in self.hash[item_id]:
				self.cluster[p]={}
				self.cluster[p][key] = [item_id] #them item dang xet vao cum co khoa key
				p+=1
		else:
			p=0
			for key in self.hash[item_id]:
				if key in self.cluster[p]:
					self.cluster[p][key].append(item_id)
				else:
					self.cluster[p][key] = [item_id]
				p+=1

	def minHash(self, item_id):
		cnt = 0
		keys_list = [] # danh sach p khoa cua item dang xet o p cum
		for i in range(self.p):
			hashCodes_list = [] # danh sach cac hashCode cua item dang xet o cum thu i,
								# day cung chinh la khoa cua item o cum do
			for j in range(self.r):
				minHashCode = self.nextPrime + 1
				for user in self.items[item_id]:
					hashCode = (self.coeffA[cnt] * user + self.coeffB[cnt]) % self.nextPrime 
					if hashCode < minHashCode:
						minHashCode = hashCode
				hashCodes_list.append(minHashCode)
				cnt += 1
			keys_list.append(tuple(hashCodes_list))
		return keys_list

	def find_similarity_items(self, item_id):	
		p=0
		temp = {}
		set1 =self.items[item_id]
		for key in self.hash[item_id]:
			for item in self.cluster[p][key]: # cac item co khoa la key
				set2 =self.items[item]
				J = (len(set1.intersection(set2)) / len(set1.union(set2)))
				if item != item_id:
					if item in temp:
						if temp[item]<J:
							temp[item] = J
					else:
						temp[item]=J
			p+=1
		temp = sorted(list(temp.items()), key=operator.itemgetter(1))
		#xoa phan tu thu i
		items_list = []
		for i in temp[-self.num_nearest_neighbors:]:
			items_list.append(i[0])
		self.similarity[item_id] = items_list

	def remove_item_from_clusters(self, item_id):
		p=0
		for key in self.hash[item_id]:
			self.cluster[p][key].remove(item_id)
			if len(self.cluster[p][key]) == 0:
				self.cluster.pop(key, None)
			p+=1

	def find_all_similarity(self):	
		for i in range(self.num_items):
			self.find_similarity_items(i)	
		return self.similarity
