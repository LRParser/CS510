import rdkit
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import pandas as pd
import gzip
import os

def main() :

    sdf_root_path = "/media/data/pubchem/SDF"
    i = 0
    max_num = 5000000
    for path, dirs, filenames in os.walk(sdf_root_path) :
        for filename in filenames:
            filepath = os.path.join(sdf_root_path, filename)

            if "Compound_102125001_102150000" in filename:
                continue

            i = i + 1

            if(i >= max_num) :
                break


            if(i % 100000 == 0) :
                print("Now featurizing: {}".format(i))

            with gzip.open(filepath, 'rb') as myfile:
                suppl = Chem.ForwardSDMolSupplier(myfile)

                for mol in suppl:

                    if not mol:
                        continue

                    try :
                        info = {}
                        rdMolDescriptors.GetMorganFingerprint(mol,1,bitInfo=info)
                        keys = info.keys()
                        keys_list = list(keys)
                        for k in keys_list:
                            print(k,end=' ')
                        print()
                    except Exception:
                        pass

if __name__ == "__main__" :
    main()
