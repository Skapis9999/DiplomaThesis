from pathlib import Path

#@title Encyclopedia

# Creates the encOut file that has all the information that will be the source of the answering model
def buildEncyclopaedia(enc = "Encyclopaedia.txt", encOut = "EncyclopaediaOut.txt",dic = "Data/"):
  enc = dic + enc
  encOut = dic + encOut 
  my_file = Path(enc)
  print("my_file is: ", my_file)

  # unassign runtime if file does not exists. It probably has to leave
  if my_file.exists():
    print("+++++++++++Encyclopaedia exists+++++++++++")
    pass
  else:
    print("--------Encyclopaedia doesn't exist------------------")
    print("No solution is found")
    return 0  

  # copy line by line fron Encyclopedia
  with open(enc) as reader, open(enc, 'r+') as writer:
    for line in reader:
      if line.strip():
        writer.write(line)
    writer.truncate()

  # remove the part between tag_start and tag_end
  tag_start = 'Jump to content'
  tag_end = 'From Wikipedia, the free enciclopedia'
  flag = 0
  lines_to_write=[]
  with open(enc) as in_file:
      for line in in_file:
          if line.strip() == tag_start:
              flag = 1 
          if (flag == 0) or (flag == 1):
            lines_to_write.append(line)
          if (line.strip() == tag_end) and (flag == 1):
            flag += 1
  with open(encOut,'w',encoding="utf8") as out_file:
      out_file.writelines(lines_to_write)  

#@title cleaning data

# gathers all data from EncyclopaediaOut.txt
def gatherData(encOut):

  my_file = Path(encOut)

  # unassign runtime if file does not exists. It probably has to leave
  if my_file.exists():
    pass
  else:
    print("--------encOut missing in gatherData------------------")
    print("No solution is found")
    print("--------encOut missing in gatherData------------------")
    return 0 
  
  word_data = []
  with open(encOut,'r') as data_file:
      for line in data_file:
        word_data.append(line.split())

  print(len(word_data), "line(s) of single words (word_data)")
  # print(word_data)
  return word_data

