import pandas as pd
import os
from pathlib import Path
from rdkit import Chem
import pickle
import time

def main() :
    print("Processing PubChem FTP Download")

    sdf_root_path = "/media/data/pubchem/SDF"
    i = 0

    all_keys = list()
    all_values = list()

    for path, dirs, filenames in os.walk(sdf_root_path) :
        for filename in filenames:

            new_file_name = os.path.join("/media/data/pubchem/smiles/",filename.replace(".sdf","_smiles.csv"))

            if os.path.exists(new_file_name) :
                continue

            keys = list()
            values = list()

            start = time.time()
            filepath = os.path.join(sdf_root_path,filename)
            suppl = Chem.SDMolSupplier(filepath)
            for mol in suppl:
                if mol is None: continue
                cid = mol.GetProp("PUBCHEM_COMPOUND_CID")
                smiles = mol.GetProp("PUBCHEM_OPENEYE_ISO_SMILES")
                keys.append(cid)
                values.append(smiles)
                all_keys.append(cid)
                all_values.append(smiles)
            end = time.time()
            print("Processed file number: {0} in {1} seconds".format(i, end - start))
            i = i + 1

            df = pd.DataFrame({"PUBCHEM_CID" : keys, "SMILES" : values},index=keys)
            df.to_csv(new_file_name,index=False)


    print("Done mapping CIDs to smiles, storing as pickle")

    with open("cid_map.pickle","wb") as f:
        pickle.dump((all_keys,all_values),f,protocol=pickle.HIGHEST_PROTOCOL)

    print("Stored data as pickle")
    print("Done")

if __name__ == '__main__':
    main()