


for file in SimilarLabel Subset Label ErrorLink ClassifierLink Classifier ClassifierPredict Rating_target Rating_truth ; do
perl -p -i -e 's/ /\t/g' $file.txt
done

java -jar psl-cli-2.1.0.jar --learn --model rule.psl --data input.data

java -jar psl-cli-2.1.0.jar --infer --model rule-learned.psl --data input.data --output scratch_testing


# java -jar psl-cli-2.1.0.jar --learn --model preference-prediction.psl --data preference-prediction-learn.data

