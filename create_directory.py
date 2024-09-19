#!/bin/python3

# Library imports
import argparse
import datetime
import pathlib
import textwrap
import shutil
import sys

# Local imports
from src.constants import FOLDER_NAME_DATA, \
                          FOLDER_NAME_IMAGES, \
                          FOLDER_NAME_TASKING, \
                          FILENAME_MINES_CSV, \
                          FILENAME_PARAMETERS, \
                          FILENAME_TASKING_TXT
from src.filesystem_utils import createDirectoryIfNecessary, \
                                 createFileWithContent, \
                                 copyFileIfPossible
from src.logger import log, LogLevel, info, error, success
from src.exit_codes import ExitCode
from src.templates import parameterTemplate


def displayNextStepsMessage(data_path: pathlib.Path):
    info("Next steps:")
    info(f"  1. Fill in the .ini files in {data_path} with the appropriate information.")
    info("  2. Run the report generation script.")
    info("  3. Review the generated reports.")


def usage():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
        '''
        Generates the folder for the APP-11 report for a specified area and task,
        and the .ini files that should be filled in by the user to generate the report.
        '''
        ),
    formatter_class=argparse.RawDescriptionHelpFormatter)

    date_now = datetime.datetime.now().strftime('%Y%m%d')

    parser.add_argument('element',
                        type=str,
                        help='Task element (TE) for which to generate the report (e.g. TE4)')
    parser.add_argument('area',
                        type=str,
                        help='Area for which to generate the report (e.g. MWD)')
    parser.add_argument('task',
                        type=str,
                        help='Task number for which to generate the report (e.g. EH01)')
    parser.add_argument('directory',
                        type=str,
                        help='Top level directory in which to generate the folders')
    parser.add_argument('--date',
                        type=str,
                        default=f"{date_now}",
                        help='Date for which to generate the reports, in YYYYMMDD format')
    parser.add_argument('--originator',
                        type=str,
                        default="TE4",
                        help='Originator of the report (usually the TE number that is sending the report)')
    parser.add_argument('--destination',
                        type=str,
                        default="CTU SESIMBRA",
                        help='Destination of the report (usually CTU Sesimbra)')
    parser.add_argument('--mines-file',
                        type=str,
                        help='Path to the file containing the CSV mines data')
    parser.add_argument('--tasking-file',
                        type=str,
                        help='Path to the file containing the associated tasking (in plain text)')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Print debug information')
    parser.add_argument('-q',
                        '--quiet',
                        action='store_true',
                        help='Quiet mode (only print errors)')

    args = parser.parse_args()

    return args


def main():
    args = usage()

    if args.verbose:
        log.setLogLevel(LogLevel.Debug)
    elif args.quiet:
        log.setLogLevel(LogLevel.Quiet)

    top_directory = pathlib.Path(args.directory).resolve()
    if not top_directory.exists():
        error(f"Directory '{top_directory}' does not exist.")
        info("Create it, and try again.")
        sys.exit(ExitCode.Failure)

    data_path = top_directory / FOLDER_NAME_DATA
    data_data_directory = data_path / args.element / args.area / args.task / FOLDER_NAME_DATA
    data_tasking_directory = data_path / args.element / args.area / args.task / FOLDER_NAME_TASKING
    data_images_directory = data_path / args.element / args.area / args.task / FOLDER_NAME_IMAGES

    createDirectoryIfNecessary(data_data_directory)
    createDirectoryIfNecessary(data_images_directory)
    createDirectoryIfNecessary(data_tasking_directory)
    createFileWithContent(data_data_directory / FILENAME_PARAMETERS,
                          parameterTemplate(args.area,
                                            args.task,
                                            args.originator,
                                            args.destination,
                                            args.date))

    if args.mines_file:
        copyFileIfPossible(pathlib.Path(args.mines_file), data_data_directory / FILENAME_MINES_CSV)
    if args.tasking_file:
        copyFileIfPossible(pathlib.Path(args.tasking_file), data_tasking_directory / FILENAME_TASKING_TXT)

    success(f"Created folders and files for {args.area}-{args.task}.")
    displayNextStepsMessage(data_path)


if __name__ == "__main__":
    main()
