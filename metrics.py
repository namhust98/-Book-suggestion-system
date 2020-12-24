"""
config.py

File thong ke chuong trinh
"""


import time
from lsh import LSH
import operator

def jaccard_calc(num_items, set_of_user):
	similarity_list = [] # phan tu thu i chua k item gan voi item i nhat
	print("\nTinh toan do do Jaccard giua tat ca cac items...")
	t0 = time.time()
	for i in range(0, num_items):
		if (i % 100) == 0:
			print("  (" + str(i) + " / " + str(num_items) + ")")
		temp = {}
		set1 = set_of_user[i]
		for j in range(0, num_items):
			set2 = set_of_user[j]
			J = (len(set1.intersection(set2)) / len(set1.union(set2)))
			if j != i:
				temp[j] = J
		temp = sorted(list(temp.items()), key=operator.itemgetter(1))
		#xoa phan tu thu i
		items_list = []
		for i in temp[-4:]:
			items_list.append(i[0])
		similarity_list.append(set(items_list))

	elapsed = (time.time() - t0)
	print("\nThoi gian tinh toan: %.2fsec" % elapsed)
	return similarity_list


def accuracy_calc(pred, true, num_items):
	s1 = set()
	s2 = set()
	acc = []
	for i in range(num_items):
		s1 = set(pred[i])
		s2 = set(true[i])
		# acc.append((len(s1.intersection(s2)) / len(s1.union(s2))))
		acc.append((len(s1.intersection(s2)) / len(s2)))		
	result = sum(acc) / num_items
	return result
