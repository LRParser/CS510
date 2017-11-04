import pandas as pd
import os
from pathlib import Path
from rdkit import Chem
import pickle
import time

def main():
    print("Loading data from pickle")

    #with open("cid_map.pickle","rb") as f:
    #    (keys, values) = pickle.load(f)

    pd.read_csv("/media/data/pubchem/summary.csv")


    root_path = "/media/data/pubchem/Data"
    root_df = pd.DataFrame({"PUBCHEM_CID" : keys, "SMILES" : values})
    df_list = list()

    for path, dirs, filenames in os.walk(root_path) :
        for dir in dirs:

            # Each directory holds a range of assay results

            joined_path = os.path.join(root_path,dir)

            for path, dirs, filenames in os.walk(joined_path) :
                for filename in filenames:

                    file_path = os.path.join(joined_path,filename)

                    # Open each assay result

                    df = pd.read_csv(file_path)

                    df["ACTIVITY_OUTCOME"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == 'Active'
                    df["ACTIVITY_OUTCOME"].astype(bool)

                    cid_series = df["PUBCHEM_CID"].astype(int)
                    outcome_series = df["ACTIVITY_OUTCOME"]
                    #smiles_series = list()
                    #for cid in cid_series:
                    #    smile = values[keys.index(cid)]
                    #    smiles_series.append(smile)

                    assay_name = filename.replace(".csv","")
                    parsed_df = pd.DataFrame({"PUBCHEM_CID" : cid_series, assay_name : outcome_series, "SMILES" : smiles_series})

                    df_list.append(parsed_df)
                    print(assay_name)

                    print("Count of parsed: {0}".format(parsed_df.count()))


    # Now parse all results smile files into one big file



    df_full = pd.concat(df_list)

    root_df.to_csv("/media/data/pubchem/pcba_full.csv")

if __name__ == "__main__" :
    main()
