#@title quick_answer_serp

def quick_answer_serp(question):
  import requests
  import json
  from transformers import pipeline
  # set up the request parameters
  params = {
    'api_key': '33AA2074BA62409E8A30D79ACB2350AA',
    'location': 'New York,New York,United States',
    'q': question
  }

  # make the http GET request to Scale SERP
  api_result = requests.get('https://api.scaleserp.com/search', params)

  # print the JSON response from Scale SERP
  # print(json.dumps(api_result.json()))

  exit_counter = 0
  # source: https://www.scaleserp.com/?gclid=Cj0KCQiA0oagBhDHARIsAI-BbgdCGXfNs58Tm8ijvm2Om9d7djHNZQJZfjRhuslMRnfWLm1i9el982QaApf7EALw_wcB
  # print the knowledge_graph information
  print('------------------Knowledge Box Start-----------------------')
  try:
    print("The description of the knowledge box is: ", api_result.json()['knowledge_graph']['description'])
  except KeyError:
    print("There is no knowledge box")
    exit_counter+=1
  print('------------------Knowledge Box End-----------------------')

  # print the related_questions 
  print('------------------Related Questions Start-----------------------')
  try:
    for item in api_result.json()['related_questions']:
      print("The question is: ", item['question'])
      print("The answer is: ", item['answer'])
  except KeyError:
    print("There is no related question")
    exit_counter+=1
  print('------------------Related Questions Start-----------------------')

  # exit if both none of these exists
  if exit_counter == 2:
    return None
  else:
    pass

  # ask the question using the model deepset/roberta-base-squad2
  question = question
  oracle = pipeline(model="deepset/minilm-uncased-squad2")

  early_answers=[]

  # answer the question via knowledge_graph
  try: 
    early_answers.append(oracle(question=question, context=api_result.json()['knowledge_graph']['description']))
  except:
    print("There is no description")

  # answer the question via related_questions
  try:
    for item in api_result.json()['related_questions']:
      # print(item['question'])
      # print(item['answer'])
      early_answers.append(oracle(question=question, context=item['answer']))
  except:
    print("No questions")

  show_all = 0              # print all the answers
  show_best = 1             # prin all the answers with score over 
  minimum_score = 0.0001    # minimum score that will be printed for show_best

  print("eartly_answers = ", early_answers)
  if len(early_answers)==0:
    return [["No answer", 0, "no url", "no context"]]

  # print answer
  answers=[]
  for item in early_answers:
    if item['score']>minimum_score*show_all:
      print('1',item)
      print('2', item['answer'])
      print('3', item['score'])
      item_temp = [item['answer'],item['score']]
      answers.append(item_temp)

  print('The answers are:', answers)
  return answers

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was
