#@title Important Word and Search functions

from googlesearch import search

def findImportantWord(question, bert=False):
  import nltk

  # create tokens and find tags
  tokens_question = nltk.word_tokenize(question)
  tagged = nltk.pos_tag(tokens_question)
  # print(tagged)

  # if 
  if bert:
    return tagged
  else:
    pass

  important_word=[]
  # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for tags
  for item in tagged:
    # keep N and JJ which are Noun and Adjective
    if ('N' in item[1]) or ('JJ' in item[1]):
      important_word.append(item[0])
      # remove not useful words
      if("be" in important_word[-1]) or ('is' in important_word[-1]) or ("are" in important_word[-1]) \
      or ("am" in important_word[-1]) or ("was" in important_word[-1]) or ("been" in important_word[-1]) \
      or ("were" in important_word[-1]) or ("of" in important_word[-1]):
        del important_word[-1]
  return important_word

def findImportantWordBert(question):

  from keybert import KeyBERT

  # get bert importance
  kw_model = KeyBERT()
  keywords = kw_model.extract_keywords(question)

  important_words = []

  for word in keywords:
    # get tagged words
    bertWords = findImportantWord(word[0], True)

    # keep N and JJ which are Noun and Adjective and of importance >0.1 
    if ((('N' in bertWords[0][1]) or ('JJ' in bertWords[0][1]))and word[1]>0.1):
      important_words.append(bertWords[0][0])

  return important_words

# query is the query for the question, lang is the language to search, num and stop is the number of the results, pause is ???
def searchAuto(query, lang, num, stop, pause):
  target_websites = []
  clean_websites = []
  print("------")
  print("I search with this query:", query)
  print("I have the following results:")
  print("------")
  search_list = search(query, lang=lang, num=num, stop=stop, pause=pause)
  for j in search_list:
    target_websites.append(j)
    text_before_hash = j.split("#")[0]
    if text_before_hash in clean_websites:
      continue
    clean_websites.append(j)
    if len(clean_websites) == 5:
      break
    print(j)
  print("------")
  # print(target_websites)
  print(clean_websites)
  return clean_websites

def slowSearch(question,lang,website_link,website):

  import time
  target_websites = []

  start = time.monotonic()

  # Search Params
  manual_link = False                   # False if url is found automatically
  # website_link = False                  # True if you want to search only in a specific website
  # website = " site:en.wikipedia.org"    # The website you want to search in if website_link == True
  if manual_link:
    target_websites.append(url)
  else:
    if website_link:
      query = question + website
    else:
      query = question
    target_websites = searchAuto(query, lang, 10, 10, 2)
    url = target_websites[0]

  searchAutoTime = time.monotonic()

  # important_words are used to check for useful links in the main page
  manual = True # True if you set the keyword  
  if manual:
    important_word = "None"      # select the word manually
  else:
    important_word = findImportantWord(question)                # extract important words
    print("The most important phrases are:", important_word)    # print important words
    print("------")

  findImportantWordTime = time.monotonic()

  s1 = searchAutoTime - start
  s2 = findImportantWordTime - searchAutoTime
  
  print("searchAuto lasted",  s1, " seconds")
  print("findImportantWord lasted  ",  s2, " seconds")
  
  return [important_word,target_websites]