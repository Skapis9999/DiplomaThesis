#@title heystack question

def heystack_question(document_store,question,model, dataFile = "dataT.txt"):

  # 4. Initialize the ElasticsearchDocumentStore:

  from haystack import Pipeline
  from haystack.nodes import TextConverter, PreProcessor
  import time

  start = time.monotonic()
  indexing_pipeline = Pipeline()
  text_converter = TextConverter()
  preprocessor = PreProcessor(
      clean_whitespace=True,
      clean_header_footer=True,
      clean_empty_lines=True,
      split_by="word",
      split_length=200,
      split_overlap=20,
      split_respect_sentence_boundary=True,
  )
  t1 = time.monotonic()
  import os

  indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
  indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
  indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])
  t2 = time.monotonic()
  files_to_index = [dataFile]
  try:
    indexing_pipeline.run_batch(file_paths=files_to_index)
  except FileNotFoundError: 
     print("No results")
     return None
  t3 = time.monotonic()

  from haystack.nodes import BM25Retriever

  retriever = BM25Retriever(document_store=document_store)
  t4 = time.monotonic()
  # from haystack.nodes import FARMReader
  from haystack.nodes import TransformersReader
  from transformers.models.bert.tokenization_bert import BasicTokenizer
  # from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


  # reader = TransformersReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
  # reader = TransformersReader(model_name_or_path="deepset/minilm-uncased-squad2", use_gpu=True)  
  # reader = FARMReader(model_name_or_path="ahotrod/albert_xxlargev1_squad2_512", use_gpu=True)

  reader = TransformersReader(model_name_or_path=model, use_gpu=True) 
  t5 = time.monotonic() 
  from haystack import Pipeline
  from haystack.utils import print_answers

  querying_pipeline = Pipeline()
  querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
  querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])
  t6 = time.monotonic()

  try:
      with open("Data/"+"haystack_debug.log", "w") as f:
          # top1 = 32
          # top2 = 16
          # predictionFlag = True
          # while predictionFlag:
          #   # enable debug for debug
          #   top1 = top1/2
          #   top1 = top2/2
          #   try:
          #     prediction = querying_pipeline.run(
          #         query=question,
          #         params={
          #             "Retriever": {"top_k": top1, "debug": False},
          #             "Reader": {"top_k": top2, "debug": False}
          #         }
          #     )
          #     predictionFlag = False
          #     print("Retriever took top",top1, "and reader took top", top2)
          #   except:
          #      pass
            if "dataTFast" not in dataFile:
              prediction = querying_pipeline.run(
                  query=question,
                  params={
                      "Retriever": {"top_k": 15, "debug": False},
                      "Reader": {"top_k": 10, "debug": False}
                  }
              )
              print("Retriever took top",15, "and reader took top", 10)
            else:
              prediction = querying_pipeline.run(
              query=question,
              params={
                  "Retriever": {"top_k": 8, "debug": False},
                  "Reader": {"top_k": 4, "debug": False}
              }
              )
              print("Retriever took top",2, "and reader took top", 1)
          
  except Exception as e:
      print(f"Exception occurred: {str(e)}")
      raise  # Re-raise the exception to see the full traceback
  t7 = time.monotonic()    
  ## ALL ANSWERS 
  # print_answers(prediction, details="all")  # Print retrieved documents and answers

  print("Dilosi ", t1-start)
  print("adding nodes ", t2-start)
  print("indexing pipeline ", t3-start)
  print("setting retriever ", t4-start)
  print("Reader ", t5-start)
  print("Adding the rest of the nodes ", t6-start)
  print("Pipeline ", t7-start)
  return prediction
  

def answer_question_heystack(prediction, i, dataFile = 'dataT.txt'):
  from pprint import pprint

  # # Full information
  # pprint(prediction)

  # from haystack.utils import print_answers

  # print_answers(
  #     prediction,
  #     details="all" ## Choose from `minimum`, `medium` and `all`
  # )

  import re

  info = prediction['answers'][i].context
  nlines = info.count('\n')
  # print("--------", i, "-------- with ", nlines, "lines")
  while(nlines > 0):
    # print('+++')
    # ccc =+1
    c = info.split("\n")
    info = c[0]
    nlines = info.count('\n')
    # print("-------- with ", nlines, "lines")
    # print(c)
    # print(info)
  file = open(dataFile,'r')
  counter = 0
  for line in file.readlines():
    if info in line:
      exit_counter = counter
      exit_line = line
      break 
    counter +=1
  try:  
    # print('exit counter = ', exit_counter)
    # print(exit_line)
    file.close()
    return exit_counter
  except NameError:
    print("Couldn't find in context")
    return None