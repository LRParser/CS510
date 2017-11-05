import psycopg2


print("Saving CID/SMILES mapping to database")

con = psycopg2.connect("")

# Ran command 'CREATE TABLE pubchem'
# CREATE TABLE pubchem ( PUBCHEM_CID bigint PRIMARY KEY, SMILES varchar (2000) NOT NULL);
#

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pubchem ( PUBCHEM_CID bigint PRIMARY KEY, SMILES varchar (200) NOT NULL);")
cur.execute("COPY pubchem FROM '/media/data/pubchem/summary.csv' delimiter ',' csv header;")
con.commit()
cur.close()
con.close()