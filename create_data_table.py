import pandas as pd
import os
from pathlib import Path
from rdkit import Chem
import pickle


def main() :
    print("Test")

    sdf_root_path = "/media/data/pubchem/SDF"
    cid_smiles_map = dict()
    i = 0
    for path, dirs, filenames in os.walk(sdf_root_path) :
        for filename in filenames:

            filepath = os.path.join(sdf_root_path,filename)
            suppl = Chem.SDMolSupplier(filepath)
            for mol in suppl:
                if mol is None: continue
                cid = mol.GetProp("PUBCHEM_COMPOUND_CID")
                smiles = mol.GetProp("PUBCHEM_OPENEYE_ISO_SMILES")
                cid_smiles_map[cid] = smiles
            i = i + 1
            if i % 50 == 0 :
                print("Processed file number: {0}".format(i))

    print("Done mapping CIDs to smiles, storing as pickle")

    with open("cid_map.pickle","wb") as f:
        pickle.dump(cid_smiles_map,f,protocol=pickle.HIGHEST_PROTOCOL)

    print("Stored data as pickle")

    root_path = "/media/data/pubchem/Data"
    root_dir = Path(root_path)
    root_df = pd.DataFrame()

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
                    smiles_series = list()
                    for cid in cid_series:
                        smile = cid_smiles_map[cid]
                        smiles_series.append(smile)

                    assay_name = filename.replace(".csv","")
                    parsed_df = pd.DataFrame({"PUBCHEM_CID" : cid_series, assay_name : outcome_series, "SMILES" : smiles_series})


                    print(assay_name)

                    print("Count of parsed: {0}".format(parsed_df.count()))
                    root_df = root_df.merge(parsed_df)
                    print("Count of master: {0}".format(root_df.count()))

            #print(dir)


    # dirs = [x for x in root_dir.iterdir() if x.is_dir()]
    # for dir in dirs:
    #     print(dir)

    master_df = pd.DataFrame()

    # First, add a column for every assay from PubChem FTP



    # file_list = [f for f in root_dir.glob('**/*') if f.is_file()]
    #
    # for file_name in file_list:
    #     # For every compound, we store its smiles and result for every bioassay
    #     # We use 0 for inactive, blank for unknown, and 1 for active
    #
    #     df = pd.read_csv(file_name)






    print("Done")

if __name__ == '__main__':
    main()