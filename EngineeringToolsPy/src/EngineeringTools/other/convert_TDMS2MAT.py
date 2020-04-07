#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

'''
EngineeringTools.other.convert_TDMS2MAT

'''

import sys
import os

from nptdms import TdmsFile
import scipy.io

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__author__ = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__ = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"


DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def convert_TDMS2MAT(tdms_filename, mat_filename, struct):
    tdms_file = TdmsFile(tdms_filename)
    tdms_df = tdms_file.as_dataframe(time_index=False)
    trans = {key : key.replace("'", '').replace("/", '_')[1:] for key in tdms_df.keys()}
    tdms_df_ = tdms_df.rename(columns=trans)
    matdata = {col_name : tdms_df_[col_name].values for col_name in tdms_df_.columns.values}
    scipy.io.savemat(mat_filename, {struct:matdata}, do_compression=True, oned_as='column')



def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s


  Licensed under the BSD 3-clause License

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-s", "--struct", dest="struct", help="name of the structure in the matfile where the data will be stored", default='tdms')
        parser.add_argument("-m", "--mat", dest="mat_filename", action="store", help="path and filename of the mat file, destination; default: tdms filename + '.mat'", default=None)
        parser.add_argument("tdms_filename", action="store", help="path and filename of the tdms file, source")                        

        # Process arguments
        args = parser.parse_args()

        tdms_filename = args.tdms_filename
        if args.mat_filename:
            mat_filename = args.mat_filename
        else:
            mat_filename = os.path.splitext(tdms_filename)[0] + '.mat'
        struct = args.struct

        print('converting "{}" to "{}" : "{}"'.format(tdms_filename, mat_filename, struct))
        convert_TDMS2MAT(tdms_filename, mat_filename, struct)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        d = 0
        if d == 0:
            sys.argv.append("-h")
        if d == 1:
            sys.argv.append("test.tdms")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'EngineeringTools.other.convert_TDMS2MAT2_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

#eof