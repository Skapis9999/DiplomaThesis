from heystackCode import heystack_question, answer_question_heystack
from findSource import findSource


def stage0(dic, document_store, question,model):

    useHaystack = True

    prediction = heystack_question(document_store,question,model, dic+"dataT.txt")
    if prediction == None:
        return [["No answer", 0, "no url", "no context"]]
    table = []
    for i in range(len(prediction['answers'])):
            exit_counter = answer_question_heystack(prediction, i,dataFile = dic+'dataT.txt')
            answer1 = findSource(prediction,exit_counter,i,useHaystack,dataFile = dic+'dataT.txt')
            table.append([answer1.answer, answer1.score, answer1.url, answer1.context])


    sorted_data = sorted(table, key=lambda x: x[1], reverse=True)
    return [sorted_data, table]