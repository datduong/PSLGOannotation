
import os,sys,re,pickle
import numpy as np
import pandas as pd
from tqdm import tqdm

import networkx
import obonet

## target file has True and Error

def run (WORKDIR,OUTPUT_PATH,LABEL_SEEN,LABEL_COMPLETE,PROTEIN_NAME,ONTO) :

  os.chdir(WORKDIR)
  # OUTPUT_PATH = 'PSLdata'
  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

  if ONTO is not 'none':
    graph = obonet.read_obo('go.obo')

  if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

  os.chdir(OUTPUT_PATH)

  ## COMMENT load in protein names
  protein_names = pd.read_csv(PROTEIN_NAME,sep="\t",header=None)
  protein_names = list ( protein_names[0] ) ## do not sort protein name, leave as the same order seen in data
  if ONTO is not 'none':
    protein_names = [ l for l in protein_names if l != 'Entry' ]

  ## COMMENT load label we seen during training classifier
  label_names_seen = pd.read_csv(LABEL_SEEN,sep="\t",header=None)
  label_names_seen = sorted (list(label_names_seen[0]))

  ## COMMENT these are labels to be predicted
  label_names_complete = pd.read_csv(LABEL_COMPLETE,sep="\t",header=None) ## "deepgo.all.terms.seen.csv"
  label_names_complete = sorted (list(label_names_complete[0]))

  ## COMMENT filter by ontology ?
  if ONTO is not 'none':
    label_names_seen = [ l for l in label_names_seen if graph.node[l]['namespace'] == ONTO ]
    label_names_complete = [ l for l in label_names_complete if graph.node[l]['namespace'] == ONTO ]

  ## COMMENT write target
  ## predict all labels and errors
  print ('labels to be predicted by PSL {}'.format(len(label_names_complete)))

  fout = open ('Classifier_target.txt','w')
  fout2 = open ('Classifier_truth.txt','w')
  
  protein_names = sorted (protein_names)
  for index,prot in tqdm(enumerate (protein_names)):
    for label in label_names_complete:
      if label in ['GO:0008150','GO:0003674','GO:0005575']: ## don't need the roots
        continue

      fout.write("TRUTH\t"+prot+"\t"+label+"\n")
      fout2.write("TRUTH\t"+prot+"\t"+label+"\t0.5\n") ## just put 0.5 worry later it doesn't matter.

      fout.write("BERT12Error\t"+prot+"\t"+label+"\n") ## error of observed classifier
      fout.write("PsiBLASTError\t"+prot+"\t"+label+"\n")

      # write observed classifier-labels which we must predict --> so called "grounding"
      if label not in label_names_seen:
        fout.write("BERT12\t"+prot+"\t"+label+"\n")
        fout.write("PsiBLAST\t"+prot+"\t"+label+"\n")

  ##
  fout.close()
  fout2.close()

  fout = open('Sample.txt','w')
  fout.write("\n".join(p+'\t1.0' for p in protein_names))
  fout.close()

  fout = open('Classifier.txt','w')
  for m in ['BERT12','PsiBLAST','BERT12Error','PsiBLASTError','TRUTH'] :
    if m in ['BERT12','PsiBLAST'] :
      fout.write(m+"\t1.0\n")
    else:
      fout.write(m+"\t0.0\n")
  fout.close()

  # C1 E1 T 1.0
  # C1 T 1.0
  fout = open('ErrorLink.txt','w')
  fout2 = open('ClassifierLink.txt','w')
  for m in ['BERT12','PsiBLAST']:
    fout.write(m+'\t'+m+'Error\tTRUTH\t1.0\n')
    fout2.write(m+'\tTRUTH\t1.0\n')
  fout.close()
  fout2.close()


if len(sys.argv)<1: ## run script
	print("Usage: \n")
	sys.exit(1)
else:
  # WORKDIR,OUTPUT_PATH,LABEL_SEEN,LABEL_COMPLETE,PROTEIN_NAME,ONTO
	run ( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] )

