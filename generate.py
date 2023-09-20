#!/bin/python3

# Note: this script was created during REPMUS 2023 with only a partial understanding of the APP-11 standard.
# It is written specifically for use with EvoLogics GmbH data.
# It is not guaranteed to be correct and should be used with caution.
# It is not polished at all, and probably full of bad coding practices and bugs.
# It was mostly written when I was very tired and/or very stressed and/or very hungry.


# Library imports
import argparse
import configparser
import csv
import datetime

# Local imports
import app11
import utils


# Name of the general data file
PARAMETERS_FILE_NAME = "parameters.ini"
ESTIMATED_STATE_FILE_NAME = "EstimatedState.csv"
MINE_DETECTION_FILE_NAME = "Mines.csv"

# Dictionary holding the data
DATA = {
        'orig': "",
        'area': "",
        'task': "",
        'vehicle': "",
        'sonar': "",
        'ref': "",
        'serial': 0,
        'start': "",
        'etc': "",
        'stop': "",
        'complete': "",
        'mission grid step': 0,
        'mission number of rows': 0,
        'mission sonar range': 0,
        'classification probability': 0,
        'probability undetected burial': 0,
        'probability undetected seabed': 0,
        'vehicle time in water': 0,
        'pma detection and processing': 0,
        'pma classification and processing': 0,
        'pma recovery and processing': 0,
        }


def parse_general(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    DATA['orig']    = config['GENERAL']['Originator ID']
    DATA['area']    = config['GENERAL']['Area']
    DATA['task']    = config['GENERAL']['Task Order Number']
    DATA['vehicle'] = config['GENERAL']['Vehicle Name']
    DATA['sonar']   = config['GENERAL']['Sonar Name']
    DATA['ref']     = config['GENERAL']['UTC Reference Datetime']
    DATA['serial']  = int(config['GENERAL']['Initial Message Serial Number'])
    DATA['start']   = config['GENERAL']['UTC Start Datetime']


def parse_start(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    DATA['etc'] = config['START']['UTC Estimated Completion Datetime']


def parse_stop(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    DATA['stop'] = config['STOP']['UTC Stop Datetime']


def parse_complete(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    DATA['complete']                           = config['COMPLETE']['UTC Complete Datetime']
    DATA['mission grid step']                  = config['COMPLETE']['Mission Grid Step'] 
    DATA['mission number of rows']             = config['COMPLETE']['Mission Number Of Rows']
    DATA['mission sonar range']                = config['COMPLETE']['Mission Sonar Range']
    DATA['classification probability']         = config['COMPLETE']['Probability Of Classifying Hit As Mine']
    DATA['probability undetected burial']      = config['COMPLETE']['Probability Of Undetected Mines Due To Total Burial']
    DATA['probability undetected seabed']      = config['COMPLETE']['Probability Of Undetected Mines Due To Seabed Profile']
    DATA['vehicle time in water']              = config['COMPLETE']['Vehicle Time In Water']
    DATA['pma detection and processing']       = config['COMPLETE']['PMA Detection & Processing']
    DATA['pma classification and processing']  = config['COMPLETE']['PMA Classification & Processing']
    DATA['pma recovery and processing']        = config['COMPLETE']['PMA Recovery & Processing']


def create_filename(report_type):
    return app11.filename(report_type, DATA['orig'], DATA['area'], DATA['task'], DATA['serial'])


def create_start_report():
    return app11.header(DATA['orig']) + \
           app11.begin() + \
           app11.shared("start", DATA['orig'], DATA['serial'], DATA['area'], DATA['task'], DATA['ref'], DATA['start'], DATA['etc']) + \
           app11.end()


def create_stop_report():
    return app11.header(DATA['orig']) + \
           app11.begin() + \
           app11.shared("stop", DATA['orig'], DATA['serial'], DATA['area'], DATA['task'], DATA['ref'], DATA['start'], DATA['stop']) + \
           app11.end()


def create_complete_report(estimated_state_filename : str,
                           mine_detection_filename : str):
    return app11.header(DATA['orig']) + \
           app11.begin() + \
           app11.shared("complete", DATA['orig'], DATA['serial'], DATA['area'], DATA['task'], DATA['ref'], DATA['start'], DATA['complete']) + \
           app11.mcmpedat(DATA['area'],
                          DATA['task'],
                          int(DATA['mission sonar range']),
                          float(DATA['classification probability']),
                          float(DATA['probability undetected burial']),
                          float(DATA['probability undetected seabed']),
                          int(DATA['mission number of rows']),
                          float(DATA['mission grid step'])) + \
           app11.trckhist(estimated_state_filename,
                          15.0,
                          DATA['vehicle']) + \
           app11.mines(mine_detection_filename,
                       DATA['sonar']) + \
           app11.narr(DATA['vehicle time in water'],
                      DATA['pma detection and processing'],
                      DATA['pma classification and processing'],
                      DATA['pma recovery and processing']) + \
           app11.end()


def create_file(filename, buffer):
    file = open(filename, 'w')
    file.write(buffer)
    file.close()


def main():
    parser = argparse.ArgumentParser(description='Generate APP-11 reports for REPMUS 2023')
    parser.add_argument('-t', '--type',
                        type=str,
                        required=True,
                        choices=['start', 'stop', 'complete'],
                        help='type of report to generate')
    parser.add_argument('-d', '--directory',
                        type=str,
                        required=True,
                        help='directory which contains all the data files and in which to generate the reports')
    args = parser.parse_args()

    config_file = args.directory + PARAMETERS_FILE_NAME
    parse_general(config_file)
    if args.type == "start":
        parse_start(config_file)
    if args.type == "stop":
        parse_stop(config_file)
        DATA['serial'] += 1
    if args.type == "complete":
        parse_complete(config_file)
        DATA['serial'] += 2

    print("\nSummary:")
    print("    Report type:            {}".format(args.type.upper()))
    print("    Message serial number:  {}".format(utils.formatMsgSerialNumber(DATA['serial'])))
    print("    Location:               {}".format(args.directory))
    print("\n")
    answer = input("Is this correct? [y/n] ")

    if answer.lower() not in ["y", "yes"]:
        print("Aborting.")
        exit(0)

    print("\nGenerating...")

    buffer = ""
    if args.type == "start":
        buffer = create_start_report()
    if args.type == "stop":
        buffer = create_stop_report()
    if args.type == "complete":
        buffer = create_complete_report(args.directory + ESTIMATED_STATE_FILE_NAME,
                                        args.directory + MINE_DETECTION_FILE_NAME)

    filename = args.directory + create_filename(args.type)
    create_file(filename, buffer)

    print("\nReport generated: {}".format(filename))


if __name__ == '__main__':
    main()
