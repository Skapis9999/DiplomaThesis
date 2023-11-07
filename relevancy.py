from urllib.request import urlopen
from urllib.request import Request


#@title relevancy and similarity functions

# relevancy function that finds if the important_words are in each page
# True if at least one exists False if none does
def relevancy(txt, important_word,url,manual):
        relevant = False
        for word in important_word:
          if manual:
            if important_word in txt:
              print("Page", url, "is  related to important word:", important_word)
              relevant = True
              break
            else:
              print("Page", url, "is  not related to important word:", important_word)              
              break
          else:
            if (word in txt): 
              print("Page", url, "is  related to word:", word)
              relevant = True
              break
            else:
              print("Page", url, "is not related to word:", word)
              relevant = False
        return relevant
  
# relevancy function that gives a score based on vectors
def pairwiseSimilarity(txt,question):
        from sklearn.feature_extraction.text import TfidfVectorizer
                                                                                                                                                                                          
        vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
        tfidf = vect.fit_transform([question, txt])                                                                                                                                                                                                                       
        pairwise_similarity = tfidf * tfidf.T 
        print("pairwise_similarity", pairwise_similarity.toarray()[1][0])
        return pairwise_similarity.toarray()[1][0]

# relevancy function that finds if the important_words are in the meta part of each webpage
# True if at least one exists False if none does
def metaDataRelevancy(url,important_word):
  from lxml import etree

  # gets the web page
  req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
        )
  f = urlopen(req).read()

  # parse the meta part of the page
  try:
    tree = etree.HTML( f )
    m = tree.xpath( "//meta" )
  except:
    return False
  # tree.xpath( "//meta[@name='Keywords']" )[0].get("content")    # example of info

  # transfer metadata to a list
  metaData = []
  for i in m:
    metaData.append(etree.tostring(i))
  # print("The metadata are", metaData)
  # print(type(important_word))
  # print(type(metaData))
  outputMetaData =[]
  for item in metaData:
    # print(type(item))
    outputMetaData.append(item.decode())
  metaDataString = " ".join(outputMetaData)
  # print(type(metaData))
  # print(type(a))
  relevant = False
  resStr = isinstance(important_word, str)
  resList = isinstance(important_word, list)

  # if important_word is a list find relevancy.
  # return True if one important_word exists in the metadata
  if resList:
    for word in important_word:
      if (word in metaDataString): 
        print("Meta Page", url, "is  related to word:", word)
        relevant = True
        break
      else:
        print("Meta Page", url, "is not related to word:", word)
        relevant = False
  
  # if important_word is a string find relevancy.
  # return True if the important_word exists in the metadata
  elif resStr:
    if (important_word in metaDataString): 
        print("Meta Page", url, "is  related to word:", important_word)
        relevant = True
    else:
        print("Meta Page", url, "is not related to word:", important_word)
        relevant = False
  # return none if there is no important_word
  elif important_word is None:
    print("important_word is empty")
  else:
    print("important_word is neither string nor a list")
  return relevant          


