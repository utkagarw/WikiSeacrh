import sys
import os
import re
import operator
import time
def merge(files_count):
	start = time.time()
	index = "index/"
	files_list = ["infobox_", "category_", "body_", "links_", "ref_", "title_"]

	files_list_new = ["index_infobox_", "index_category_", "index_body_", "index_links_", "index_ref_", "index_title_"]


	for a in range(0,len(files_list)):
		new_files_count = 1
		fptr = []
		new_name = index + files_list_new[a] + str(new_files_count)
		new_fptr = open(new_name,'w')
		new_name1 = index + "Secondary_" + files_list[a]
		new_fptr_sec = open(new_name1,'w')
		index_words = 0
		max_index_words = 2000
		fl = 0
		for j in range(1,files_count+1):
			name = index + files_list[a] + str(j)
			fpt = open(name, 'r') 
			fptr.append(fpt)

		word_ctr = [0]*files_count
		words_list = [""]*files_count
		words_split = [""]*files_count
		flag = [0]*files_count
	

		for i in range(len(word_ctr)):
			try:
				words_list[i] = fptr[i].readline().split("\n")[0]
				words_split[i] = words_list[i].split("=")[0]
			except:
				flag[i] = 1

		while(1):
			cur1 = "zzzzzzzzzzzzzzzzzzzzzzz"
			cur2 = "zzzzzzzzzzzzzzzzzzzzzzz"
			for i in range(len(word_ctr)):
				if(words_list[i] == ''):
					flag[i] = 1
				if words_split[i]!= "" and words_split[i] < cur1:
					cur1 = words_split[i]
			word1=""
			for i in range(len(word_ctr)):
				try:
					if(cur1 == words_split[i]):
						if(word1 == ""):
							word1 = words_list[i]
						else:
							x1 = word1.split("=")[1]
							cnt1 = x1.split("$")[0]
							l = len(cnt1)
							list1 = x1[l:]

							word2 = words_list[i].split("=")[1]
							cnt2 = word2.split("$")[0]
							l = len(cnt2)
							list2 = word2[l:]
							
							word1 = word1.split("=")[0] + '=' +str((int(cnt1)) + (int(cnt2))) + list1 + list2
						word_ctr[i] += 1
						words_list[i] = fptr[i].readline().split("\n")[0]
						words_split[i] = words_list[i].split("=")[0]
						if(words_split[i] == ""):
							flag[i] = 1
				except:
					cur2 = "zzzzzzzzzzzzzzzzzzzzzzz"
					flag[i] = 1
		
			x = word1.split('=')
			y = x[1].split('$')
	#		print x
	#		print y
			dic_new = {}
			for m in y:
				z = m.split(':')
				if(len(z) > 1):
				#	print "Yes", z[0], z[1]
					dic_new[z[0]] = int(z[1])
			dic_new = sorted(dic_new.items(), key=operator.itemgetter(1))
			dic_new.reverse()
			word1 = ""
			for m in dic_new:
			#	print m
				word1 += '$' + m[0] + ':' + str(m[1])
			word1 = x[0]+ '=' + y[0] + word1

			new_fptr.write(word1+"\n")
			if(fl == 0):
				new_fptr_sec.write( word1.split("=")[0] +"\n")
				fl = 1
			if 0 not in flag:
				break
			index_words += 1
			if(index_words == max_index_words):
				new_fptr.close()
				new_files_count += 1
				new_name = index + files_list_new[a] + str(new_files_count)
				new_fptr = open(new_name,'w')
				index_words = 0
				fl = 0
		new_fptr_sec.close()
	end = time.time()
	print end-start