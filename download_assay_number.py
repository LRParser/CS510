import sys
##GB import os
##GB import pandas as pd
##GB from rdkit import Chem
from pubchempy import *


if len(sys.argv) < 2:
	print "Please enter an Assay number."
	sys.exit(1)
aid = sys.argv[1]


download('CSV', aid + '_CID_SMILES_Mapping.csv', [aid], operation='property/CanonicalSMILES,IsomericSMILES', overwrite=True)

outfile_name = "AID_" + sys.argv[1] + "_datatable_all.csv"
outfile = open(outfile_name, 'w+')


a = Assay.from_aid(aid)
### Testing
print a.target
sid = a.aid  ## For some reason, according to docs: The PubChem Substance Idenfitier (SID).
s = Substance.from_sid(sid)
print s.cids


### I'm not sure if the parsing is ok if there are multiple dicts in results
### See http://pubchempy.readthedocs.io/en/latest/api.html
for curr_dict in a.results:

	outfile.write("PUBCHEM_RESULT_TAG,PUBCHEM_SID,PUBCHEM_CID,PUBCHEM_ACTIVITY_OUTCOME,PUBCHEM_ACTIVITY_SCORE,PUBCHEM_ACTIVITY_URL,PUBCHEM_ASSAYDATA_COMMENT,Activation\n")

	result_type = curr_dict["type"]
	outfile.write("RESULT_TYPE,,,,,,," + str(result_type) + "\n")

	### Note, result_descr can have more than one entry
	result_descr = curr_dict["description"]
	outfile.write("RESULT_DESCR,,,,,,," + str(result_descr[0]) + "\n")

	result_unit = curr_dict["tc"]["unit"]
	outfile.write("RESULT_UNIT,,,,,,," + str(result_unit) + "\n")

	result_conc = curr_dict["tc"]["concentration"]
	outfile.write("RESULT_ATTR_CONC_MICROMOL,,,,,,," + str(result_conc) + "\n")

	
outfile.close()
