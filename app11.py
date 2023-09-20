# Functions to generate APP-11 lines used in REPMUS 2023 APP-11 report generation.

# Library imports
import math

# Local imports
import constants
import utils


def filename(report_type : str,
             originator : str,
             area : str,
             task : str,
             msg_serial : int) -> str:

    nmw_tq = ""

    if (report_type == "start"):
        nmw_tq = constants.NMW_TQ_START
    if (report_type == "stop"):
        nmw_tq = constants.NMW_TQ_STOP
    if (report_type == "complete"):
        nmw_tq = constants.NMW_TQ_COMPLETE

    return "TE X446.02.02.{}_{}-{}_{}_{}.txt" \
            .format(originator, area, task, nmw_tq, utils.formatMsgSerialNumber(msg_serial))


def header(originator : str) -> str:
    time = utils.currentDatetime()
    return ("R {}\n"
            "FM TE X446.02.02.{}\n"
            "TO CTU X446.02.02\n"
            "INFO EXCON\n"
            "\n"
            ).format(time, originator)


def begin():
    return ("BT\n"
            "\n"
            "NATO UNCLASSIFIED\n"
            "\n")


def end():
    return "BT\n"


def shared(report_type : str,
           originator : str,
           msg_serial : int,
           area : str,
           task : str,
           ref : str,
           start : str,
           stop : str) -> str:

    nmw_tq = ""
    nmw_tq_first = ""
    nmw_tq_second = ""
    if (report_type == "start"):
        nmw_tq = constants.NMW_TQ_START
        nmw_tq_first = constants.NMW_TQ_START
        nmw_tq_second = constants.NMW_TQ_ETC
    elif (report_type == "stop"):
        nmw_tq = constants.NMW_TQ_STOP
        nmw_tq_first = constants.NMW_TQ_START
        nmw_tq_second = constants.NMW_TQ_STOP
    else:
        nmw_tq = constants.NMW_TQ_COMPLETE
        nmw_tq_first = constants.NMW_TQ_START
        nmw_tq_second = constants.NMW_TQ_COMPLETE

    body = ""
    body += "EXER/REPMUS 2023//\n"
    body += "MSGID/OPREP NWM/APP-11(E)/1/446.02.02.{}/{}/SEP/-/-/NATO/UNCLASSIFIED//\n".format(originator, utils.formatMsgSerialNumber(msg_serial))
    body += "REF/A/TYPE:MSG/OPDIR/CTU446.02.02/SEP2023//\n"
    body += "REF/B/TYPE:MSG/OPTASK NWM/CTU446.02.02/{}//\n".format(ref)
    body += "GEODATUM/WGE//\n"
    body += "NMWREPQ/TASKREP/{}//\n".format(nmw_tq)
    body += "HEADING/MCM//\n"
    body += "MTASKREP/{}-{}/446.02.02.{}/AREA:{}/{}/{}/{}/{}//\n".format(area, task, originator, area, nmw_tq_first, start, nmw_tq_second, stop)
    body += "\n"

    return body


def mcmpedat(area : str,
             task : str,
             characteristic_width : int,
             classification_probability : float,
             probability_undetected_due_to_burial : float,
             probability_undetected_due_to_seabed : float,
             number_of_tracks : int,
             track_spacing : float) -> str:

    # NOTE:
    # this function makes assumptions:
    #  - only 1 run per track
    #  - completion is always 100%
    # obviously this is not correct all the time, but for us it is and this simplifies things

    track_info = ""
    for i in range(0, number_of_tracks):
         dist_to_center_line = ((number_of_tracks - 1) / 2 - i) * track_spacing
         qualifier = "PS" if (dist_to_center_line >= 0) else "MS"
         dist_to_center_line = abs(dist_to_center_line)
         track_info += "{}{}M/1/1".format(qualifier, int(round(dist_to_center_line)))
         if (i < number_of_tracks - 1):
             track_info += "/"

    return "MCMPEDAT/{}-{}/100/-/{}M/-/{}/-/1/-/-/{}/{}/{}//\n\n" \
           .format(area,
                   task,
                   characteristic_width,
                   classification_probability,
                   probability_undetected_due_to_burial,
                   probability_undetected_due_to_seabed,
                   track_info)


def trckhist(file : str,
             delta_t : float,
             equipment : str) -> str:

    body = ""
    data = utils.parseCsv(file)
    data = utils.throttle_data(data, delta_t)
    for line in data:
        body += ("TRCKHIST/{}/{}/{}/{}/{}/{}//\n" \
                .format(equipment,
                        utils.extractAndFormatDTG(line),
                        utils.extractAndFormatFix(line),
                        utils.extractAndFormatSensorAltitude(line),
                        utils.extractAndFormatSpeed(line),
                        utils.extractAndFormatHeading(line)))

    return body + "\n"


def mines(file : str,
          sonar_type : str) -> str:

    body = ""
    data = utils.parseCsv(file)

    for line in data:
        detection_type = line[5].lower()
        if detection_type == constants.MILEC:
            body += milecrep(line, sonar_type)
        if detection_type == constants.MILCO:
            body += milcorep(line, sonar_type)
        if detection_type == constants.MDET:
            body += mdetrep(line, sonar_type)

    return body + "\n"


def milecrep(line, sonar_type) -> str:
    return "MILECREP/{}/WGE/{}/{}/{}/{}/{}//\n" \
           .format(utils.getMineDTG(line),
                   utils.getMineFix(line),
                   utils.getMineCircularErrorProbability(line),
                   sonar_type.upper(),
                   "UNCERTAIN",
                   utils.getMineImageName(line))


def milcorep(line, sonar_type) -> str:
    return "MILCOREP/{}/{}/WGE/{}/{}/{}/{}/-/{}/{}//\n"     \
           .format(utils.getMineContactReferenceNumber(line),
                   utils.getMineDTG(line),
                   utils.getMineFix(line),
                   utils.getMineCircularErrorProbability(line),
                   sonar_type.upper(),
                   utils.getMineSonarConfidenceLevel(line),
                   "LOOKS LIKE A MINE",
                   utils.getMineImageName(line))


def mdetrep(line, sonar_type) -> str:
    return "MDETREP/SIGHTED/VISUAL/{}/-/DIVER/WGE/{}/{}/-/SEE IMAGE {}/{}//\n" \
           .format(utils.getMineDTG(line),
                   utils.getMineFix(line),
                   utils.getMineCircularErrorProbability(line),
                   utils.getMineImageName(line),
                   utils.getMineReferenceNumber(line))


def narr(time_in_water: float,
         pma_detection_and_processing_time: float,
         pma_classification_and_processing_time: float,
         pma_recovery_and_processing_time: float) -> str:

    return "NARR/{}H/{}H/{}H/{}H//\n\n" \
           .format(time_in_water,
                   pma_detection_and_processing_time,
                   pma_classification_and_processing_time,
                   pma_recovery_and_processing_time)

