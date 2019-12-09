
import os,sys,re,pickle
import numpy as np
import pandas as pd
from tqdm import tqdm

WORK_DIR = '/u/scratch/d/datduong/deepgo/dataExpandGoSet/'
os.chdir("/u/scratch/d/datduong/deepgo/data/")
OUTPUT_PATH = 'PSLdata'
if not os.path.exists(OUTPUT_PATH):
  os.mkdir(OUTPUT_PATH)

os.chdir(OUTPUT_PATH)
# need format Classifier Protein Label
# we predict 3 ontology separately, so we have to concat them

ClassifierName = 'BERT12'

# onto = 'mf'
for onto in ['mf','cc','bp'] :

  ## COMMENT we save all models in the folder @data
  prediction = pickle.load(open("/u/scratch/d/datduong/deepgo/data/BertNotFtAARawSeqGO/"+onto+"/fold_1/2embPpiAnnotE256H1L12I512Set0/ProtAnnotTypeLarge/YesPpiYesTypeScaleFreezeBert12Ep10e10Drop0.1/prediction_train_all_on_test.pickle","rb")) ## num_prot x num_label seen

  ## COMMENT return a dict with true labels
  prediction = prediction['prediction']

  protein_names = pd.read_csv(WORK_DIR+"train/fold_1/ProtAnnotTypeTopoData/test-"+onto+"-input.tsv",sep="\t",header=None)
  protein_names = list ( protein_names[0] ) ## do not sort protein name, leave as the same order seen in data

  label_names_seen = pd.read_csv(WORK_DIR+"train/deepgo."+onto+".csv",sep="\t",header=None)
  label_names_seen = sorted (list(label_names_seen[0]))

  fout = open (ClassifierName+"-"+onto+".txt",'w')
  for index1, protein1 in enumerate ( tqdm(protein_names) )  : ## num protein
    this = "\n".join ( ClassifierName + "\t" + protein1 + "\t" + label_names_seen[index2] + "\t" + str( np.round(p,9)) for index2,p in enumerate( prediction[index1] ) )
    fout.write(this)

  #
  fout.close()





