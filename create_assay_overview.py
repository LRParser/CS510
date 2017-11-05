import pandas as pd
import os
from pathlib import Path
from rdkit import Chem
import pickle
import time

def main():
    print("Loading SMILES/CIDs from reference CSV")

    root_df = pd.read_csv("/media/data/pubchem/summary.csv",index_col="PUBCHEM_CID")
    root_path = "/media/data/pubchem/Data"

    df_list = list()

    for path, dirs, filenames in os.walk(root_path) :
        for dir in dirs:

            # Each directory holds a range of assay results

            joined_path = os.path.join(root_path,dir)

            for path, dirs, filenames in os.walk(joined_path) :
                for filename in filenames:

                    if filename not in ["1030.csv","1379.csv"]:
                        continue

                    assay_name = filename.replace(".csv","")
                    print("Parsing: {0}".format(assay_name))

                    file_path = os.path.join(joined_path,filename)

                    # Open each assay result

                    df = pd.read_csv(file_path)

                    df = df.dropna(subset=["PUBCHEM_CID"])

                    #for index, row in df['PUBCHEM_CID'].iteritems():
                    #    if pd.isnull(row):
                    #        print('index:', index, 'isnull')

                    df["ACTIVITY_OUTCOME"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == 'Active'
                    df["ACTIVITY_OUTCOME"].astype(int)

                    df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
                    cid_series = df["PUBCHEM_CID"].values


                    #cid_series = pd.to_numeric()
                    outcome_series = df["ACTIVITY_OUTCOME"].values
                    smiles_series = list()
                    cids_kept = list()
                    outcomes_kept = list()
                    for cid, outcome in zip(cid_series,outcome_series):
                        print(cid)
                        try :
                            ref_row = root_df.iloc[cid]
                            if(ref_row is not None and ref_row["SMILES"] is not None) :
                                smile = ref_row.SMILES
                                cids_kept.append(cid)
                                smiles_series.append(smile)
                                outcomes_kept.append(outcome)

                        except :
                            print("Passed on CID")

                    parsed_df = pd.DataFrame({"PUBCHEM_CID" : cids_kept, assay_name : outcomes_kept, "SMILES" : smiles_series})
                    parsed_df.set_index("PUBCHEM_CID")

                    df_list.append(parsed_df)
                    print(assay_name)

                    print("Count of parsed: {0}".format(parsed_df.count()))


    # Now parse all results smile files into one big file



    df_full = pd.concat(df_list)

    df_full.to_csv("/media/data/pubchem/assay_summary.csv",index=False)

if __name__ == "__main__" :
    main()
