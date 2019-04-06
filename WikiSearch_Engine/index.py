import sys
import xml.sax
import re
import os
from Stemmer import Stemmer
import merge
stem=Stemmer('english')

stop_set = []
docs_max = 1000
file_count = 1
cont = 0
dict_title = {}
dict_body = {}
dict_infobox = {}
dict_category = {}
dict_links = {}
dict_ref = {}

title_file = open("index/list_title",'w')
file_infobox = open('index/infobox_1', 'w')
file_title = open('index/title_1', 'w')
file_body = open('index/body_1', 'w')
file_ref = open('index/ref_1', 'w')
file_links = open('index/links_1', 'w')
file_category = open('index/category_1', 'w')

def stop_words_set():
	global stop_set
	f = open('stopwords.txt', 'r')
	i = 0
	for word in f:
		if word[-1] == '\n':
			word = word[:-1]
		stop_set.append(word)
	stop_set = set(stop_set)



class My_Wiki_Handler( xml.sax.ContentHandler ):
	def __init__(self):
		self.title = ""
		self.body = ""
		self.infobox = ""
		self.category = ""
		self.links = ""
		self.ref = ""
		self.stack = []
		self.stack.append("Dummy1")
		self.cur_tag = "Dummy1"
		self.data = ""
		self.id = ""
		self.docs_count = 0

#	def page_init(self):

	# Call when an element starts
	def startElement(self, tag, attributes):
		self.stack.append(tag)
		self.cur_tag = tag

	def endElement(self, tag):
		global stop_set, docs_max, file_count, cont
		global dict_title, dict_infobox, dict_category, dict_ref, dict_links, dict_body
		global file_infobox, file_title, file_category, file_ref, file_body, file_links
	
		if(self.cur_tag == "page"):
			self.docs_count += 1
			cont += 1
			self.title = ""
			self.body = ""
			self.infobox = ""
			self.category = ""
			self.links = ""
			self.ref = ""
			if len(self.stack) > 3:
				self.stack = []
				self.stack.append("Dummy1")
				self.stack.append("Dummy2")
				self.cur_tag = "Dummy2"
			self.data = ""
			self.id = ""

			if self.docs_count == docs_max:
				string_infobox = ""
				string_title = ""
				string_infobox = ""
				string_infobox = ""
				string_infobox = ""
				string_infobox = ""
				
			#	if(file_count == 2):
			#		print dict_title["red"]
				for word in sorted( dict_title.keys() ):
					string_title = word + "=" + dict_title[word] + '\n'
					file_title.write(string_title)

				for word in sorted( dict_infobox.keys() ):
					string_infobox = word + "=" + dict_infobox[word] + '\n'
					file_infobox.write(string_infobox)

				for word in sorted( dict_category.keys() ):
					string_category = word + "=" + dict_category[word] + '\n'
					file_category.write(string_category)

				for word in sorted( dict_body.keys() ):
					string_body = word + "=" + dict_body[word] + '\n'
					file_body.write(string_body)

				for word in sorted( dict_ref.keys() ):
					string_ref = word + "=" + dict_ref[word] + '\n'
					file_ref.write(string_ref)

				for word in sorted( dict_links.keys() ):
					string_links = word + "=" + dict_links[word] + '\n'
					file_links.write(string_links)

				clear_dict()
				close_file()

				self.docs_count = 0
				file_count += 1
				infobox = "index/infobox_"+str(file_count)
				title = "index/title_"+str(file_count)
				body = "index/body_"+str(file_count)
				ref = "index/ref_"+str(file_count)
				links = "index/links_"+str(file_count)
				category = "index/category_"+str(file_count)

				file_title = open(title, 'w')
				file_infobox = open(infobox, 'w')
				file_body = open(body, 'w')
				file_ref = open(ref, 'w')
				file_links = open(links, 'w')
				file_category = open(category, 'w')

			if(cont%10000 == 0):
				print str(cont) + " Docs parsed"
		elif(len(self.stack) > 1 and self.stack[-2] == "page" and self.cur_tag == "id"):
			self.data = re.sub( '\n', '', self.data )
			self.id = int(self.data)
			title_file.write(str(self.id)+":"+self.title + "\n")
		elif(self.cur_tag == "title"):
			self.data = re.sub( '\n', ' ', self.data )
			self.title = self.data.lower()
		#	print type(self.id)

		elif(self.cur_tag == "text"):
			self.text = self.data
			self.parse()
			self.write_dict()

		self.data = ""
	#	print self.stack

		self.stack.pop()
	#	print "Hi"
	#	print self.stack
		self.cur_tag = self.stack[-1]

	# Call when a character is read
	def characters(self, content):
		unicode_content = content.encode("utf-8").strip()
		if unicode_content:
			self.data += unicode_content+'\n'

	def parse(self):
		global stop_set
		lines = self.text.split('\n')

		flag = 0
		ans = 0
		for line in lines:
			line = line.lower()

			if flag <=2 and "{{infobox" in line:										#flag = 1 write infobox
				flag = 1
			elif flag == 1 and (line == "}}" or line =="\n"):
				flag = 2

			elif flag == 2 and ("==reference" in line or "== reference" in line):		#flag = 3 for reference
				flag = 3
	
			elif flag == 3 and line == "\n":
				flag = 4

			elif flag <= 4 and "[[category" in line:									#flag = 5 for category
				flag = 5

			elif flag <= 6 and ("==external" in line or "== external" in line):
				flag = 7

			elif flag == 7 and line == "\n":
				flag = 8

			elif flag == 5 and "[[category" not in line:
				flag = 6

			if flag>-1 and (flag%2) == 0 and line != "\n":
				self.body += line + '\n'

			if(flag == 1):
				self.infobox += line + '\n' 

			if(flag == 3) and ("== reference" not in line and "==reference" not in line):
				self.ref += line+"\n"

			if(flag == 5):
				x = line.split(':')
				try:
					self.category = self.category + x[1][:len(x[1])-2]+"\n"
				except:
					continue
			
			if(flag == 7):
				self.links += line+"\n"				

		# print "*************TITLE****************"
		# print self.title
		# print "*************CATEGORY****************"
		# print "*************INFOBOX****************"
		# print "*************INFOBOX****************"
		# print "*************INFOBOX****************"
