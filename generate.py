#!/bin/python3

# Library imports
import argparse
import configparser
import csv
import datetime
import sys
import textwrap

# Local imports
import constants
from reports import create_report
from datatypes import ReportType
import utils


def parse_parameters(filename: str,
                     report_type: ReportType) -> int:

    config = configparser.ConfigParser()
    config.read(filename)

    data = {}

    data['originator']                             = config['GENERAL']['Originator ID']
    data['area']                                   = config['GENERAL']['Area']
    data['task']                                   = config['GENERAL']['Task Order Number']
    data['vehicle name']                           = config['GENERAL']['Vehicle Name']
    data['sonar type']                             = config['GENERAL']['Sonar Type']
    data['reference utc']                          = config['GENERAL']['UTC Datetime - Reference']

    data['start utc']                              = config['START']['UTC Datetime - Start']

    if report_type == ReportType.Start:
        data['message serial number']              = config['START']['Message Serial Number']
        data['etc utc']                            = config['START']['UTC Datetime - Estimated Completion']

    if report_type == ReportType.Interrupt:
        data['message serial number']              = config['INTERRUPT']['Message Serial Number']
        data['interrupt utc']                      = config['INTERRUPT']['UTC Datetime - Interrupt']

    if report_type == ReportType.Resume:
        data['message serial number']              = config['RESUME']['Message Serial Number']
        data['resume utc']                         = config['RESUME']['UTC Datetime - Resume']

    if report_type == ReportType.Cancel:
        data['message serial number']              = config['CANCEL']['Message Serial Number']
        data['cancel utc']                         = config['CANCEL']['UTC Datetime - Cancel']
    
    if report_type == ReportType.Stop:
        data['message serial number']              = config['STOP']['Message Serial Number']
        data['stop utc']                           = config['STOP']['UTC Datetime - Stop']

    if report_type == ReportType.Complete:
        data['message serial number']              = config['COMPLETE']['Message Serial Number']
        data['complete utc']                       = config['COMPLETE']['UTC Datetime - Complete']
        data['mission grid step']                  = config['COMPLETE']['Mission Grid Step'] 
        data['mission number of rows']             = config['COMPLETE']['Mission Number Of Rows']
        data['mission sonar range']                = config['COMPLETE']['Mission Sonar Range']
        data['classification probability']         = config['COMPLETE']['Probability Of Classifying Hit As Mine']
        data['probability undetected burial']      = config['COMPLETE']['Probability Of Undetected Mines Due To Total Burial']
        data['probability undetected seabed']      = config['COMPLETE']['Probability Of Undetected Mines Due To Seabed Profile']
        data['vehicle time in water']              = config['COMPLETE']['Vehicle Time In Water']
        data['pma detection and processing']       = config['COMPLETE']['PMA Detection & Processing']
        data['pma classification and processing']  = config['COMPLETE']['PMA Classification & Processing']
        data['pma recovery and processing']        = config['COMPLETE']['PMA Recovery & Processing']

    data['message serial number'] = data['message serial number'].zfill(3)
    data['report type']           = report_type

    return data


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


def main():

    parser = argparse.ArgumentParser(
    description=textwrap.dedent(
    '''
    Generate APP-11 reports for REPMUS 2023.

    Note: Proceed with caution!
    ---------------------------
    This script was created during REPMUS 2023 with only a partial understanding of the APP-11 standard.
    It was mostly written when I was very tired and/or very stressed and/or very hungry.
    It is written specifically for use with EvoLogics GmbH data.
    It is definitely not guaranteed to be correct and should be used with caution.
    It is not polished at all, and (very likely) contains many bad coding practices and bugs.
    '''
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t',
                        '--report-type',
                        type=ReportType,
                        required=True,
                        choices=list(ReportType),
                        help='type of report to generate')
    parser.add_argument('-d',
                        '--directory',
                        type=str,
                        required=True,
                        help='directory which contains all the data files and in which to generate the reports')

    args = parser.parse_args()

    data = parse_parameters(args.directory + constants.PARAMETERS_FILE_NAME, args.report_type)

    print("\n")
    print("Summary:")
    print("    Report type:            {}".format(str(args.report_type)))
    print("    Message serial number:  {}".format(data['message serial number']))
    print("    Location:               {}".format(args.directory))
    print("\n")
    answer = input("Is this correct? [y/n] ")
    if answer.lower() not in ["y", "yes"]:
        print("Aborting")
        sys.exit(0)

    print("\nGenerating...")

    # If it is a complete report, we need to parse the estimated state and mine detection data
    if args.report_type == ReportType.Complete:
        print("  --> Parsing estimated state data...")
        data['estimated state data']  = parseCsv(args.directory + constants.ESTIMATED_STATE_FILE_NAME)
        print("  --> Parsing mine detection data...")
        data['mine data']             = parseCsv(args.directory + constants.MINE_DETECTION_FILE_NAME)

    print("  --> Compiling APP-11 report...")
    filepath, filename = create_report(data, args.directory)

    print("\nReport generated at: {}".format(filepath))
    print("\nEmail title: {}".format(filename))
    print("")


if __name__ == '__main__':
    main()
