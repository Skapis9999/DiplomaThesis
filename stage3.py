from search import htmlToText, depthSimilarity
from encyclopaedia import buildEncyclopaedia, cleanEncyclopaedia
from heystackCode import heystack_question, answer_question_heystack
from answer import answer_question, print_answers
from findSource import findSource
from transformers import pipeline

def stage3(url, dic, document_store, important_word, df,target_websites, question,model,table):
    print("Second stage with multiple websites begins")
    print("--------------------")
    parallel = False
    oracle = pipeline(model=model)

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

    print("-----Starting building Enc-----")
    buildEncyclopaedia()
    data = cleanEncyclopaedia()
    print("-----Ending building Enc-----")

    useHaystack = True
    if useHaystack:
        prediction = heystack_question(document_store,question,model,dic+"dataT.txt")
        if prediction == None:
            return [["No answer", 0, "no url", "no context"]] 
    else:
        [cr, step] = answer_question(data,oracle,question)

    useHaystack = True
    if useHaystack:
        for i in range(len(prediction['answers'])):
            exit_counter = answer_question_heystack(prediction, i,dataFile = dic+'dataT.txt')
            answer1 = findSource(prediction,exit_counter,i,useHaystack,dataFile = dic+'dataT.txt')
            table.append([answer1.answer, round(answer1.score,2), answer1.url, answer1.context])

        # print(question)
        # from tabulate import tabulate
        # print(tabulate(table, headers = ['Answer', 'Score', 'url', 'Context'], tablefmt="grid"))
    else:
        print_answers(data, cr, step,dataFile = dic+'dataTFast.txt')

    max_row = max(table, key=lambda x: x[1])
    print("Row with maximum value in the second column:", max_row)

    # srt = "The answer is: "+ max_row[0]+ " with as score of "+ str(max_row[1])
    sorted_data = sorted(table, key=lambda x: x[1], reverse=True)
    return [sorted_data]