#		if(self.id == 2070):
#			print self.title
		self.title = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.title) if len(j)>0]
		self.infobox = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.infobox) if len(j)>0]
		self.body = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.body) if len(j)>0]
		self.ref = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.ref) if len(j)>0]
		self.links = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.links) if len(j)>0]
		self.category = [j.strip() for j in re.compile(r'[^A-Za-z0-9]+').split(self.category) if len(j)>0]

		self.title = [stem.stemWord(x) for x in self.title if stem.stemWord(x) not in stop_set]
		self.infobox = [stem.stemWord(x) for x in self.infobox if stem.stemWord(x) not in stop_set]
		self.body = [stem.stemWord(x) for x in self.body if stem.stemWord(x) not in stop_set]
		self.ref = [stem.stemWord(x) for x in self.ref if stem.stemWord(x) not in stop_set]
		self.links = [stem.stemWord(x) for x in self.links if stem.stemWord(x) not in stop_set]
		self.category = [stem.stemWord(x) for x in self.category if stem.stemWord(x) not in stop_set]
#		if(self.id == 2070):
#			print self.title

	def write_dict(self):
		global dict_title, dict_body, dict_infobox, dict_category, dict_links, dict_ref

		words = set(self.title)
#		if(self.id == 2070):
#			print words

		for word in words:
#			if(self.id == 2070):
#				try:
#					print dict_title[word]
#				except:
#					print word
			if word not in dict_title:
				dict_title[word] = "1$" + str((self.id)) + ":" + str(self.title.count(word))
			else:
				str1 = dict_title[word]
				cnt = int(str1.split('$')[0])
				dict_title[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.title.count(word))
