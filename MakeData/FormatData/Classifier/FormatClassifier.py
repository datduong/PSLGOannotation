
import os,sys,re,pickle
import numpy as np
import pandas as pd
from tqdm import tqdm

import networkx
import obonet

def run (CLASSIFIER_NAME,WORKDIR,OUTPUT_PATH,LABEL_SEEN,PROTEIN_NAME,MODEL_OUTPUT,ONTO,OUTPUT_NAME) :

  # need format Classifier Protein Label
  # we predict 3 ontology separately, so we have to concat them

  os.chdir(WORKDIR)
  # OUTPUT_PATH = 'PSLdata'
  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

  if ONTO is not 'none':
    graph = obonet.read_obo('go.obo')

  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

  os.chdir(OUTPUT_PATH)

  ## COMMENT load back saved prediction
  prediction = pickle.load(open(MODEL_OUTPUT,"rb")) ## num_prot x num_label seen
  prediction = prediction['prediction'] ## has 'true_label' too

  ## COMMENT load in protein names
  protein_names = pd.read_csv(PROTEIN_NAME,sep="\t",header=None)
  protein_names = list ( protein_names[0] ) ## do not sort protein name, leave as the same order seen in data
  if ONTO is not 'none':
    protein_names = [ l for l in protein_names if l != 'Entry' ]

  ## COMMENT load label we seen during training classifier
  label_names_seen = pd.read_csv(LABEL_SEEN,sep="\t",header=None)
  label_names_seen = sorted (list(label_names_seen[0]))
  if ONTO is not 'none':
    label_names_seen = [ l for l in label_names_seen if l in graph.node ]
    label_names_seen = [ l for l in label_names_seen if graph.node[l]['namespace'] == ONTO ]

  ## COMMENT write out
  fout = open (OUTPUT_NAME,'w') # 'ClassifierPredict.txt'
  for index1, protein1 in enumerate ( tqdm(protein_names) )  : ## num protein
    this = "\n".join ( CLASSIFIER_NAME + "\t" + protein1 + "\t" + label_names_seen[index2] + "\t" + str( np.round(p,9)) for index2,p in enumerate( prediction[index1] ) )
    fout.write(this+"\n") ## so we have proper spacing between protein labels

  #
  fout.close()


## COMMENT run script
if len(sys.argv)<1:
	print("Usage: \n")
	sys.exit(1)
else:
  # CLASSIFIER_NAME,WORKDIR,OUTPUT_PATH,LABEL_SEEN,PROTEIN_NAME,MODEL_OUTPUT,ONTO
	run ( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])



