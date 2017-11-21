import pandas as pd
import os
from rdkit import Chem
import time
import gzip

f = gzip.open("/media/data/pubchem/SDF/Compound_001500001_001525000.sdf.gz","rb")

suppl = Chem.ForwardSDMolSupplier(f)

for mol in suppl :
    if mol is None:
        continue
    cid = mol.GetProp("PUBCHEM_COMPOUND_CID")

    if int(cid) == 1511280:
        for name in mol.GetPropNames() :
            print(name)
        print(mol.GetProp("PUBCHEM_OPENEYE_CAN_SMILES"))

    #print(cid)


f.close()