
## 

for onto in mf cc bp ; do 
  mkdir $SCRATCH/deepgo/data/BertNotFtAARawSeqGO/mf/fold_1/2embPpiAnnotE256H1L12I512Set0/ProtAnnotTypeLarge/
done 

for onto in mf cc bp ; do
  scp -r /local/datdb/deepgo/data/BertNotFtAARawSeqGO/mf/fold_1/2embPpiAnnotE256H1L12I512Set0/ProtAnnotTypeLarge/YesPpiYesTypeScaleFreezeBert12Ep10e10Drop0.1 $hoffman2:$scratch/deepgo/data/BertNotFtAARawSeqGO/mf/fold_1/2embPpiAnnotE256H1L12I512Set0/ProtAnnotTypeLarge/
done 



