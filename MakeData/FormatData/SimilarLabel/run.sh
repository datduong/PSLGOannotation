

#!/bin/bash
. /u/local/Modules/default/init/modules.sh
module load python/3.7.2
cd /u/scratch/d/datduong/PSLGOannotation/MakeData/FormatData/SimilarLabel
python3 FormatSimilarLabel.py

