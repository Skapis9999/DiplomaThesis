#@title finds source

def findSource(prediction, exit_counter, i,useHaystack,dataFile = "dataT.txt"):
  # results from Haystack
  if useHaystack:
    # try:  
    #   # print('exit counter = ', exit_counter)
    #   pass
    # except NameError:
    #   print("Model failed?")
    file = open(dataFile,'r')
    counter = 0
    for line in file.readlines():
      # '!@#$%^' is before the url
      if '!@#$%^' in line:
        x = line.split('!@#$%^',1)
        y = x[1].split('.html',1)
        url = y[0]
      if counter == exit_counter:
        break 
      counter +=1
    if exit_counter == 0:
      url = None
    file.close()

    answer1 = Answer(prediction['answers'][i].answer, prediction['answers'][i].score, prediction['answers'][i].context, url)
    print("Answer is:", answer1.answer)
    print("Score is:", answer1.score)
    print("Context is:", answer1.context)
    print("Source is :", answer1.url)
    print("")
    return answer1
  # results from manual way
  else:
    url = "None"
    file = open(dataFile,'r')
    counter = 0
    for line in file.readlines():     
      if '!@#$%^' in line:
        x = line.split('!@#$%^',1)
        y = x[1].split('.html',1)
        url = y[0]
      if counter == exit_counter:
        file.close()
        return url 
      counter +=1
    file.close()
    if i == 0:
      url = "None, i is 0"
      return url
    return url

class Answer:
  answer = "No answer"
  score = "No score"
  context = "No context"
  url = "No url"

  def __init__(self, answer, score, context, url):
    self.answer = answer
    self.score = score
    self.context = context
    self.url = url

  def __str__(self) -> str:
     return f"{self.answer}{self.score}{self.context}{self.url}"