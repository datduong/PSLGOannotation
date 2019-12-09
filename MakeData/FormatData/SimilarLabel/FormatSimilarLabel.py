
## Labels ==> GO terms.
## need to see which terms are similar, so we can infer unseen labels.

## probably have to do batch mode

import pickle, os, re, sys
import pandas as pd
import numpy as np

import networkx
import obonet

from tqdm import tqdm
from sklearn.metrics import pairwise

os.chdir("/u/scratch/d/datduong/deepgo/data")
OUTPUT_PATH = 'PSLdata'
if not os.path.exists(OUTPUT_PATH):
  os.mkdir(OUTPUT_PATH)

graph = obonet.read_obo('go.obo')

label_names_seen = pd.read_csv("deepgo.all.terms.seen.csv",sep="\t",header=None)
label_names_seen = sorted (list(label_names_seen[0]))

label_vec = pickle.load(open("cosine.AveWordClsSep768.Linear768.Layer12/label_vector.pickle","rb"))
label_names_complete = sorted(list(label_vec.keys()))
print (label_names_complete[0:10])

os.chdir(OUTPUT_PATH)

label_vec_matrix = np.zeros( (len(label_names_complete),768) )
for index1, value1 in enumerate(label_names_complete):
  label_vec_matrix[index1] = label_vec[value1]

label_index_map = {value1 : index1 for index1, value1 in enumerate(label_names_complete)}
index_label_map = {index1 : value1 for index1, value1 in enumerate(label_names_complete)}

sim = pairwise.cosine_similarity(label_vec_matrix) ## possible ??

## COMMENT write out similar pairs
fout = open("SimilarLabel.txt","w")
for index1, value1 in tqdm (enumerate(label_names_complete)):

  if index1 > 100:
    exit ## testing

  # get all ancestors (don't want get ancestors), we capture long-range similarity
  ancestors = networkx.descendants(graph, value1)
  where1 = np.where ( sim[index1] > 0.80 )[0]
  if len(where1) > 1:
    for w in where1:
      if w == index1: ## don't compare to self.
        continue
      value2 = index_label_map[w]
      if value2 not in ancestors: ## ancestor will be accounted for by subset-rule
        fout.write(value1+"\t"+value2+"\t"+str( np.round ( sim[index1][w], 6 ) )+"\n")

fout.close()


# GO:0000001      GO:0000266      0.8350666279101928
# pairwise.cosine_similarity([label_vec['GO:0000001'],label_vec['GO:0000266']])
# GO:0000001      GO:0001563      0.767143928332986
# pairwise.cosine_similarity([label_vec['GO:0000001'],label_vec['GO:0001563']])
