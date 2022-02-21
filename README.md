# AthaMap
This repository contains scripts associated with the AthaMap2 database. Most scripts are included for documentation purposes. The


## Combine Position Weight Matrices (PWMs) of the same TF binding site
This script takes different PWMs that belong to the same transcription factor and calculates an average value for individual positions. The motifs are reduced to the smalles suppported size to enable a sensitive analysis.

```
Usage
python3 PWM_merger.py --in <FOLDER> --info <FILE> --out <FOLDER>

Mandatory:
--in        STR     Input folder with PWM files
--info      STR     Info table file
--out       STR     Output folder for PWM files
```


`--in` specifies the input folder that contains PWM files. Text files (.txt) in this folder will be processed if they are mentioned in the info table (`--info`).

`--info` specifies an information input table that connects different PWMs of the same transcription factor. The transcritpion factor ID is given in the first column. The PWM ID is given in the fourth column.

`--out` specifies the output folder. This folder will be created if it does not exist already. Output files will be placed in this folder.



## Screen genome sequence for motifs based on PWMs



## Analyze co-expression of TFs with their putative target genes



## Transfer positions between annotation versions


