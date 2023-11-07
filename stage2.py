from search import htmlToText
from encyclopaedia import buildEncyclopaedia, cleanEncyclopaedia
from heystackCode import heystack_question, answer_question_heystack
from answer import answer_question, print_answers
from findSource import findSource
from transformers import pipeline


def stage2(url, dic, document_store, important_word, df, question, model):

    import time
    start = time.monotonic()

    print("-----Starting parsing webpages-----")
    htmlToText(important_word,0,url,df,question,"htmlToTextFast.txt",False,False,dic,1 , "EncyclopaediaFast.txt")
    v1 = time.monotonic()
    print("-----Ending parsing webpages-----")
    print("-----Starting building fast Enc-----")
    buildEncyclopaedia(enc = "EncyclopaediaFast.txt", encOut = "EncyclopaediaFastOut.txt",dic=dic)
    v2 = time.monotonic()
    print("-----Ending building fast Enc-----")

    from os.path import exists

    dataFast = cleanEncyclopaedia(encOut="EncyclopaediaFastOut.txt", dataFile = 'dataTFast.txt',dic=dic)

    file_exists = exists(dic+'dataTFast.txt')
    if file_exists:
        pass
    else:
        table = [["No answer", 0, "no url", "no context"]]
        return [table, table]
    
    useHaystack = True
    if useHaystack:
        predictionFast = heystack_question(document_store,question,model, dic+"dataTFast.txt")
    else:
        oracle = pipeline(model=model)
        [cr, step] = answer_question(dataFast,oracle,question)
    v3 = time.monotonic()
    if useHaystack:
        table = []
        for i in range(len(predictionFast['answers'])):
            exit_counter = answer_question_heystack(predictionFast, i, dataFile = dic+'dataTFast.txt')
            answer1Fast = findSource(predictionFast,exit_counter,i,useHaystack, dataFile = dic+'dataTFast.txt')
            table.append([answer1Fast.answer, round(answer1Fast.score,2), url, answer1Fast.context])
        print(question)
        # from tabulate import tabulate
        # print(tabulate(table, headers = ['Answer', 'Score', 'url', 'Context'], tablefmt="grid"))
        v4 = time.monotonic()
    else:
        print_answers(dataFast, cr, step, dataFile = dic+'dataTFast.txt')

    # max_row = max(table, key=lambda x: x[1])
    # print("Row with maximum value in the second column:", max_row)

    sorted_data = sorted(table, key=lambda x: x[1], reverse=True)
    print("--------------------")

    s1 = v1 - start
    s2 = v2 - v1
    s3 = v3 - v2
    s4 = v4 - v3
    print("htmlToText lasted ",  s1, " seconds")
    print("buildEncyclopaedia lasted ",  s2, " seconds")
    print("heystack_question lasted",  s3, " seconds")
    print("tabulate lasted",  s4, " seconds")
    print("--------------------")

    return [sorted_data, table]