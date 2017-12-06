import pandas as pd
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, rdMolDescriptors
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold
import gensim
from gensim import models
import time
import pickle
import json
import urllib
import requests
import os
import gzip
import zipfile
import bisect

print("Loading smiles from disk")
with open('/media/data/pubchem/kekulesmiles_tuple.pickle',"rb") as f:
    keys, values = pickle.load(f)
print("Loaded data from disk")

gene_symbol = "PPARG"
# Use an API call to find all related bioassays. For now, use the assays related to PPAR gamma
assays_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/{0}/aids/TXT".format(gene_symbol)
r = requests.get(assays_url)
relevant_assays = [int(x) for x in r.text.split('\n') if len(x) > 0]
print(len(relevant_assays))

assay_dir = "/media/data/pubchem/Data"

# Each assay n is in a file starting from 0001 to 1000, etc

assay_paths = list()

dfs = list()
fingerprints = list()
activities = list()

for assay_num in relevant_assays:
    print(assay_num)
    # Round assay into down to nearest thousand
    assay_num_rounded_lower = assay_num - (assay_num % 1000) + 1
    assay_num_rounded_upper = assay_num_rounded_lower + 999
    expected_folder_name = "{0:0>7}_{1:0>7}".format(assay_num_rounded_lower, assay_num_rounded_upper)
    expected_name = "{0}.zip".format(expected_folder_name)
    expected_path = os.path.join(assay_dir, expected_name)
    assay_paths.append(expected_path)
    archive = zipfile.ZipFile(expected_path, 'r')

    with archive.open(expected_folder_name + '/' + str(assay_num) + ".csv.gz") as f:
        with gzip.open(f) as g:
            df = pd.read_csv(g)
            df["IS_ACTIVE"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"
            df["IS_ACTIVE"].astype(bool)

            df_active = df[df["IS_ACTIVE"] == True]
            df_inactive = df[df["IS_ACTIVE"] == False]
            print("Active are: {}, Inactive are: {}".format(df_active.count()["PUBCHEM_CID"],
                                                            df_inactive.count()["PUBCHEM_CID"]))

            dfs.append(df)
            print("Added assay: " + str(assay_num))

cids = list()
fingerprints = list()
activities = list()
mols = list()

for df in dfs:
    cid = row["PUBCHEM_CID"]
