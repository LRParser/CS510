import ftplib
import os
import time

def main() :
    ftp = ftplib.FTP("ftp.ncbi.nih.gov")
    ftp.login("anonymous", "anonymous")
    ftp.cwd("/pubchem/Compound/CURRENT-Full/SDF")
    try :
        os.mkdir("SDF")
    except :
        print("Directory SDF already exists")

    filelist = ftp.nlst()
    print("Downloading: {0} files".format(len(filelist)))
    i = 0
    for filename in filelist:

        local_filename = os.path.join('SDF', filename)
        with open(local_filename, 'wb') as file :
            ftp.retrbinary('RETR ' + filename, file.write)
        i = i + 1
        print("Downloaded file {0} of {1}".format(i,len(filelist)))

    ftp.quit()

if __name__ == "__main__" :
    main()



