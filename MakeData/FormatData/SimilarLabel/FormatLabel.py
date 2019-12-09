

## Labels ==> GO terms.
## need to see which terms are similar, so we can infer unseen labels.

## probably have to do batch mode

import pickle, os, re, sys
import pandas as pd
import numpy as np

import networkx
import obonet

from tqdm import tqdm

from scipy.spatial.distance import cosine

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

## COMMENT create subset file, parent \t child \t 1
fout = open("Subset.txt","w")
for index1, value1 in enumerate(label_names_complete):
  if value1 in ['GO:0008150','GO:0003674','GO:0005575']: ## don't need the roots when compute similarity
    continue
  # Find edges to parent terms
  for child, parent, key in graph.out_edges(value1, keys=True):
    if key == 'is_a':
      fout.write(parent+"\t"+child+"\t1.0\n")
fout.close()

  ## COMMENT write out which label we have seen, and not
foutLabel = open("Label.txt","w")
for index1, value1 in enumerate(label_names_complete):
  if value1 in label_names_seen:
    foutLabel.write(value1+"\t"+"1.0\n") ## WE SEE THIS LABEL
  else:
    foutLabel.write(value1+"\t"+"0.0\n")
foutLabel.close()


