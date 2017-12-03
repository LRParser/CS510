import pandas as pd
import os
from rdkit import Chem
import time
import gzip
import pickle

def main() :
    print("Processing PubChem FTP Download")

    sdf_root_path = "/media/data/pubchem/SDF"
    results_path = "/media/data/pubchem/smiles"

    try:
        os.makedirs(results_path)
    except :
        print("Results directory already exists")

    compound_read_count = 0
    max_smiles_len = 50
    keys = list()
    values = list()
    overall_start = time.time()

    all_paths = list()

    for path, dirs, filenames in os.walk(sdf_root_path) :
        for filename in filenames:

            if "102125001_102150000" in filename:
                continue

            file_path = os.path.join(sdf_root_path, filename)
            all_paths.append(file_path)

    all_paths.sort()

    for filepath in all_paths:

        print("Processing: {0}".format(filepath))
        start = time.time()

        with gzip.open(filepath,'rb') as myfile:
            suppl = Chem.ForwardSDMolSupplier(myfile)
            for mol in suppl:
                if mol is None: continue
                cid = mol.GetProp("PUBCHEM_COMPOUND_CID")
                try :
                    Chem.Kekulize(mol)
                    smiles = Chem.MolToSmiles(mol,kekuleSmiles=True)
                    if len(smiles) > max_smiles_len:
                        compound_read_count =compound_read_count + 1
                        #print("Skipped compound: {0} due to large size".format(cid))
                        continue

                    keys.append(int(cid))
                    values.append(smiles)
                except Exception:
                    #print(e)
                    continue
            end = time.time()

        print("Processed file, processed thru compound number: {0} in {1} seconds".format(compound_read_count, end - start))
        compound_read_count = compound_read_count + 1


    overall_end = time.time()
    secs_elapsed = overall_end - overall_start
    print("Parsed all smiles in: {0} seconds, or {1} minutes, or {2} hours".format(secs_elapsed,secs_elapsed/60,secs_elapsed/3600))

    #print("Sorting lists and saving pickle")
    #overall_start = time.time()
    #keys, values = (list(t) for t in zip(*sorted(zip(keys, values))))

    with open("/media/data/pubchem/kekulesmiles_tuple.pickle","wb") as f:
        pickle.dump((keys,values),f)
    print("Done")
    overall_end = time.time()
    secs_elapsed = overall_end - overall_start
    print("Sorted and saved smiles in: {0} seconds, or {1} minutes, or {2} hours".format(secs_elapsed, secs_elapsed / 60,
                                                                                   secs_elapsed / 3600))

if __name__ == '__main__':
    main()