# cleans the data of encOut
def cleanEncyclopaedia(encOut="EncyclopaediaOut.txt", dataFile = 'dataT.txt',dic = "Data/"):

  encOut = dic + encOut
  dataFile = dic + dataFile
  print("++++++++++++ ",encOut)
  word_data = gatherData(encOut)
  if type(word_data)==int:
    return 0

  data2 = []
  counter = 0
  for line in word_data:
      data2.append(" ".join([str(item) for item in line]))

      # keeps the website line always
      if ("!@#$%^") in data2[-1]:
        continue
      # delete lines with these words
      if ("mw" in data2[-1]) or ("wg" in data2[-1]) or ("@" in data2[-1]) or ("ext." in data2[-1]) \
      or ("wiki" in data2[-1]) or ("ext." in data2[-1]) or ("cctypes" in data2[-1]) \
      or ("This page was last edited" in data2[-1]) or ("Main Article" in data2[-1])\
      or ("ReadView" in data2[-1]) or ("var" in data2[-1]) or ("//" in data2[-1]) or ("Sign Up" in data2[-1])\
      or ("documment.cookie" in data2[-1])or ("==" in data2[-1]) or ("JSON" in data2[-1])\
      or ("getElements" in data2[-1]) or ("eventAction" in data2[-1]) or ("+=" in data2[-1])\
      or ("Do Not Show Again" in data2[-1]) or ("href" in data2[-1]) or (".append" in data2[-1]) \
      or ("text-" in data2[-1]) or ("if(" in data2[-1]) or ("if (" in data2[-1]) \
      or ("px" in data2[-1]) or ("<img" in data2[-1]) or ("Wikimedia" in data2[-1]) or ("font-" in data2[-1]) \
      or ("border-radius" in data2[-1]) or ("rem" in data2[-1]) or ("margin:" in data2[-1]) \
      or ("transition:" in data2[-1]) or ("solid transparent" in data2[-1]) or ("arhiveorg" in data2[-1])\
      or ("Terms of Service" in data2[-1])  or ("JSON" in data2[-1])  or ("Creative Commons" in data2[-1])\
      or ("http" in data2[-1]) or ("setCookie" in data2[-1]) or (");" in data2[-1]) \
      or ("event." in data2[-1]) or ("()" in data2[-1]) or (".cookie" in data2[-1]) \
      or (".event" in data2[-1]) or ("siteSection" in data2[-1]) \
      or ("Thank you for your feedback" in data2[-1]) or ("grid-" in data2[-1]) \
      or ("archiveorg" in data2[-1]) or (("ZIP" in data2[-1]) and ("download" in data2[-1])) \
      or ("width=" in data2[-1]) or ("%;" in data2[-1]) or ("you agree to the Terms and" in data2[-1])\
      or ("e.thumbhide" in data2[-1]) or (">=pw" in data2[-1]) or ("console.log" in data2[-1]) \
      or ("Español" in data2[-1]) or ("PDFPrintable" in data2[-1]) or ("Français" in data2[-1]) \
      or ("sliderLayout" in data2[-1]) or ("fullwidth" in data2[-1]) or ("visibilityLevels" in data2[-1]) \
      or ("gridwidth" in data2[-1]) or ("gridheight" in data2[-1]) or ("lazyType" in data2[-1]) \
      or ("perspectiveType" in data2[-1]) or ("editorheight" in data2[-1]) or ("responsiveLevels" in data2[-1]) \
      or ("stopAtSlide" in data2[-1]) or ("stopAfterLoops" in data2[-1]) or ("stopLoop" in data2[-1]) \
      or ("visible_area" in data2[-1]) or ("OnAndroid" in data2[-1]) or ("];" in data2[-1]) \
      or ("integrationId" in data2[-1]) or (".style" in data2[-1]) or ("wd-icon" in data2[-1]) \
      or ("onSelectChange" in data2[-1]) or ("dropdown.onchange" in data2[-1]) or ("color: white" in data2[-1]) \
      or ("color:white" in data2[-1]) or ("display: none" in data2[-1]) or ("display:none" in data2[-1]) \
      or ("-gradient" in data2[-1]) or ("element.style." in data2[-1]) or ("clientWidth" in data2[-1]) \
      or ("clientHeight" in data2[-1]) or ("pagePadding" in data2[-1]) or ("getElementById" in data2[-1]) \
      or ("dateTime" in data2[-1]) or ("innerWidth" in data2[-1]) or ("fixVcRow" in data2[-1]) \
      or ("})" == data2[-1]) or ("reverse_header_buttons" in data2[-1]) or ("ix = 0," == data2[-1]) \
      or ("newh;" in data2[-1]) or ("innerWidth" in data2[-1]) or ("sl;" == data2[-1]) \
      or ("url: url" == data2[-1]) or ("cache: true," == data2[-1]) or ("text/css" in data2[-1]) \
      or ("line-height:" in data2[-1]) or ("link.rel" in data2[-1]) or ("stylesheet" in data2[-1]) \
      or ("pageWidth:" in data2[-1]) or ("display: block;" in data2[-1]) or ("return false" in data2[-1]) \
      or ("page: null" in data2[-1]) or ("row!important" in data2[-1]) or ("return true" in data2[-1]) \
      or ("display: flex" in data2[-1]) or ("justify-content:" in data2[-1]) or ("offsetTop" in data2[-1]) \
      or ("!important;" in data2[-1]) or ("gem-icon" in data2[-1]) or ("vertical-align:" in data2[-1]) \
      or ("box-shadow:" in data2[-1]) or ("border: none" in data2[-1]) or ("wait_for_update:" in data2[-1]) \
      or ("analytics_storage:" in data2[-1]) or ("ad_storage:" in data2[-1]) or ("functionality_storage:" in data2[-1]) \
      or ("personalization_storage:" in data2[-1]) or ("security_storage:" in data2[-1]) or ("img.wp" in data2[-1]) \
      or ("color: red;" in data2[-1]) or ("onHoverStop:" in data2[-1]) or ("}," in data2[-1]) \
      or ("z-index:" in data2[-1]) or ("color: red;" in data2[-1]) or ("hide" == data2[-1]) \
      or ("Search" == data2[-1]) or ("Contact Us" == data2[-1]) or ("Create account Log in" == data2[-1]) \
      or ("1 reference" == data2[-1]) or ("2 reference" == data2[-1]) or ("3 reference" == data2[-1]) or ("4 reference" == data2[-1])\
      or ("Create accountLog in" == data2[-1]) or ("Sidebar" == data2[-1]) or ("stopLoop" in data2[-1]) \
      or ('Jump to navigation' == data2[-1]) or ('Jump to search' == data2[-1]) or ("videoPlayerId" in data2[-1]) \
      or ('britannica.com' in data2[-1]) or ('TopicCollectionPage' in data2[-1]) or (',"currency": "USD"' in data2[-1]) \
      or (',"country": "US"' in data2[-1]) or (',"state": "NV"' in data2[-1]) or ("1806775393686135912" in data2[-1]) \
      or ('"hasAds": true' in data2[-1]) or ('.adthrive.' in data2[-1]) or ("s.async" in data2[-1]) \
      or ('s.referrerpolicy' in data2[-1]) or ('Search Britannica' in data2[-1]) or ("cam_targeting_values" in data2[-1]) \
      or ('&amp;' in data2[-1]) or ('pathname' in data2[-1]) or ("isPhone" in data2[-1]) \
      or ('isDesktop' in data2[-1]) or ('logoutUrl' in data2[-1]) or ("fetchOffset" in data2[-1]) \
      or ('.wpb_wrapper' in data2[-1]) or ('li.current' in data2[-1]) or ("column-inner" in data2[-1]) \
      or ('.td-' in data2[-1]) or ('.tdi' in data2[-1]) or ("auto;" in data2[-1]) \
      or ('Marketing' == data2[-1]) or ('Preferences' == data2[-1]) or (".tdi_" in data2[-1]) \
      or ('blockClass ' in data2[-1]) or ('Manage consent' == data2[-1]) or ("View preferences" == data2[-1]) \
      or ('Skip to content' == data2[-1]) or ('blockOffsetLeft' in data2[-1]) or ("blockInner " in data2[-1]) \
      or ('tdbMenuItem.' in data2[-1]) or ('Related Posts' == data2[-1]) or (">" == data2[-1]) \
      or ('content-visibility:' in data2[-1]) or ('auto;' in data2[-1]) or ("tdbSearchItem." in data2[-1]) \
      or ('height:auto' in data2[-1]) or ('!important' in data2[-1]) or ("background-image:" in data2[-1]) \
      or ('max-height:' in data2[-1]) or ('box-sizing:' in data2[-1]) or ("border-box;" in data2[-1]) \
      or ('position: fixed;' in data2[-1]) or ('overflow: hidden;' in data2[-1]) or ("opacity: 0;" in data2[-1]) \
      or ('opacity: 1;' == data2[-1]) or ('color: ;' in data2[-1]) or ("background-color:" in data2[-1]) \
      or ('JmendelCookieName' in data2[-1]) or ('autocompleteToSearchPage' in data2[-1]) or ("freeTopicReason" in data2[-1]) \
      or ('.async' in data2[-1]) or ('documentGroup' in data2[-1]) or ("firstTopicPage" in data2[-1]) \
      or ("};" in data2[-1]) or ("return;" in data2[-1]) or ("dataType:" in data2[-1]) or ("revapi" in data2[-1]) \
      or ("margin-left:" in data2[-1]) or ("flex-wrap:" in data2[-1]) or ("wrap;" in data2[-1]) \
      or ("margin-left:" in data2[-1]) or ("flex-wrap:" in data2[-1]) or ("wrap;" in data2[-1]) \
      or ("bottom: 0" in data2[-1]) or ("flex-wrap:" in data2[-1]) or ("wrap;" in data2[-1]) \
      or ("left: 0" in data2[-1]) or ("right: 0" in data2[-1]) or (".ajax" in data2[-1]) \
      or ("tdi." in data2[-1]) or (".tdi" in data2[-1]) or ("tdi_" in data2[-1]) \
      or ("inline;" in data2[-1]) or ("_tdi_" in data2[-1]) or ("_tdi" in data2[-1]) \
      or ("margin-top:" in data2[-1]) or ("-webkit-transform:" in data2[-1]) or ("none;" in data2[-1]) \
      or ("padding-" in data2[-1]) or ("background-" in data2[-1]) or ("FacebookInstagramLinkedinTwitterYoutube" in data2[-1]) \
      or ("transform-origin" in data2[-1]) or ("-webkit-" in data2[-1]) or ("0;" in data2[-1]) \
      or ("default;" in data2[-1]) or ("none;" in data2[-1]) or ("cover;" in data2[-1]) \
      or ("-height:" in data2[-1]) or ("min-height:" in data2[-1]) or ("relative;" in data2[-1]) \
      or ("<" == data2[-1][0]) or (":" == data2[-1][0]) or ('="' in data2[-1]) \
      or ("><" in data2[-1]) or ("class=" in data2[-1]) or ('column;' in data2[-1]) or ('accept the Privacy Policy' in data2[-1])\
      or ("visible;" in data2[-1]) or ("column-count:" in data2[-1]) or ('="' in data2[-1]) \
      or ("Share this page" in data2[-1]) or ("Copy the URL" in data2[-1]) or ("We use cookies" in data2[-1])\
      or (" cookies" == data2[-1]) or ("filter:blur" in data2[-1]) or ("opacity:0" in data2[-1]) or ("margin-left:" in data2[-1]):
        # print("found it!")
        counter =+ 1
        del data2[-1]

      if len(data2)>1:
        if ("!@#$%^") in data2[-1]:
          continue
        # delete lines with these words
        if ("asdf" in data2[-1]) or ("asdf" in data2[-1]) or ('asdf' in data2[-1]) \
        or ("asdf" in data2[-1]) or ("asdf" in data2[-1]) or ('asdf' in data2[-1]) \
        or ("row;" in data2[-1]) or ("solid;" in data2[-1]) or ('hidden;' in data2[-1]) \
        or ("flex-direction:" in data2[-1]) or ("flex:" in data2[-1]) or ('-style' in data2[-1]) \
        or (" ,       ..." in data2[-1]) or ("" == data2[-1]) or (' ' == data2[-1]) \
        or ("}" == data2[-1][0]) or ("." == data2[-1][0]) or (';' in data2[-1][-1]) \
        or ("inline-block;" in data2[-1]) or ("absolute;" in data2[-1]) or ("''" in data2[-1]):
          counter =+ 1
          del data2[-1]
          continue

      try:
        if ("!@#$%^") in data2[-1]:
          continue
        # delete lines with these words
        if (("Wikibooks(" in data2[-2]) or ("Wikinews(" in data2[-2]) or ("Wikiquote(" in data2[-2]) \
        or ("Wikisource(" in data2[-2]) or ("Wikiversity(" in data2[-2]) or ("Wikivoyage(" in data2[-2]) \
        or ("Wiktionary(" in data2[-2]) or ("Multilingual sites(" in data2[-2])) \
        and "edit" in data2[-1]:
          counter =+2
          del data2[-2:]
      except:
        pass

      try:
        if ("!@#$%^") in data2[-1]:
          continue
        # delete lines with these words
        if ("Statistics" in data2[-1]) or ("Developers" in data2[-2]) or ("Data access" in data2[-3]) \
        or ("Disclaimers" in data2[-4]) or ("About Wikidata" in data2[-5]) \
        or ("Print/export" in data2[-6]) or ("URICite" in data2[-7]):
          counter =+7
          del data2[-7:]
      except:
        pass

      try:
        if ("!@#$%^") in data2[-1]:
          continue
        # delete lines with these words
        if ("Statistics" in data2[-1]) or ("Developers" in data2[-2]) or ("Disclaimers" in data2[-3]):
          counter =+3
          del data2[-3:]
      except:
        pass
  # print some stats
  print(counter, "deletions")
  print(len(data2), "line(s) of data2")
  # print(data2)

  data=[]
  # remove unprintable characters
  import string
  printable = set(string.printable)
  filter(lambda x: x in printable, data2)
  counter_test = 0
  for s in data2:
    a = ''.join(filter(lambda x: x in printable, s))
    data.append(a)
    if counter_test == 0:
      counter_test=+1
      continue
    counter_test=+1
    if ("!@#$%^") in data[-1]:
        continue
    # delete lines with these words
    if (data[-1] == "") or (data[-1] =="}") or ("*/" in data[-1]) or ("lp" in data[-1]) \
    or (".optin" in data[-1]) or ("{" in data[-1]) or (".country" in data[-1]) or ("[edit]" in data[-1]) \
    or (".frb" in data[-1]) or (".frequency" in data[-1]) or ("*" in data[-1]) or ("#" in data[-1]) \
    or ("mw" in data[-1]) or ("RLQ" in data[-1]) or ("^" in data[-1]) or ("Main article" in data[-1]) \
    or ("See also:" in data[-1]) or ("inTalkContributions" in data[-1]) or (".elementor" in data[-1]) \
    or ("window." in data[-1]) or ("||" in data[-1]) or ("||" in data[-1]) or ("isArray" in data[-1]) \
    or (".whb-" in data[-1]) or ("||" in data[-1]):
        del data[-1]
        continue

    a = ["Jump to content", "Toggle sidebar", "Create account", "Pages for logged out editors learn more", "TalkContributions", "Main pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonate", "What links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageWikidata item", "Download as PDFPrintable version", "On this Wikipedia the language links are at the top of the page across from the article title. Go to top.", "Toggle the table of contents", "ArticleTalk", "ReadEditView history", "From Wikipedia", "the free encyclopedia", "additional terms may apply. By using this site", "you agree to the Terms of Use and Privacy Policy. Wikipedia is a registered trademark of the Wikimedia Foundation", "Inc., a non-profit organization.", "Privacy policy", "About Wikipedia", "Contact Wikipedia", "Mobile view", "Cookie statement"]
    b =['From Wikipedia, the free encyclopedia', 'additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.']

    # remove phrases in a and b
    if (data[-1] in a) or (len(data) == 0) or (data[-1] in b):
      if ("!@#$%^") in data2[-1]:
          continue 
      del data[-1]
      continue

    # remove less than 10 letters
    if len(data[-1]) < 10:
      del data[-1]
      continue
    
    # remove less than 4 words
    if len(data[-1].split()) < 3:
      del data[-1]
      continue

  print(len(data), "line(s) of data")
  # print(data)
  with open(dataFile, 'w') as f:
      for line in data:
          f.write("%s\n" % line)
  return data
