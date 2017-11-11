import sys
import urllib2


def getResponse(url):
    try:
        connection = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return ""
    else:
        return connection.read().rstrip()


def cidToSmiles(cid):
    return getResponse("http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/IsomericSMILES/TXT" % cid)


def aidToCsvFile(aid):

	result = getResponse("https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/%s/CSV" % aid)

	if not result:
		return -1
	else:
		outfile_name = "AID_" + aid + "_datatable_all.csv"
		outfile = open(outfile_name, 'w+')
		outfile.write(result)
		outfile.close()
		return 0


def main():
	if len(sys.argv) < 2:
		print "Please enter an Assay number."
		sys.exit(1)

	aid = sys.argv[1]
	if aidToCsvFile(aid) == -1:
		print "No results were returned for aid %s." % aid


if __name__ == "__main__":
	main()
