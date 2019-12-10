


cd /u/scratch/d/datduong/deepgo/data/PSLdata/molecular_function
scp /u/scratch/d/datduong/PSLGOannotation/MakeData/ExampleCode/psl-cli-2.1.0.jar .

# for file in Sample SimilarLabel Subset Label ErrorLink ClassifierLink Classifier ClassifierPredict Classifier_target Rating_truth ; do
# perl -p -i -e 's/ /\t/g' $file.txt
# done

## train
java -jar psl-cli-2.1.0.jar --learn --model rule.psl --data input.data

## inference
java -jar psl-cli-2.1.0.jar --infer --model rule-learned.psl --data input.data --output scratch_testing
