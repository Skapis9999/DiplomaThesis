#@title answer and print functions

import time
from findSource import findSource


# function that answers the question linearly. Very slow with many data.
def answer_question(data,oracle,question):
  # print(data)
  print("Data size is: ", len(data))

  counter = 0                 # counter to use with the stem in the while loop
  l = len(data)               # lenth of the data variable
  cr = []                     # context results   

  step = 3                    # Step. It says how many lines it combines per answer 
  i = 0                       # Current position
  start_test = time.time()

  if step == 1:
    for words in data:
      counter+=1
      print(counter, " out of ", l)
      cr.append(oracle(question=question, context=words))
  # '''
  # if step = n
  # while current position is smaller than lenth
  # if the next position is the end then then the current step is the answer
  # else if the next position is not the end
  # then answer with the current and the next lines
  # ''' 
  elif step == 2:
    while i<l:
      if(i+1)==l:
        cr.append(oracle(question=question, context=data[i]))
        break
      counter+=2
      print(counter, " out of ", l)
      cr.append(oracle(question=question, context=data[i]+data[i+1]))
      i=i+2
  elif step == 3: 
    while i<l:
      if(i+1)==l:
        print('In the last iteration I had one data')
        cr.append(oracle(question=question, context=data[i]))
        break
      if(i+2)==l:
        print('In the last iteration I had two data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]))
        break
      counter+=3
      print(counter, " out of ", l)
      cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]))
      i=i+3
  elif step == 4:
    while i<l:
      if(i+1)==l:
        print('In the last iteration I had one data')
        cr.append(oracle(question=question, context=data[i]))
        break
      if(i+2)==l:
        print('In the last iteration I had two data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]))
        break
      if(i+3)==l:
        print('In the last iteration I had three data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]))
        break
      counter+=4
      print(counter, " out of ", l)
      cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]+data[i+3]))
      i=i+4
  elif step == 5:
    while i<l:
      if(i+1)==l:
        print('In the last iteration I had one data')
        cr.append(oracle(question=question, context=data[i]))
        break
      if(i+2)==l:
        print('In the last iteration I had two data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]))
        break
      if(i+3)==l:
        print('In the last iteration I had three data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]))
        break
      if(i+4)==l:
        print('In the last iteration I had four data')
        cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]+data[i+3]))
        break
      counter+=5
      print(counter, " out of ", l)
      cr.append(oracle(question=question, context=data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]))
      i=i+5

  end_test = time.time()
  print(end_test - start_test, ' seconds lapsed')
  return [cr, step]

# print the answers that the model extracted
def print_answers(data, cr, step, dataFile="dataT.txt"):
  # print(cr)
  # print(len(cr))

  final_results = []

  # keep answer with score higher than 0.1 out of 1
  limit = 0.1
  for i in range(len(cr)):
    if cr[i]['score']>limit:
      final_results.append(cr[i])
      cr[i]['index']=i
      
  # print(len(final_results))
  # print(final_results)

  print("--------------------------")
  table = []

  # final results sorted by score
  final_results_sorted = sorted(final_results, key=lambda d: d['score'], reverse=True)
  for item in final_results_sorted:
    print("The answer", item['answer'], "is correct with a chance of", item['score']*100, "%")
    # print for step == 1
    if step == 1:
      i = item['index']
      if i == 0:
        context = data[0]+" "+data[1]
      elif i == len(cr) - 1:
        context = data[len(cr)]+" "+data[len(cr) - 1]
      else:
        context = data[i-1]+" "+data[i]+" "+data[i+1]
      print("We use step ", step)
      print("Context:", context)
      url = findSource(exit_counter=i, i=None,useHaystack=False,dataFile =dataFile)
      table.append([item['answer'], item['score'], url, context])
      continue
    # print for step > 1
    if(item['index']>(len(cr))-step):
      i = item['index']
      # get context
      context = data[i]+" "+data[i+1]
      # find source function to get the url of the website of the source
      url = findSource(exit_counter=i, i=None,useHaystack=False,dataFile =dataFile)
      # append answer, score, url of source and context in a table
      table.append([item['answer'], item['score'], url, context])
      continue
    else:
      context = ' '
      i = item['index']
      for k in range(step):
        context=context+data[step*i+k]+" "
      print("We use step ", step)
      print("Context:", context)
      url = findSource(exit_counter=i, i=None,useHaystack=False,dataFile =dataFile)
      table.append([item['answer'], item['score'], url, context])
      continue
  print("----------------")
  from tabulate import tabulate
  # for i in range(len(prediction['answers'])):
  #   exit_counter = answer_question_heystack(prediction, i)
  #   answer1 = findSource(exit_counter,i)

  # print tabulated a table with the results
  print(tabulate(table, headers = ['Answer', 'Score', 'url', 'Context'], tablefmt="grid"))