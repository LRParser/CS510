import rdkit
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import pandas as pd

import gensim, logging

def main() :
    suppl = Chem.SDMolSupplier("Compound_000025001_000050000.sdf")
    all_keys = list()


    for mol in suppl:

        if not mol:
            continue

        info = {}
        rdMolDescriptors.GetMorganFingerprint(mol,1,bitInfo=info)
        keys = info.keys()
        keys_string = list()
        keys_list = list(keys)
        for k in keys_list:
            print(k,end=' ')
            #keys_string.append(str(k))
        print()
        all_keys.append(keys_string)

    #dictionary = corpora.Dictionary(texts)
    #corpus = [dictionary.doc2bow(text) for text in keys_string]
    #model = gensim.models.Word2Vec(keys_string, min_count=1)
    #model.build_vocab(keys_string)
    #print(model.wv["2246728737"])


if __name__ == "__main__" :
    main()
