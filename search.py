import re
import pandas as pd

from urllib.request import urlopen
from urllib.request import Request
from relevancy import relevancy, pairwiseSimilarity, metaDataRelevancy
from createCsv import create_csv



#@title parcing functions

# write our links in the first position of "links.txt"
def line_prepender(filename, target_websites, dic="Data/"):
    with open(dic+filename, 'w') as f:
      for line in target_websites[1:]:
        f.write(f"{line}\n")

# find all links and store them in the links file which has to be "links.txt" while the source is file_path file which has to be "temp.txt"
def findLinks(file_path,links,dic="Data/"):
  with open(file_path, 'r', encoding="utf-8") as file:
        # read all content of a file
        content = file.read()
        # find all urls
        linksFound =  re.findall(r'(https?://[^\s]+)', content)
        # write all urls in 
        f = open(dic+links, "a", encoding="utf-8")
        for item in linksFound:
            f.write("%s\n" % item)
        f.close()

# data preprocessing of links that are not useful
def addCleanLinks(f,file1):
  # keep only english wikipedia links
  for line in f:
            # list_of_illegal_words = ['static','ichef',\
            #   '//', 'donate.wikimedia', 'wikimedia', 'wikimediafoundation',\
            #   'mediawiki', 'premium.britannica', 'beyond.britannica',\
            #   'https://twitter.com/britannica', 'https://www.facebook.com/BRITANNICA/',\
            #   'https://schema.org', 'insitez.blob.core.windows', '3-88/js', '3-88/dist',\
            #   '3-88/', 'googletagmanager', '.pdf', '.PDF', 'archive.org/details', '.apng',\
            #   '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png',\
            #   '.svg', '.webp', '.bmp', '.ico', '.cur', '.tif', 'doi.org', 'jstor.org',\
            #   'creativecommons.org', 'semanticscholar.org', 'books.google.com'
            # ]

            # if any(word in line for word in list_of_illegal_words):
            #    print(line)
            #    continue

            if ('.wikipedia' in line) and ('en.wikipedia' not in line): 
                continue
            # remove some specific unrelated pages
            if ('static' in line) or ('ichef' in line): 
                continue
            if ('//' not in line) or ("donate.wikimedia" in line) \
            or ("donate.wikimedia" in line) or ("foundation.wikimedia" in line)\
            or ("developer.wikimedia" in line) or ("stats.wikimedia" in line)\
            or ("wikimediafoundation" in line) or ("mediawiki" in line)\
            or ("premium.britannica." in line) or ("https://beyond.britannica.com" in line)\
            or ("https://schema.org" in line) or ("https://www.facebook.com/BRITANNICA/" in line)\
            or ("https://twitter.com/britannica" in line) or ("insitez.blob.core.windows" in line)\
            or ("3-88/js" in line) or ("3-88/dist" in line) or (".googletagmanager.com" in line)\
            or (".pdf" in line) or (".PDF" in line) or ("archive.org/details" in line)\
            or (".apng" in line) or (".avif" in line) or (".gif" in line)\
            or (".jpg" in line) or (".jpeg" in line) or (".jfif" in line)\
            or (".pjpeg" in line) or (".pjp" in line) or (".png" in line)\
            or (".svg" in line) or (".webp" in line) or (".bmp" in line)\
            or (".ico" in line) or (".cur" in line) or (".tif" in line)\
            or ("doi.org" in line) or ("jstor.org" in line) or ("creativecommons.org" in line)\
            or ("semanticscholar.org" in line) or ("books.google.com" in line): 
              continue
            # some wiki sites have an extra part at the end
            if ('wiki' in line) and ('&amp' in line): 
                line = line.split('&amp')[0]  
            # some wiki sites have an extra part at the end
            if ('wiki' in line) and ('#sitelinks' in line): 
                line = line.split('#sitelinks')[0]
            if '\"' in line:
                pos = line.find('\"')
                # print(line[:pos])
                new_line = line[:pos]
                if '\n' in new_line[-2:]:
                  new_line = new_line[-2:]
                file1.write(new_line)
                file1.write("\n")
            else:
                # print(line)
                file1.write(line)
                file1.write("\n")


