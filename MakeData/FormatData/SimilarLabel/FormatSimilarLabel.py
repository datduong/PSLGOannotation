
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

def run (WORKDIR,OUTPUT_PATH,LABEL_SEEN,LABEL_COMPLETE,LABEL_VECTOR,ONTO) :

  # WORKDIR = "/u/scratch/d/datduong/deepgo/data"
  os.chdir(WORKDIR)
  # OUTPUT_PATH = 'PSLdata'
  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

  graph = obonet.read_obo('go.obo')

  label_names_seen = pd.read_csv(LABEL_SEEN,sep="\t",header=None) ## "deepgo.all.terms.seen.csv"
  label_names_seen = sorted (list(label_names_seen[0]))

  ## COMMENT these are labels to be predicted
  label_names_complete = pd.read_csv(LABEL_COMPLETE,sep="\t",header=None) ## "deepgo.all.terms.seen.csv"
  label_names_complete = sorted (list(label_names_complete[0]))

  ## COMMENT filter by ontology ?
  if ONTO is not 'none':
    label_names_seen = [ l for l in label_names_seen if graph.node[l]['namespace'] == ONTO ]
    label_names_complete = [ l for l in label_names_complete if graph.node[l]['namespace'] == ONTO ]

  label_names_complete = sorted ( list ( set (label_names_complete + label_names_seen) ) ) ## make sure we have all @label_names_seen into the list to be predicted as well
  print ('total label to be predicted by PSL {}'.format(len(label_names_complete)))

  ## COMMENT word vectors
  label_vec = pickle.load(open(LABEL_VECTOR,"rb")) # "/u/scratch/d/datduong/deepgo/data/cosine.AveWordClsSep768.Linear768.Layer12/label_vector.pickle"
  names_in_label_vec = sorted(list(label_vec.keys())) ## @names_in_label_vec is needed to retain correct order
  index_label_map = {index1 : value1 for index1, value1 in enumerate(names_in_label_vec)}

  label_vec_matrix = np.zeros( (len(names_in_label_vec),768) )
  for index1, value1 in enumerate(names_in_label_vec):
    label_vec_matrix[index1] = label_vec[value1]

  sim = pairwise.cosine_similarity(label_vec_matrix) ## possible ?? ... quite fast actually

  # for ONTO in ['cellular_component','molecular_function','biological_process']:

  print ('output path will be {}'.format(OUTPUT_PATH))
  os.chdir(OUTPUT_PATH)

  ## COMMENT write out similar pairs
  fout = open("SimilarLabel.txt","w")

  for index1, value1 in enumerate(tqdm(names_in_label_vec)): ## @names_in_label_vec must do this to retain correct ordering
    if value1 not in label_names_complete: ## only get sim of labels we want PSL to predict
      continue

    # if index1 > 100:
    #   exit() ## testing

    ancestors = networkx.descendants(graph, value1) # don't want get ancestors, we capture long-range similarity
    where1 = np.where ( sim[index1] > 0.80 )[0] ## depends on the whole 40k terms
    if len(where1) > 1:
      for w in where1:
        if w == index1: ## don't compare to self.
          continue
        value2 = index_label_map[w] # because of @where1, ## depends on the whole 40k terms
        if value2 not in label_names_complete: ## only get sim of labels we want PSL to predict
          continue
        if graph.node[value2]['namespace'] != ONTO: ## split by ontology
          continue
        if value2 not in ancestors: ## ancestor will be accounted for by subset-rule
          fout.write(value1+"\t"+value2+"\t"+str( np.round ( sim[index1][w], 6 ) )+"\n")

  fout.close()


## COMMENT run script
if len(sys.argv)<1: 
	print("Usage: \n")
	sys.exit(1)
else:
  # WORKDIR,OUTPUT_PATH,LABEL_SEEN,LABEL_COMPLETE,LABEL_VECTOR,ONTO
	run ( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] )



# label_vec = pickle.load(open("/u/scratch/d/datduong/deepgo/data/cosine.AveWordClsSep768.Linear768.Layer12/label_vector.pickle","rb")) 

# GO:1990841  GO:0031490  0.922209
# pairwise.cosine_similarity([label_vec['GO:1990841'],label_vec['GO:0031490']])
# array([[1.        , 0.92220945],
#        [0.92220945, 1.        ]])

# GO:1990939  GO:0008574  0.98641
# pairwise.cosine_similarity([label_vec['GO:1990939'],label_vec['GO:0008574']])
# array([[1.        , 0.98641018],
#        [0.98641018, 1.        ]])






