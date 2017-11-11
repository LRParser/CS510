import pandas as pd
import os
import functools
import psycopg2
import dask
import dask.dataframe as dd
import numpy as np

def main():
    #dask.set_options(get=dask.async.get_sync)

    print("Loading SMILES/CIDs from reference CSV")

    #root_df = pd.read_csv("/media/data/pubchem/summary.csv",index_col="PUBCHEM_CID")
    #root_df = dd.from_pandas(root_df,npartitions=20)
    root_path = "/media/data/pubchem/Data"

    root_df = None

    df_list = list()

    names_to_parse = "PCBA-1030,PCBA-1379,PCBA-1452,PCBA-1454,PCBA-1457,PCBA-1458,PCBA-1460,PCBA-1461,PCBA-1468,PCBA-1469,PCBA-1471,PCBA-1479,PCBA-1631,PCBA-1634,PCBA-1688,PCBA-1721,PCBA-2100,PCBA-2101,PCBA-2147,PCBA-2242,PCBA-2326,PCBA-2451,PCBA-2517,PCBA-2528,PCBA-2546,PCBA-2549,PCBA-2551,PCBA-2662,PCBA-2675,PCBA-2676,PCBA-411,PCBA-463254,PCBA-485281,PCBA-485290,PCBA-485294,PCBA-485297,PCBA-485313,PCBA-485314,PCBA-485341,PCBA-485349,PCBA-485353,PCBA-485360,PCBA-485364,PCBA-485367,PCBA-492947,PCBA-493208,PCBA-504327,PCBA-504332,PCBA-504333,PCBA-504339,PCBA-504444,PCBA-504466,PCBA-504467,PCBA-504706,PCBA-504842,PCBA-504845,PCBA-504847,PCBA-504891,PCBA-540276,PCBA-540317,PCBA-588342,PCBA-588453,PCBA-588456,PCBA-588579,PCBA-588590,PCBA-588591,PCBA-588795,PCBA-588855,PCBA-602179,PCBA-602233,PCBA-602310,PCBA-602313,PCBA-602332,PCBA-624170,PCBA-624171,PCBA-624173,PCBA-624202,PCBA-624246,PCBA-624287,PCBA-624288,PCBA-624291,PCBA-624296,PCBA-624297,PCBA-624417,PCBA-651635,PCBA-651644,PCBA-651768,PCBA-651965,PCBA-652025,PCBA-652104,PCBA-652105,PCBA-652106,PCBA-686970,PCBA-686978,PCBA-686979,PCBA-720504,PCBA-720532,PCBA-720542,PCBA-720551,PCBA-720553,PCBA-720579,PCBA-720580,PCBA-720707,PCBA-720708,PCBA-720709,PCBA-720711,PCBA-743255,PCBA-743266,PCBA-875,PCBA-881,PCBA-883,PCBA-884,PCBA-885,PCBA-887,PCBA-891,PCBA-899,PCBA-902,PCBA-903,PCBA-904,PCBA-912,PCBA-914,PCBA-915,PCBA-924,PCBA-925,PCBA-926,PCBA-927,PCBA-938,PCBA-995".split(',')

    i = 0

    print("Total assays: {0}".format(len(names_to_parse)))

    #con = psycopg2.connect("")
    #cur = con.cursor()

    full_df = None

    for path, dirs, filenames in os.walk(root_path) :
        for dir in dirs:

            # Each directory holds a range of assay results
            joined_path = os.path.join(root_path,dir)

            for path, dirs, filenames in os.walk(joined_path) :
                for filename in filenames:

                    assay_name = "PCBA-" + filename.replace(".csv","")

                    if assay_name not in names_to_parse:
                        continue

                    print("Parsing: {0}".format(assay_name))

                    file_path = os.path.join(joined_path,filename)

                    # Open each assay result
                    #

                    df = pd.read_csv(file_path,usecols=["PUBCHEM_CID","PUBCHEM_ACTIVITY_OUTCOME"])
                    df = df.dropna()
                    df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
                    df.set_index("PUBCHEM_CID")


                    df["ACTIVITY_OUTCOME"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == 'Active'
                    df = df.drop(["PUBCHEM_ACTIVITY_OUTCOME"],axis=1)
                    df["ACTIVITY_OUTCOME"] = df["ACTIVITY_OUTCOME"].astype(np.bool)
                    df = df.rename(columns={'ACTIVITY_OUTCOME': assay_name})

                    print(df.head())

                    #df["ACTIVITY_OUTCOME"] = df["ACTIVITY_OUTCOME"].astype(bool)

                    #cid_series = df["PUBCHEM_CID"].values

                    if root_df is None :
                        root_df = df
                        #root_df = dd.from_pandas(root_df,npartitions=20)
                    else :
                        root_df = root_df.merge(df,how='outer',on="PUBCHEM_CID")
                        root_df = root_df.to_sparse()
                        #root_df = root_df.append(df[assay_name])
                        #root_df.compute()
                        #
                    #root_df.compute()
                    #df_list.append(parsed_df)

                    #parsed_df.to_csv("/media/data/pubchem/"+assay_name,index=False)

                    #current_results = pd.read_csv(summary_path)
                    #current_results.set_index("mol_id")

                    #merged_df = current_results.merge(parsed_df,on="mol_id")
                    #merged_df.to_csv(summary_path)


                    #df_list.append(parsed_df)
                    print(assay_name)
                    #root_df.drop_duplicates(inplace=True)

                    print(root_df.head())


                    print("Count of Merged: {0}".format(root_df.count()))

                    i = i + 1

                    print("Assays processed: {0}".format(i))

    #df_final = pd.concat(df_list)

    #print("Creating summary")

    #df_final = functools.reduce(lambda left, right: pd.merge(left, right), df_list)
    #df_final = df_final.fillna(0)

    #print(root_df.head())


    root_df.to_csv("/media/data/pubchem/assay_final.csv",index=False)

if __name__ == "__main__" :
    main()
