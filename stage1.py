def stage1(question,language,website):

    import time
    start = time.monotonic()

    from importantWordAndSearch import slowSearch
    # language to search
    lang = language
    if website=="All":      # False if url is found automatically
        manual_link = False
    else:
        manual_link = True

    # Directory
    dic = "Data/"

    # find current directory
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Current directory is: ", dir_path)

    
    v1 = time.monotonic()

    
    [important_word,target_websites] = slowSearch(question,lang,manual_link,website)
    v2 = time.monotonic()

    # delete all files from previous runs
    directory = '/home/chris/Documents/diplomaThesis/flask/Data'
    file_pattern = '*.txt'
    file_pattern2 = '*.csv'

    import os
    import glob

    # Find all .txt files in the directory
    files = glob.glob(os.path.join(directory, file_pattern))
    # Find all .csv files in the directory
    files2 = glob.glob(os.path.join(directory, file_pattern2))

    # Delete each file
    for file in files:
        os.remove(file)
    for file in files2:
        os.remove(file)

    # print them 
    print("------Files in the directory. It should contain no .txt files------")
    cmd = "ls -al /home/chris/Documents/diplomaThesis/flask/Data"
    os.system(cmd)
    print("------")

    v3 = time.monotonic()

    import pandas as pd

    df = pd.DataFrame(columns=['Page', 'Pairwise Similarity', 'Existance', 'Meta Existance'])
    
    name = "_".join(important_word)
    with open(dic+ str(name) + '.csv', "w") as my_empty_csv:
        # now you have an empty file already
        pass 

    url = target_websites[0]

    v4 = time.monotonic()

    s1 = v1 - start
    s2 = v2 - v1
    s3 = v3 - v2
    s4 = v4 - v3
    print("ElasticsearchDocumentStore Initialized (deleted)",  s1, " seconds")
    print("SlowSearch  lasted  ",  s2, " seconds")
    print("Deleted txt files lasted  ",  s3, " seconds")
    print("sv files created  ",  s4, " seconds")

    return [url, dic, important_word, df,target_websites]