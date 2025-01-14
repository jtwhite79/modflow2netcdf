#!python
# coding=utf-8

import os
import sys
import logging
import argparse

from modflow2netcdf.mfnetcdf import ModflowToNetCDF

from modflow2netcdf import logger
logger.level = logging.INFO
logger.addHandler(logging.StreamHandler(sys.stdout))


def main(name_file, config_file, action, output=None, verbose=None, verify=False):

    if verbose is True:
        logger.level = logging.DEBUG
    else:
        verbose = False
        logger.level = logging.INFO

    # Try to load files for immediate warnings back to the user
    try:
        with open(name_file) as f:
            f.read()
    except IOError:
        logger.info("Error opening namefile: {!s}".format(name_file))
        return

    try:
        with open(config_file) as f:
            f.read()
    except IOError:
        logger.info("Error opening configuration file: {!s}".format(config_file))
        return

    if action not in ['plot', 'netcdf']:
        logger.error("The 'action' paramter must be 'plot' or 'netcdf'")
        return

    mo = ModflowToNetCDF(os.path.basename(name_file), config_file=config_file, verbose=verbose, model_ws=os.path.dirname(name_file))
    if action == "plot":
        mo.to_plot()
    else:
        action == "netcdf"
        mo.save_netcdf(output, verify)

    return 0


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', action='store', choices=('plot', 'netcdf',))

    parser.add_argument('-n', '--name_file',
                        help="Modflow Namefile (.nam) to load.",
                        required=True)
    parser.add_argument('-c', '--config_file',
                        help="Modflow2netcdf configiration file to load.",
                        required=True)
    parser.add_argument('-o', '--output_file',
                        help="Output file (only used with the 'netcdf' action), defaults to 'output.nc'",
                        default='output.nc',
                        nargs='?')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help="Set output to be verbose, defaults to False")
    parser.add_argument('-vf', '--verify',
                        action='store_true',
                        default=False,
                        help="Set output to verify NetCDF file, defaults to False")

    args = parser.parse_args()
    print args
    name_file_path   = os.path.realpath(args.name_file)
    config_file_path = os.path.realpath(args.config_file)
    output_file_path = os.path.realpath(args.output_file)

    return main(name_file_path, config_file_path, args.action, output=output_file_path, verbose=args.verbose, verify=args.verify)


if __name__ == "__main__":
    run()
