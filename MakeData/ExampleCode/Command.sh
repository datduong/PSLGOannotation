


for file in Sample SimilarLabel Subset Label ErrorLink ClassifierLink Classifier ClassifierPredict Rating_target Rating_truth ; do
perl -p -i -e 's/ /\t/g' $file.txt
done

java -jar psl-cli-2.1.0.jar --learn --model rule.psl --data input.data

java -jar psl-cli-2.1.0.jar --infer --model rule-learned.psl --data input.data --output scratch_testing

sort -V scratch_testing/CLASSIFIERPREDICT.txt

# java -jar psl-cli-2.1.0.jar --learn --model preference-prediction.psl --data preference-prediction-learn.data

#### EXAMPLE

3 and 4 similar

C1 P1 3 0.8 so C1 P1 4 high
C2 P1 3 0.0 so C2 P1 4 low
  --> T P1 4 should be high + low

C1 P2 3 0.6 --> C1 P2 4 medium high
C2 P2 3 0.1 --> C2 P2 4 low
  --> T P2 4 should be medium high + low (should be less than T P1 4)

'T'     'P1'    '2'     0.5159568190574646 -->> looks like simple average
'T'     'P1'    '3'     0.42127561569213867
'T'     'P1'    '4'     0.7367483973503113 --> higher than T P2 #EXAMPLE
'T'     'P1'    '5'     0.5080637335777283
'T'     'P2'    '2'     0.7106379866600037
'T'     'P2'    '3'     0.36329710483551025
'T'     'P2'    '4'     0.5493872761726379 --> lower than T P1 #EXAMPLE
'T'     'P2'    '5'     0.368010014295578