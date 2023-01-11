# AthaMap
This repository contains scripts associated with the AthaMap database and related transcription factor analyses. Most scripts are included for documentation purposes and might not be helpful beyond the described purpose.


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
This script screens a given genome sequence for all occurrences of TF binding sites based on the provided PWM.

```
Usage
python3 PWM_screen.py --pwm <FILE> --seq <FILE> --out <FILE>

Mandatory:
--pwm       STR     Input PWM file
--seq       STR     Input FASTA file
--out       STR     Output file
```


`--pwm` specifies the PWM input file (.txt) that provides the information for the identification of TF binding sites.

`--seq` specifies the FASTA input file that contains the sequences that will be screened for TF binding sites.

`--out` specifies the output file (.txt) that lists all identified TF binding sites.





## Analyze co-expression of TFs with their putative target genes
This script compares the co-expression of TFs with their target genes against co-expression with a random set of genes.

```
Usage1
python3 cis2coexp.py --cis <FILE> --exp <FILE> --ref <STR> --out <FILE>

Usage2
python3 cis2coexp.py --cisdir <FOLDER> --exp <FILE> --reffile <FILE> --out <FILE>

Mandatory1:
--cis       STR     Input target gene file
--exp       STR     Input expression file
--ref       STR     AGI of TF
--out       STR     Output file

Mandatory2:
--cisdir    STR     Folder containing input target gene files
--exp       STR     Input expression file
--reffile   STR     File containing AGIs of TFs
--out       STR     Output file

Optional:
--cutoff    FLOAT   Mininmal score cutoff
```


`--cis` specifies the target gene input file.

`--exp` specifies the gene expression input file.

`--ref` specifies the Arabidopsis Gene Identifier (AGI) of the analzyed TF.

`--out` specifies the output file.

`--cisdir` specifies a folder containing the target gene input files.

`--reffile` specifies a file containing the AGIs of the analyzed TFs.

`--cutoff` specifies the minimal score that should be considered.


## Transfer positions between annotation versions
This script allows the transfer of cis-regulatory elements annotated in AthaMap based on the _Arabidopsis thaliana_ genome sequence TAIR8 to TAIR10.

```
Usage
python3 pos_transfer.py --in <FILE> --tair10 <FILE> --tair8 <FILE> --out <FILE>

Mandatory:
--in       STR     Input cis-regulatory element file
--tair10   STR     Input TAIR10 FASTA file
--tair8    STR     Input TAIR8 FASTA file
--out      STR     Output cis-regulatory element file
```


`--in` specifies the input file that contains information about the positions of cis-regulatory elements based on TAIR8. This file can be downloaded from AthaMap.

`--tair10` specifies the _Arabidopsis thaliana_ genome sequence TAIR10 FASTA file.

`--tair8` specifies the _Arabidopsis thaliana_ genome sequence TAIR8 FASTA file.

`--out` specifies the output file that contains information about the positions of cis-regulatory elements based on TAIR10.



# References




