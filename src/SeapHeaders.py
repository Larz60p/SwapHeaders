# Replace header inoriginal file header with header in header file, writing output to outputfile
# Larz60+
from pathlib import Path
import argparse


class SwapHeaders:
    def __init__(self, origfile=None, headerfile=None, outfile=None):
        self.home = Path('.')
        self.data = self.home / 'data'
        self.original_file = self.data / origfile
        self.header_file = self.data / headerfile
        self.out_file = self.data / outfile

        with self.header_file.open() as fh:
            self.header_data = fh.readlines()

        self.orig = self.original_file.open()
        self.fo = self.out_file.open('w')

    def close_files(self):
        self.orig.close()
        self.fo.close()

    def get_replacement_header(self, match):
        retrec = None
        for line in self.header_data:
            if not line.startswith('>'):
                continue
            if match in line:
                retrec = line
                break
        return retrec

    def read_orig_record(self):
        """
        original file record read
        :return: data or False
        """
        while True:
            data = self.orig.readline()
            if not data:
                break
            yield data

    def make_new_file(self):
        with self.out_file.open('w') as fo:
            for orig in self.read_orig_record():
                match = None
                if orig.startswith('>'):
                    match = orig[1:]
                    x = match.rfind('.')
                    if x:
                        match = match[:x]
                    new = self.get_replacement_header(match)
                    if new is not None:
                        fo.write(new)
                    else:
                        fo.write(orig)
                else:
                    fo.write(orig)


def main():
    # Typical command line call python SwapHeaders.py -i 'File1.txt' -b 'File2.txt' -o 'Fileout.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ifile",
                        dest='original_filename',
                        help="Filename where headers are to be replaced",
                        action="store")

    parser.add_argument("-b", "--bfile",
                        dest='replace_original_filename',
                        help="Filename containing body",
                        action="store")

    parser.add_argument("-o", "--ofile",
                        dest='out_filename',
                        help="Output filename",
                        action="store")

    args = parser.parse_args()
    original_filename = args.original_filename

    replace_original_filename = args.replace_original_filename

    out_filename = args.out_filename

    sh = SwapHeaders(origfile=original_filename, headerfile=replace_original_filename, outfile=out_filename)
    sh.make_new_file()
    sh.close_files()


if __name__ == '__main__':
    main()
