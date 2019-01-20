#!/usr/bin/python3

import sys
import re
import json
import fileinput
import math
import nltk
import csv

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = []
doclength = []

def main():
	# code for testing offline	
	if len(sys.argv) < 2:
		print ('usage: ./retriever.py term [term ...]')
		sys.exit(1)

	read_index_files()

	query_terms = []
	query_results = [] 
	arg = ''.join(sys.argv[1:])
	#counter = 1
	if '.txt' in arg:
		for line in fileinput.input(arg):
			query_terms = line.strip()
			string_query = ''.join(query_terms)
			query_terms = nltk.word_tokenize(string_query)
			results = retrieve_vector(query_terms)
			query_results.append(results)
			#counter += 1
	else:
		query_terms = sys.argv[1:]
		results = retrieve_vector(query_terms)
		query_results.append(query_terms)

	counter = 1
	endList = []
	for i in query_results:
		counterTwo = 0
		for j in i:
			tempList = []
			counterTwo +=1
			tempList.append(str(counter))
			tempList.append(str(counterTwo))
			tempList.append(j)
			print(tempList, 'templist')
			endList.append(tempList)
		counter += 1

	with open('testCsvIR.csv', 'w') as f:
		w = csv.writer(f)
		w.writerows(endList)


def read_index_files():
	## reads existing data from index files: docids, vocab, postings
	# uses JSON to preserve list/dictionary data structures
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclength
	# open the files
	in_d = open('docids.txt', 'r')
	in_v = open('vocab.txt', 'r')
	in_p = open('postings.txt', 'r')
	in_l = open('doclengths.txt', 'r')
	# load the data
	docids = json.load(in_d)
	vocab = json.load(in_v)
	postings = json.load(in_p)
	doclength = json.load(in_l)
	# close the files
	in_d.close()
	in_v.close()
	in_p.close()
	
	return
	
	
def retrieve_vector(query_terms):
	## a function to perform Boolean retrieval
	# assumes the postings lists are lists, not dicts
	
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclength


	idf_List = []
	scores = [0] * len(docids)
	print(query_terms, 'query terms')
	for term in query_terms:
		if term in vocab:
			#print(vocab.index(term), 'termID')
			idf = math.log10(len(docids)/float(len(postings[str(vocab.index(term))])))
			idf_List.append(str(idf))
			post = postings[str(vocab.index(term))]
			for i, v in post.items():
				docId = int(i)
				fre = int(v)
				docTerms = doclength[docId]
				tf = fre/docTerms
				tfIdf = tf * idf
				scores[docId] += tfIdf
		else:
			print(term, ' not in vocab')

	counterIt = 0
	while counterIt < len(docids):
		scores[counterIt] = scores[counterIt]/doclength[counterIt]
		counterIt += 1

	answer = [] * 10
	counterAll = 0
	while counterAll < 10:
		maximum = scores[0]
		index = 0
		counter = 0
		for tfIdf in scores:
			if tfIdf > maximum:
				maximum = tfIdf
				index = counter
			counter += 1
		answer.append(docids[index])
		scores[index] = 0
		counterAll += 1

	return answer
		
	# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()
	

