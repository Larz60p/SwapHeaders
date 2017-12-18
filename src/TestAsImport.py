import SwapHeaders

def testit(file1name, file2name, outfilename):
    sh = SwapHeaders.SwapHeaders(origfile=file1name, headerfile=file2name, outfile=outfilename)
    sh.make_new_file()
    sh.close_files()

if __name__ == '__main__':
    testit(file1name='File1.txt', file2name='File2.txt', outfilename='Newfile.txt')
