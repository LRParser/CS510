import pandas as pd
import os
import pickle
import array

root_path = "/media/data/pubchem/Data"


def create_cid_list(assays_to_parse) :

    assays_parsed = list()
    assay_paths = list()
    cid_set = set()
    i = 0

    for path, dirs, filenames in os.walk(root_path) :
        for dir in dirs:

            # Each directory holds a range of assay results
            joined_path = os.path.join(root_path,dir)

            for path, dirs, filenames in os.walk(joined_path) :
                for filename in filenames:

                    assay_name = "PCBA-" + filename.replace(".csv","")

                    if (assay_name not in assays_to_parse):
                        continue

                    print("Parsing: {0}".format(assay_name))

                    file_path = os.path.join(joined_path,filename)
                    assay_paths.append(file_path)

                    df = pd.read_csv(file_path,usecols=["PUBCHEM_CID","PUBCHEM_ACTIVITY_OUTCOME"])
                    df = df.dropna()
                    df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
                    df = df.set_index("PUBCHEM_CID")
                    #df = df[~df.index.duplicated(keep='first')]

                    cid_set = cid_set.union(set(df.index.values))

                    i = i + 1

                    assays_parsed.append(assay_name)

                    print("Assays processed: {0}".format(i))

    return assays_parsed, assay_paths, cid_set

def main():

    parse_128_only = True

    pcba_128 = "PCBA-1030,PCBA-1379,PCBA-1452,PCBA-1454,PCBA-1457,PCBA-1458,PCBA-1460,PCBA-1461,PCBA-1468,PCBA-1469,PCBA-1471,PCBA-1479,PCBA-1631,PCBA-1634,PCBA-1688,PCBA-1721,PCBA-2100,PCBA-2101,PCBA-2147,PCBA-2242,PCBA-2326,PCBA-2451,PCBA-2517,PCBA-2528,PCBA-2546,PCBA-2549,PCBA-2551,PCBA-2662,PCBA-2675,PCBA-2676,PCBA-411,PCBA-463254,PCBA-485281,PCBA-485290,PCBA-485294,PCBA-485297,PCBA-485313,PCBA-485314,PCBA-485341,PCBA-485349,PCBA-485353,PCBA-485360,PCBA-485364,PCBA-485367,PCBA-492947,PCBA-493208,PCBA-504327,PCBA-504332,PCBA-504333,PCBA-504339,PCBA-504444,PCBA-504466,PCBA-504467,PCBA-504706,PCBA-504842,PCBA-504845,PCBA-504847,PCBA-504891,PCBA-540276,PCBA-540317,PCBA-588342,PCBA-588453,PCBA-588456,PCBA-588579,PCBA-588590,PCBA-588591,PCBA-588795,PCBA-588855,PCBA-602179,PCBA-602233,PCBA-602310,PCBA-602313,PCBA-602332,PCBA-624170,PCBA-624171,PCBA-624173,PCBA-624202,PCBA-624246,PCBA-624287,PCBA-624288,PCBA-624291,PCBA-624296,PCBA-624297,PCBA-624417,PCBA-651635,PCBA-651644,PCBA-651768,PCBA-651965,PCBA-652025,PCBA-652104,PCBA-652105,PCBA-652106,PCBA-686970,PCBA-686978,PCBA-686979,PCBA-720504,PCBA-720532,PCBA-720542,PCBA-720551,PCBA-720553,PCBA-720579,PCBA-720580,PCBA-720707,PCBA-720708,PCBA-720709,PCBA-720711,PCBA-743255,PCBA-743266,PCBA-875,PCBA-881,PCBA-883,PCBA-884,PCBA-885,PCBA-887,PCBA-891,PCBA-899,PCBA-902,PCBA-903,PCBA-904,PCBA-912,PCBA-914,PCBA-915,PCBA-924,PCBA-925,PCBA-926,PCBA-927,PCBA-938,PCBA-995".split(',')
    #pcba_128 = "PCBA-1030,PCBA-1379".split(',')

    if parse_128_only :
        assays_to_parse = pcba_128
    else :
        ncgc_assays = list()
        with open("ncgc_bioassays.txt") as f:
            for line in f:
                ncgc_assays.append("PCBA-{0}".format(line))
        assays_to_parse = ncgc_assays

    pickle_path = 'data.cids.pickle'

    if os.path.isfile(pickle_path) :
        with open(pickle_path, 'rb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            (assays_parsed, assay_paths, cid_ref_list) = pickle.load(f)
            print("Loaded CID info from pickle")
    else :
        assays_parsed, assay_paths, cid_set = create_cid_list(assays_to_parse)
        cid_ref_list = list(cid_set)
        cid_ref_list.sort()
        assays_parsed.sort()
        assay_paths.sort()
        with open(pickle_path, 'wb') as f:
            pickle.dump((assays_parsed, assay_paths, cid_ref_list), f, pickle.HIGHEST_PROTOCOL)
            print("Wrote CID info to pickle")

    header_line = list()
    header_line.append("mol_id")
    header_line.append(",SMILES")
    for assay_name in assays_parsed:
        header_line.append(",")
        header_line.append(assay_name)
    header_line_txt = "".join(header_line)


    print("CID length is: {0}".format(len(cid_ref_list)))
    path_final = "/media/data/pubchem/assay_final.csv"
    assay_results = list()
    cid_len = len(cid_ref_list)

    for assay_path in assay_paths :

        filename = os.path.basename(assay_path)

        assay_name = "PCBA-" + filename.replace(".csv","")

        if assay_name not in assays_parsed:
            continue


        df = pd.read_csv(assay_path,usecols=["PUBCHEM_CID","PUBCHEM_ACTIVITY_OUTCOME"])
        df["IS_ACTIVE"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"
        df = df.rename(columns={'IS_ACTIVE': assay_name})
        df = df.dropna()
        df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
        df[assay_name] = df[assay_name].astype(int)
        df = df.set_index("PUBCHEM_CID")
        df = df[~df.index.duplicated(keep='first')]


        assay_results_array = array.array('i',(-1 for i in range(0,cid_len)))
        print(assay_path)
        for i in range(0,cid_len) :
            cid = cid_ref_list[i]
            if cid in df.index:
                #print(cid)
                val = df.get_value(cid, assay_name)
                #print(val)
            else:
                # Just write NA
                val = -1

            assay_results_array[i] = val

        assay_results.append(assay_results_array)
        print("Parsed: {0}".format(assay_name))


    # Now, write out the results csv, going line by line through all molecule results



    f_final = open(path_final, "w+")
    f_final.write(header_line_txt + "\n")

    assay_results_len = len(assay_results)

    pickle_path = "data.smiles.pickle"
    with open(pickle_path, 'rb') as f:
        keys_values_dict = pickle.load(f)
    print("Wrote CID info to pickle")

    for i in range(0,cid_len) :
        cid = cid_ref_list[i]
        # printing the mol_id
        line_for_comp = "CID"+str(cid)
        # printing the SMILES
        line_for_comp += ","+keys_values_dict[cid]
        for j in range(0,assay_results_len) :
            val = assay_results[j][i]
            if val == -1:
                line_for_comp += ","
            else:
                line_for_comp += "," + str(val)
        f_final.write(line_for_comp + "\n")

    f_final.close()


if __name__ == "__main__" :
    main()

