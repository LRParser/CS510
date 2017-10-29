import pandas as pd
import os
from pathlib import Path
from rdkit import Chem
import pickle
import time
import gzip

def main() :
    print("Processing PubChem FTP Download")

    sdf_root_path = "/home/joe/media/data/pubchem/SDF"
    results_path = "/home/joe/media/data/pubchem/smiles"

    try:
        os.makedirs(results_path)
    except :
        print("Results directory already exists")

    i = 0

    all_keys = list()
    all_values = list()

    for path, dirs, filenames in os.walk(sdf_root_path) :
        for filename in filenames:

            print("Processing: {0}".format(filename))

            new_file_name = os.path.join(results_path,filename.replace(".sdf.gz","_smiles.csv"))

            if os.path.exists(new_file_name) :
                print("Already processed: {0}".format(new_file_name))
                continue

            keys = list()
            values = list()

            start = time.time()
            filepath = os.path.join(sdf_root_path,filename)
            
            with gzip.open(filepath,'rb') as myfile:
                suppl = Chem.ForwardSDMolSupplier(myfile)
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

    with open("/home/joe/media/data/pubchem/cid_map.pickle","wb") as f:
        pickle.dump((all_keys,all_values),f,protocol=pickle.HIGHEST_PROTOCOL)

    print("Stored data as pickle")
    print("Done")

if __name__ == '__main__':
    main()
