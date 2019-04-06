import sys
import re
import os
from Stemmer import Stemmer
import math
import operator
import time
stem=Stemmer('english')

stop_set = []
array_dicts = []

index = "index/"
fields = ["infobox_", "category_", "body_", "links_", "ref_", "title_"]
file_list = ["index_infobox_", "index_category_", "index_body_", "index_links_", "index_ref_", "index_title_"]
sec = "Secondary_"
doc_name = {}

def stop_words_set():
	global stop_set
	f = open('stopwords.txt', 'r')
	i = 0
	for word in f:
		if word[-1] == '\n':
			word = word[:-1]
		stop_set.append(word)
	stop_set = set(stop_set)

def get_secondary_index():
	global index, fields, file_list, sec, array_dicts

	for i in range(len(fields)):
		dict = {}
		file_name = index + sec + fields[i]
#		print file_name

		f_ptr = open(file_name, 'r')
		dict_sec = []
		cnt = 1
		for word in f_ptr:
			word = word[:-1]
			dict_sec.append(word)
			cnt += 1
		array_dicts.append(dict_sec)
#	print array_dicts

def get_file_name():
	global index
	global doc_name
	file_name = index + "list_title"
	f_ptr = open(file_name, 'r')

	for line in f_ptr:
		line = line[:-1]
		x = line.split(":")
		doc_name[x[0]] = x[1]


def find_doc(word, doc_list):
	if(len(doc_list) == 0) or (doc_list[0] > word):
		return -1;

	for i in range(len(doc_list)):
		if(word > doc_list[i]):
			return i
	return 0

def search(num_of_docs, file_length ):
	global stop_set
	global index, fields, file_list, sec, array_dicts

	stop_words_set()
	get_secondary_index()
	get_file_name()

#	print array_dicts[2]
	
	weight = [0.25, 0.15, 0.3, 0.1, 0.1, 0.8]
	print "Enter the number of queries you want to enter: ",
	t = int(raw_input())

	flag_dict = {"i":0, "c":1, "b":2, "l":3, "r":4, "t":5}
	flag_dict1 = {0:"i", 1:"c", 2:"b", 3:"l", 4:"r", 5:"t"}

	for i in range(t):
		flag = [1,1,1,1,1,1]

		print "Query " + str(i+1) + ": ",

		query =  raw_input()
		start = time.time()
		flag = [0 for i in range(6)]
		query = query.lower()
		query = query.split()
		
		query_final = {0:[],1:[],2:[],3:[],4:[],5:[]}
	#	print stop_set
		for j in query:
			if ":" in j:
				x = j.split(":")
				flag[flag_dict[x[0]]] = 1
				x[1] = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(x[1]) if len(j)>0]
				x[1] = [stem.stemWord(p) for p in x[1] if stem.stemWord(p) not in stop_set]
				for m in x[1]:
					query_final[flag_dict[x[0]]].append(m)
			else:
				j = [k.strip() for k in re.compile(r'[^A-Za-z0-9]+').split(j) if len(k)>0]
				j = [stem.stemWord(p) for p in j if stem.stemWord(p) not in stop_set]
				if(len(j) > 0):
					j = j[0]
					for k in range(6):
						query_final[k].append(j)
		if 1 not in flag:
			flag = [1 for i in range(6)]

		tfidf = {}
#		print query_final
		for j in range(6):
			if len(query_final[j]) == 0:
				continue
			
			for k in query_final[j]:
				doc_num = find_doc(k, array_dicts[j])
				if(doc_num == -1):
					continue
				file_name = index + file_list[j] + str(doc_num+1)
#				print file_name
				f_ptr = open(file_name, 'r')

				for line in f_ptr:
					line = line[:-1]
					line = line.split("=")

					if(line[0] == k):
						x = line[1].split('$')
						idf_cost = int(x[0])
#						print line[1]
						if(idf_cost > 0):
							idf_cost = math.log10((num_of_docs/idf_cost))
						for y in range(1,len(x)):
							z = x[y].split(":")
							tf_cost = math.log10(1+int(z[1]))
							try:
								tfidf[z[0]] += tf_cost*idf_cost*weight[j]
							except:
								tfidf[z[0]] = tf_cost*idf_cost*weight[j]
						break
			end = time.time()
			if end-start > 1.5:
				break
		tfidf = sorted(tfidf.items(), key=operator.itemgetter(1))
		tfidf.reverse()
		
		x = min(len(tfidf), 10)
		if x == 0:
			continue
		print "\n\n"
		print "\tBest Search result(s):"
		for k in range(x):
			print "\t    - " + doc_name[tfidf[k][0]]
		print "\n\n"
		end = time.time()
		print end-start

search(5311,0)