from quick_answer_serp import quick_answer_serp
from importantWordAndSearch import findImportantWord, findImportantWordBert,searchAuto, slowSearch
from relevancy import relevancy, pairwiseSimilarity, metaDataRelevancy
from createCsv import create_csv
from search import line_prepender,findLinks, addCleanLinks, search_str, depthSearch,\
    returnRelevantTxt, htmlToText, loopInDepthSimilarity, removeDuplicateLines, depthSimilarity
from encyclopaedia import buildEncyclopaedia, gatherData, cleanEncyclopaedia    
from answer import answer_question, print_answers 
# import findSource ## it may be needed
from findSource import findSource
from heystackCode import heystack_question, answer_question_heystack

#@title Question and Important Word

import time

with open('readme.txt', 'w') as f:
    f.write('Create a new text file!')

print('+++++++++++++++')
import pathlib
print(pathlib.Path().resolve())    
print('+++++++++++++++')

# counting total time
start_total = time.time()

# language to search
lang = 'en'

# Directory
dic = "flask/Data/"

# webpage to search on and the question
# url is not necessary if it is not in manual mode 

# url ='https://en.wikipedia.org/wiki/Dashuigou_Formation'
question = 'What is The Dashuigou Formation?'
# url ='https://en.wikipedia.org/wiki/Newtown_Township,_Delaware_County,_Pennsylvania'
# question = 'Where is Newtown Township?'
# url ='https://en.wikipedia.org/wiki/Athens_Tram'
# question = 'When did the first extension of the Athens Tram take place?'
# url ='https://en.wikipedia.org/wiki/Socrates'
# question = 'When did Socrates die?'
# url ='https://en.wikipedia.org/wiki/Jenson_Button'
# question = 'Where was the first Grand Prix victory of Jenson Button?'
# question = 'Which is the capital of Greece'
# question = 'Who is Evangelia Ritzaleou?'
# url = 'https://www.judithsreadingroom.org/freedom-through-literacy-award/'

# very quick answer. Limited results per month. Enable !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# startQuick = time.time()
# quick_answer_serp(question)
# endQuick = time.time()
# print(endQuick - startQuick, ' seconds lapsed for Quick')

import os
from haystack.document_stores import ElasticsearchDocumentStore

# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document"
)
print("----------------ElasticsearchDocumentStore Initialized----------------")
[important_word,target_websites] = slowSearch(question,lang)

#@title imports and removing files

import transformers
import re
from pathlib import Path
from transformers import pipeline
from urllib.request import urlopen
import urllib
from urllib.request import Request
import time
import elasticsearch

import os
import glob

# delete all files from previous runs
directory = '/home/chris/Documents/diplomaThesis/flask/Data'
file_pattern = '*.txt'

# Find all .txt files in the directory
files = glob.glob(os.path.join(directory, file_pattern))
# print(files)

# Delete each file
for file in files:
    os.remove(file)

# print them 
print("------Files in the directory. It should contain no .txt files------")
cmd = "ls -al /home/chris/Documents/diplomaThesis/flask/Data"
os.system(cmd)
print("------")

import pandas as pd

df = pd.DataFrame(columns=['Page', 'Pairwise Similarity', 'Existance', 'Meta Existance'])

#@title Parcing Main

start = time.time()

url = target_websites[0]
print("-----Starting parsing webpages-----")
htmlToText(important_word,0,url,df,question,"htmlToTextFast.txt",False,False,dic,1 , "EncyclopaediaFast.txt")
print("-----Ending parsing webpages-----")
print("-----Starting building Enc-----")
buildEncyclopaedia(enc = "EncyclopaediaFast.txt", encOut = "EncyclopaediaFastOut.txt",dic=dic)
print("-----Ending building Enc-----")

dataFast = cleanEncyclopaedia(encOut="EncyclopaediaFastOut.txt", dataFile = 'dataTFast.txt',dic=dic)

fastEncTime = time.time()
print(fastEncTime - start, ' seconds lapsed for fast enc')

startFastTime = time.time()
useHaystack = True
if useHaystack:
  predictionFast = heystack_question(document_store,question, dic+"dataTFast.txt")
else:
  oracle = pipeline(model="deepset/roberta-base-squad2")
  [cr, step] = answer_question(dataFast,oracle,question)

fastTime = time.time()
print(fastTime - startFastTime, ' seconds lapsed for fast')


startFastTimeAnswer = time.time()
if useHaystack:
  table = []
  for i in range(len(predictionFast['answers'])):
    exit_counter = answer_question_heystack(predictionFast, i, dataFile = dic+'dataTFast.txt')
    answer1Fast = findSource(predictionFast,exit_counter,i,useHaystack, dataFile = dic+'dataTFast.txt')
    table.append([answer1Fast.answer, answer1Fast.score, url, answer1Fast.context])
  print(question)
  from tabulate import tabulate
  print(tabulate(table, headers = ['Answer', 'Score', 'url', 'Context'], tablefmt="grid"))
else:
  print_answers(dataFast, cr, step, dataFile = dic+'dataTFast.txt')

fastTimeAnswer = time.time()
print(fastTimeAnswer - startFastTimeAnswer, ' seconds lapsed for fast answer')


print("--------------------")
print("Second stage with multiple websites begins")
print("--------------------")
parallel = False

startFullDepthSimilarity = time.time()
if parallel:
  print("-----Starting parsing webpages-----")
  a = depthSimilarity(url,question,df,target_websites,important_word,parallel)
  print("-----Ending parsing webpages-----")
  for item in a:
    file1 = open(dic+"Encyclopaedia.txt", "a")  # append mode
    try:
      file1.write(item)
    except TypeError:
      print(None)
    file1.close()
else:
  print("-----Starting parsing webpages-----")
  depthSimilarity(url,question,df,target_websites,important_word)
  print("-----Ending parsing webpages-----")

end = time.time()

print(fastEncTime - start, ' seconds lapsed for fast enc')
print(fastTime - startFastTime, ' seconds lapsed for fast')
print(fastTimeAnswer - startFastTimeAnswer, ' seconds lapsed for fast answer')
print(end-startFullDepthSimilarity, ' seconds lapsed for rest of the sources')
print(end - start, ' seconds lapsed')

print("-----Starting building Enc-----")
buildEncyclopaedia()
data = cleanEncyclopaedia()
print("-----Ending building Enc-----")

useHaystack = True
if useHaystack:
  prediction = heystack_question(document_store,question, dic+"dataT.txt")
else:
  [cr, step] = answer_question(data,oracle,question)

  useHaystack = True
if useHaystack:
  for i in range(len(prediction['answers'])):
    exit_counter = answer_question_heystack(prediction, i,dataFile = dic+'dataT.txt')
    answer1 = findSource(prediction,exit_counter,i,useHaystack,dataFile = dic+'dataT.txt')
    table.append([answer1.answer, answer1.score, answer1.url, answer1.context])

  print(question)
  from tabulate import tabulate
  print(tabulate(table, headers = ['Answer', 'Score', 'url', 'Context'], tablefmt="grid"))
else:
  print_answers(data, cr, step,dataFile = dic+'dataTFast.txt')