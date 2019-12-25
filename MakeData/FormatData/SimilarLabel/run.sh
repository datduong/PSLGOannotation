



#### get labels

#!/bin/bash
. /u/local/Modules/default/init/modules.sh
module load python/3.7.2
cd /u/scratch/d/datduong/PSLGOannotation/MakeData/FormatData/SimilarLabel
WORKDIR='/u/scratch/d/datduong/deepgo'
OUTPUT_PATH=$WORKDIR'/data/PSLdata'
mkdir $OUTPUT_PATH 
ONTO='cellular_component'
onto='cc' ## need because we use short name
OUTPUT_PATH=$WORKDIR'/data/PSLdata/'$ONTO
LABEL_SEEN=$WORKDIR/data/train/deepgo.$onto.csv
LABEL_COMPLETE=$WORKDIR/data/train/deepgo.$onto.csv

python3 FormatLabel.py $WORKDIR/data $OUTPUT_PATH $LABEL_SEEN $LABEL_COMPLETE $ONTO

## COMMENT using bert12 ... probably should be using elmo or bert11+12
LABEL_VECTOR=$WORKDIR/data/cosine.AveWordClsSep768.Linear768.Layer12/label_vector.pickle

cd /u/scratch/d/datduong/PSLGOannotation/MakeData/FormatData/SimilarLabel
python3 FormatSimilarLabel.py $WORKDIR/data $OUTPUT_PATH $LABEL_SEEN $LABEL_COMPLETE $LABEL_VECTOR $ONTO
