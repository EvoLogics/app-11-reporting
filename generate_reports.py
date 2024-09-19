#!/bin/python3

# Library imports
import argparse
import configparser
import csv
import pathlib
import textwrap
import sys

# Local imports
from src.constants import FILENAME_ESTIMATED_STATE_CSV, \
                          FILENAME_MINES_CSV, \
                          FILENAME_PARAMETERS, \
                          FILENAME_NUMBER_CACHE_FILE, \
                          FOLDER_NAME_DATA, \
                          FOLDER_NAME_REPORTS, \
                          PARAMETER_SECTION_MAP
from src.create_report import create_report
from src.datatypes import ReportType
from src.filesystem_utils import readDictFromFileIfPossible, \
                                 createFileWithContent, \
                                 createDirectoryIfNecessary
from src.exit_codes import ExitCode
from src.logger import Logger, LogLevel, log, success, info, warning, error, debug


def usage():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
        '''
        Generates the APP-11 reports for a specified area and task.
        '''
        ),
    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('element',
                        type=str,
                        help='Tasking element (TE) for which to generate the report (e.g. TE4)')
    parser.add_argument('area',
                        type=str,
                        help='Area for which to generate the report (e.g. MWD)')
    parser.add_argument('task',
                        type=str,
                        help='Task number for which to generate the report (e.g. EH01)')
    parser.add_argument('directory',
                        type=str,
                        help='Top level directory in which to generate the folders')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Print debug information')
    parser.add_argument('-q',
                        '--quiet',
                        action='store_true',
                        help='Quiet mode (only print errors)')
    parser.add_argument('--only',
                        type=ReportType,
                        choices=list(ReportType),
                        help='If specified, only generate report for this type')
    parser.add_argument('--start-number',
                        type=int,
                        help='If specified, use this number as start number instead of the next available from cache')

    args = parser.parse_args()

    return args


def parseCsv(filepath: str) -> list:

    data = []

    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)

    # Remove the first row, which contains the column names
    if len(data) > 0:
        data.pop(0)

    return data


def get_cache_dict(cache_file: pathlib.Path) -> dict:
    return readDictFromFileIfPossible(cache_file)


def hasNumber(cache_dict: dict, area: str, task: str):
    number_list = []
    found = False
    for key in cache_dict:
        if key == area:
            field = cache_dict[key]
            for subkey in field:
                if subkey == task:
                    found = True
                    number_list = field[subkey]
    return found, number_list


def maxNumber(cache_dict: dict) -> int:
    max_number = 0
    for key in cache_dict:
        field = cache_dict[key]
        for subkey in field:
            number = max(field[subkey])
            if number > max_number:
                max_number = number
    return max_number


def getReportStartNumber(cache_dict: dict, area: str, task: str) -> int:
    has_number, report_numbers = hasNumber(cache_dict, area, task)
    if not has_number:
        report_start_number = maxNumber(cache_dict) + 1
    else:
        report_start_number = report_numbers[0]
    debug(f"Report start number: {report_start_number}")
    return has_number, report_start_number


def getParams(data_directory: pathlib.Path) -> dict:
    params = configparser.ConfigParser()
    params.read(data_directory / FILENAME_PARAMETERS)
    return params


def getReportTypes(params: dict) -> list:
    report_types = []
    for key in PARAMETER_SECTION_MAP.keys():
        if key in params:
            report_types.append(PARAMETER_SECTION_MAP[key])
    return report_types


def getData(params: dict) -> dict:
    data = {}
    data['area']                = params['GENERAL']['Area']
    data['task']                = params['GENERAL']['Task Order Number']
    data['originator']          = params['GENERAL']['Originator']
    data['destination']         = params['GENERAL']['Destination']
    data['reference utc']       = params['GENERAL']['Reference UTC Datetime']

    data['start utc']           = params['START']['Start UTC Datetime']
    data['etc utc']             = params['START']['Estimated Completion UTC Datetime']
    data['start comments']      = params['START']['Comments']

    data['stop utc']            = params['STOP']['Stop UTC Datetime']
    data['stop progress']       = params['STOP']['Progress']
    data['stop comments']       = params['STOP']['Comments']

    data['complete utc']        = params['COMPLETE']['Complete UTC Datetime']
    data['complete comments']   = params['COMPLETE']['Comments']

    return data


def getAdditionalData(data: dict,
                      report_type: ReportType,
                      data_directory: pathlib.Path,
                      add_extended_mcmpedat: bool) -> dict:
    if report_type == ReportType.Complete:
        if add_extended_mcmpedat:
            debug("Parsing estimated state data...")
            data['estimated state data'] = parseCsv(data_directory / FILENAME_ESTIMATED_STATE_CSV)
        debug("Parsing mine detection data...")
        data['mine data'] = parseCsv(data_directory / FILENAME_MINES_CSV)
    return data


def main():
    args = usage()

    if args.verbose:
        log.setLogLevel(LogLevel.Debug)
    elif args.quiet:
        log.setLogLevel(LogLevel.Quiet)

    info("Generating APP-11 reports...")

    top_directory = pathlib.Path(args.directory).resolve()
    data_directory = top_directory  / FOLDER_NAME_DATA / args.element / args.area / args.task / FOLDER_NAME_DATA
    reports_path = top_directory / FOLDER_NAME_REPORTS
    reports_directory = reports_path / args.element / args.area / args.task
    param_data_file = data_directory / FILENAME_PARAMETERS
    mines_data_file = data_directory / FILENAME_MINES_CSV
    number_cache_file = top_directory / FILENAME_NUMBER_CACHE_FILE

    if not top_directory.exists():
        error(f"Directory '{top_directory}' does not exist.")
        info("Create it, and try again.")
        sys.exit(ExitCode.Failure)

    if not (param_data_file).exists():
        error(f"Directory '{data_directory}' does not contain a file '{FILENAME_PARAMETERS}'.")
        info("Create it, and try again.")
        sys.exit(ExitCode.Failure)

    if not (mines_data_file).exists():
        error(f"Directory '{data_directory}' does not contain a file '{FILENAME_MINES_CSV}'.")
        info("Create it, and try again.")
        sys.exit(ExitCode.Failure)

    if not number_cache_file.exists():
        debug(f"No number cache file found - creating...")
        createFileWithContent(top_directory / FILENAME_NUMBER_CACHE_FILE, "")

    if not reports_directory.exists():
        createDirectoryIfNecessary(reports_directory)
        debug(f"No reports directory found - creating...")

    params = getParams(data_directory)
    report_types = getReportTypes(params)
    data = getData(params)
    cache_dict = get_cache_dict(number_cache_file)
    has_number, report_start_number = getReportStartNumber(cache_dict, args.area, args.task)

    if args.start_number is not None:
        report_start_number = args.start_number
    else:
        report_start_number = report_start_number

    report_number = report_start_number
    report_numbers = []
    for report in report_types:
        info(f"Generating {report} report with number {report_number}...")
        data["message serial number"] = report_number
        data = getAdditionalData(data, report, data_directory, False)
        create_report(report,
                      data,
                      reports_directory,
                      False,
                      False,
                      False)
        report_numbers.append(report_number)
        report_number += 1

    if not has_number:
        new_pair = {args.task: report_numbers}
        if cache_dict.get(args.area) is None:
            cache_dict[args.area] = new_pair
        else:
            cache_dict[args.area][args.task] = report_numbers
        createFileWithContent(number_cache_file, str(cache_dict), True)

    success("APP-11 reports generated successfully.")


if __name__ == "__main__":
    main()