# Reads html of a webpage and extracts hypelinks
# Finds all hyperlinks and urls in the file and it stores them in a file named "links.txt"
def search_str(file_path,links,url,target_websites, dic="Data/"):

    # write our links returned from searchAuto in the first position
    line_prepender(links,target_websites, dic)

    # gathering links from the first page
    gatherLinks = False

    if gatherLinks:
      try:
        # find all the links and store them in file_path
        findLinks(file_path,links, dic)
      except:
        print("No primary Page")

    with open(dic+'links.txt', 'r+', encoding="utf-8") as f:
        file1 = open(dic+"cleanLinks.txt", "a")  # append mode
        addCleanLinks(f,file1)
        file1.close()

# Creates a file named "html.txt" that includes the html of the page
# Finds all hyperlinks and urls in the file and it stores them in a file named "links.txt
def depthSearch(url,target_websites, dic="Data/"):    
    import fileinput
    from bs4 import BeautifulSoup

    try:
      req = Request(
          url=url,
          headers={'User-Agent': 'Mozilla/5.0'}
      )
      page = urlopen(req).read()
      soup = BeautifulSoup(page, "lxml")
      body = soup.find('body')
      the_contents_of_body_without_body_tags = body.findChildren(recursive=False)
      # open(dic+"temp.txt", "w").close()
      f = open(dic+"temp.txt", "w", encoding="utf-8")
      f.write(str(the_contents_of_body_without_body_tags))
      f.close()
    except:
       print("LinkedIn is not supported")

    file_path="temp.txt"

    search_str(dic+file_path,"links.txt",url,target_websites)
    

# tag URLs and return text if relevant
def returnRelevantTxt(url, txt0, prefixUrl="!@#$%^", relevant=True):
  # tag the url with the special tag "!@#$%^" if relevant
      if relevant:
        txt = "\n" + prefixUrl + url + "\n" + txt0
      # return empty string if not relevant  
      else:
        txt = ""
        return None
      # just return the txt
      return txt


# retrieves text from a website and it stores it in a file named htmlToText.txt
def htmlToText(important_word, counter, url, df,question, file_name="htmlToText.txt",manual = True, parallel = False, dic="Data/", wait_second = 1, enc = "Encyclopaedia.txt"):
    import urllib.request
    import gc
    from bs4 import BeautifulSoup
    from urllib import request
    from urllib.request import Request, urlopen
    ########################################

    x = 0
    # get the availability of a website
    if "linkedin" in url:
      print("LinkedIn is not supported")
      print("---------------")
      return None
    try:
      req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
      )
      # get wait_second seconds to get a site or skip it
      x = urllib.request.urlopen(req, timeout=wait_second).getcode()
    except:
      print("Too slow and return")
      print("---------------")
      return None
    # garbage collector
    gc.collect()
    if x == 200:
      print("200 and pass")
      print("---------------")
      pass
    else:
      print("Not 200 and return")
      print("---------------")
      return None
    
    # parse the website
    req = Request(
    url=url, 
    headers={'User-Agent': 'Mozilla/5.0'}
    )

    try:
      soup = BeautifulSoup(urlopen(req).read(),features="lxml")
      txt0 = soup.get_text()
    except:
      txt0 = " None "
      print ("An error occurred")

    
    # # text similarity 
    # pairwise_similarity = pairwiseSimilarity(txt0,question)
    # # solution with important word
    # relevant = relevancy(txt0,important_word,url,manual)
    # # solution with important word in metaData
    # relevantMeta = metaDataRelevancy(url,important_word)

    #prefix of Urls. It is used to tag them in text and recognise them easily
    prefixUrl="!@#$%^"

    # parallel parsing
    if parallel:
      txt = returnRelevantTxt(url, txt0, prefixUrl, True)
      if txt == None:
        return None
      # just return the txt
      return txt
    # not parallel parsing
    else:
      # # make a df about the different similarity methods
      # # this part is skipped in the parallel method due to fear that the csv file will be busy
      # df = pd.concat([df, pd.DataFrame(['Page', 'Pairwise Similarity',\
      #                 'Existance','Meta Existance'])], ignore_index=True)
      # # columns=['Page', 'Pairwise Similarity', 'Existance', 'Meta Existance']
      
      # # in the first iteration create the column names 
      # if counter == 1:
      #   df_temp = pd.DataFrame(columns=['Page', 'Pairwise Similarity', 'Existance', 'Meta Existance'])
      #   df_temp = pd.concat([df_temp, pd.DataFrame(['Page', 'Pairwise Similarity',\
      #                 'Existance','Meta Existance'])], ignore_index=True)
      #   # add the row in the csv
      #   create_csv(important_word, df_temp)
      # # add the row in the csv
      # create_csv(important_word, row=df.iloc[0])
 
      txt = returnRelevantTxt(url, txt0, prefixUrl, True)
      if txt == None:
        return None

    # appends information in Encyclopedia
    f = open(dic+file_name, "w", encoding="utf-8")
    f.write(txt)
    file1 = open(dic+enc, "a")  # append mode
    # file1 .write((prefixUrl+url))
    file1.write(txt)
    file1.close()
    f.close()

