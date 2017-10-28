# CS510

## Setup

Prerequisites: Ubuntu 16.04, Anaconda from https://www.anaconda.com/download/#linux, Chrome Browser (for jupyter notebook)

Run:

```
./bootstrap.py
source activate cs510-env
jupyter notebook
```

Then open classifier.ipynb in the opened notebook


Notes:

To get compounds used in assay 1032, do

```
cat /media/data/pubchem/Data/0001001_0002000/1032.csv | cut -d, -f3 > CIDS_ASSAY_1032.csv
```
