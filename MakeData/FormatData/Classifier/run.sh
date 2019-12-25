
##

for onto in mf cc bp ; do
  mkdir $SCRATCH/deepgo/data/BertNotFtAARawSeqGO/$onto/fold_1/2embPpiAnnotE256H1L12I512Set0/YesPpiYesTypeScaleFreezeBert12Ep10e10Drop0.1/
done

for onto in mf cc bp ; do
  scp -r /local/datdb/deepgo/data/BertNotFtAARawSeqGO/$onto/fold_1/2embPpiAnnotE256H1L12I512Set0/YesPpiYesTypeScaleFreezeBert12Ep10e10Drop0.1 $hoffman2:$scratch/deepgo/data/BertNotFtAARawSeqGO/$onto/fold_1/2embPpiAnnotE256H1L12I512Set0/
done


#### get classifier
#!/bin/bash
. /u/local/Modules/default/init/modules.sh
module load python/3.7.2
cd /u/scratch/d/datduong/PSLGOannotation/MakeData/FormatData/Classifier

WORKDIR='/u/scratch/d/datduong/deepgo'
OUTPUT_PATH=$WORKDIR'/data/PSLdata'
mkdir $OUTPUT_PATH
ONTO='biological_process' #'molecular_function' ## COMMENT
onto='bp' ## need because we use short name
OUTPUT_PATH=$WORKDIR'/data/PSLdata/'$ONTO
LABEL_SEEN=$WORKDIR/data/train/deepgo.$onto.csv

CLASSIFIER_NAME='BERT12' ## COMMENT
PROTEIN_NAME=$WORKDIR/data/train/fold_1/ProtAnnotTypeData/test-$onto-input.tsv # '/local/datdb/deepgo/data/train/fold_1/ProtAnnotTypeData/test-mf-input.tsv
OUTPUT_NAME=$CLASSIFIER_NAME'-cls'
MODEL_OUTPUT=$WORKDIR/data/BertNotFtAARawSeqGO/$onto/fold_1/2embPpiAnnotE256H1L12I512Set0/YesPpiYesTypeScaleFreezeBert12Ep10e10Drop0.1/prediction_train_all_on_test.pickle
python3 FormatClassifier.py $CLASSIFIER_NAME $WORKDIR/data $OUTPUT_PATH $LABEL_SEEN $PROTEIN_NAME $MODEL_OUTPUT $ONTO $OUTPUT_NAME

CLASSIFIER_NAME='PsiBLAST' ## COMMENT
PROTEIN_NAME=$WORKDIR/data/train/fold_1/test-$onto.tsv # /u/scratch/d/datduong/deepgo/data/train/fold_1/test-mf.tsv
OUTPUT_NAME=$CLASSIFIER_NAME'-cls'
MODEL_OUTPUT=$WORKDIR/data/train/fold_1/blastPsiblastResultEval10/test-$onto-prediction.pickle
python3 FormatClassifier.py $CLASSIFIER_NAME $WORKDIR/data $OUTPUT_PATH $LABEL_SEEN $PROTEIN_NAME $MODEL_OUTPUT $ONTO $OUTPUT_NAME

## COMMENT create things to be predicted
PROTEIN_NAME=$WORKDIR/data/train/fold_1/ProtAnnotTypeData/test-$onto-input.tsv
LABEL_COMPLETE=$WORKDIR/data/train/deepgo.$onto.csv
python3 FormatTarget.py $WORKDIR/data $OUTPUT_PATH $LABEL_SEEN $LABEL_COMPLETE $PROTEIN_NAME $ONTO