# target function for parallel parsing
def loopInDepthSimilarity(counter,df,manual,line,question,dic,important_word,parallel):
  # print("######################################## Page")
  # print(line)
  line=line.strip()  
  htmlToText(important_word, counter, line,df,question,"depth1.txt",manual,parallel,dic)           


# removes duplicate url links and returns them
def removeDuplicateLines(url, dic="Data/"):
  # Using readlines() storing urls in Lines
    # Remove duplicate links
    file1 = open(dic+'cleanLinks.txt', 'r')
    dublicatesLines = file1.readlines()
    url=url.strip()
    dublicatesLines.append(url)
    print('-----------------------------------')
    for item in dublicatesLines:
      if 'w/index.php?title=' in item:
        item = item.replace("w/index.php?title=", "wiki/")
    # print(dublicatesLines)
    print('-----------------------------------')
    print("Total websites including dublicates", len(dublicatesLines))
    print('-----------------------------------')
    Lines = list(dict.fromkeys(dublicatesLines))
    print(Lines)
    Lines.remove('\n')
    print("Number of websites we are searching for:", len(Lines))
    # print(Lines)
    print('-----------------------------------')
    file1.close()
    return Lines

def depthSimilarity(url,question,df,target_websites,important_word,parallel=True, dic="Data/",manual=False):
    # finds all urls in url and stored in file cleanHtml.txt
    depthSearch(url,target_websites)

    # Using readlines() storing urls in Lines
    # Remove duplicate links
    Lines = removeDuplicateLines(url)

    counter = 0
    if parallel:
      import multiprocessing
      from multiprocessing import Process

      # Manager is a process that gathers the returning values of the
      # other processes. (I think)
      manager = multiprocessing.Manager()
      return_dict = manager.dict()
      encyclopedia_list = []
      for line in Lines:
        counter+=1
        # create a new process instance
        process = Process(target=loopInDepthSimilarity, args=(counter,df,manual,line,question,dic,important_word, return_dict))
        encyclopedia_list.append(process)
        # start the process
        process.start()
      for proc in encyclopedia_list:
        proc.join()
      # print(return_dict.values())
      returningValues = return_dict.values()
      return returningValues
    elif not parallel:
      for line in Lines:
        counter+=1
        print("######################################## Page", counter)
        # print(line)
        page_limit = 6
        if counter == page_limit:
          print("Limit is", page_limit, "pages")
          break
        line=line.strip()
        if "." not in line:
          continue
        
        # not useful anymore. 
        # with open('cleanUniqueLinks.txt', 'a') as f: 
        #   f.write(line)
        #   f.write('\n')   
        htmlToText(important_word, counter,line,df,question,"depth1.txt",manual,parallel,dic)           