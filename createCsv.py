#@title similarity csv files
import pandas as pd

df = pd.DataFrame(columns=['Page', 'Pairwise Similarity', 'Existance', 'Meta Existance'])

# create a csv file with all the different similarities. Pariwise Similarity, Existance in page, Existance in Metadata
def create_csv(important_word,row, dic="Data/"):
  try:
    if row.empty == True:
      print('Empty')
      return None
    import csv
    name = "_".join(important_word)
    f = open(dic+ str(name) + '.csv', 'a')
    writer = csv.writer(f)
    writer.writerow(row)
    print('Row added')
    f.close()
  except Exception as error:
    print(error)