#			if(self.id == 2070):
#					print dict_title[word]
#		if(self.id == 2070):
#				print words

		words = set(self.body)

		for word in words:
			if word not in dict_body:
				dict_body[word] = "1$" + str((self.id)) + ":" + str(self.body.count(word))
			else:
				str1 = dict_body[word]
				cnt = int(str1.split('$')[0])
				dict_body[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.body.count(word))

		words = set(self.infobox)

		for word in words:
			if word not in dict_infobox:
				dict_infobox[word] = "1$" + str((self.id)) + ":" + str(self.infobox.count(word))
			else:
				str1 = dict_infobox[word]
				cnt = int(str1.split('$')[0])
				dict_infobox[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.infobox.count(word))

		words = set(self.category)

		for word in words:
			if word not in dict_category:
				dict_category[word] = "1$" + str((self.id)) + ":" + str(self.category.count(word))
			else:
				str1 = dict_category[word]
				cnt = int(str1.split('$')[0])
				dict_category[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.category.count(word))

		words = set(self.ref)

		for word in words:
			if word not in dict_ref:
				dict_ref[word] = "1$" + str((self.id)) + ":" + str(self.ref.count(word))
			else:
				str1 = dict_ref[word]
				cnt = int(str1.split('$')[0])
				dict_ref[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.ref.count(word))

		words = set(self.links)

		for word in words:
			if word not in dict_links:
				dict_links[word] = "1$" + str((self.id)) + ":" + str(self.links.count(word))
			else:
				str1 = dict_links[word]
				cnt = int(str1.split('$')[0])
				dict_links[word] = str(cnt+1) + str1[len(str(cnt)):] + "$" + str((self.id)) + ":" + str(self.links.count(word))


def clear_dict():
	global dict_title, dict_infobox, dict_category, dict_ref, dict_links, dict_body
	dict_title.clear()
	dict_infobox.clear()
	dict_body.clear()
	dict_ref.clear()
	dict_links.clear()
	dict_category.clear()

def close_file():
	global file_infobox, file_title, file_category, file_ref, file_body, file_links
	file_title.close()
	file_infobox.close()
	file_body.close()
	file_ref.close()
	file_links.close()
	file_category.close()

def main():
	global stop_set, docs_max, file_count,cont
	global dict_title, dict_infobox, dict_category, dict_ref, dict_links, dict_body
	global file_infobox, file_title, file_category, file_ref, file_body, file_links
#		global total_no_document

	stop_words_set()	
	# create an XMLReader
	parser = xml.sax.make_parser()
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	# override the default ContextHandler
	Handler = My_Wiki_Handler()
	parser.setContentHandler( Handler )
	parser.parse("corpus2.xml")

	string_infobox = ""
	string_title = ""
	string_category = ""
	string_body = ""
	string_ref = ""
	string_links = ""

	for word in sorted( dict_title.keys() ):
		string_title = word + "=" + dict_title[word] + '\n'
		file_title.write(string_title)

	for word in sorted( dict_infobox.keys() ):
		string_infobox = word + "=" + dict_infobox[word] + '\n'
		file_infobox.write(string_infobox)

	for word in sorted( dict_category.keys() ):
		string_category = word + "=" + dict_category[word] + '\n'
		file_category.write(string_category)

	for word in sorted( dict_body.keys() ):
		string_body = word + "=" + dict_body[word] + '\n'
		file_body.write(string_body)

	for word in sorted( dict_ref.keys() ):
		string_ref = word + "=" + dict_ref[word] + '\n'
		file_ref.write(string_ref)

	for word in sorted( dict_links.keys() ):
		string_links = word + "=" + dict_links[word] + '\n'
		file_links.write(string_links)

	clear_dict()	
	close_file()
	print "Merging Begins"
	merge.merge(file_count)
	os.system("rm index/body* index/category* index/infobox* index/title* index/ref* index/links*")

	print cont
main()