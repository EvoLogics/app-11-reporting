# Functions to generate APP-11 lines used in REPMUS 2023 APP-11 reports.

# Library imports
import math
import textwrap

# Local imports
from constants import CTU_ORIGINATOR, \
                      NMW_TQ_MAP, \
                      NMW_TQ_SECOND_MAP
from datatypes import ReportType
from utils import currentDatetime


def filename(report_type : ReportType,
             originator : str,
             area : str,
             task : str,
             msg_serial : str) -> str:

    return "TE X{}.{}_{}-{}_{}_{}" \
            .format(CTU_ORIGINATOR,
                    originator,
                    area,
                    task,
                    NMW_TQ_MAP[report_type],
                    msg_serial)


def header(originator : str) -> str:

    return textwrap.dedent(
           """\
           R {}
           FM TE X{}.{}
           TO CTU X{}
           INFO EXCON

           """\
            .format(currentDatetime(),
                     CTU_ORIGINATOR,
                     originator,
                     CTU_ORIGINATOR))


def begin() -> str:

    return textwrap.dedent(
            """\
            BT

            NATO UNCLASSIFIED

            """
            )


def end() -> str:

    return "BT\n"


def msgid(originator : str,
          msg_serial_number : str) -> str:

    return "MSGID/OPREP NWM/APP-11(E)/1/{}.{}/{}/SEP/-/-/NATO/UNCLASSIFIED//\n" \
            .format(CTU_ORIGINATOR,
                    originator,
                    msg_serial_number)


def ref(serial_letter: str,
        information_product: str,
        datetime: str) -> str:

    return "REF/{}/TYPE:MSG/{}/CTU{}/{}//\n" \
            .format(serial_letter,
                    information_product,
                    CTU_ORIGINATOR,
                    datetime)


def nmwrepq(nmw_time_qualifier: str) -> str:
    return "NMWREPQ/TASKREP/{}//\n" \
            .format(nmw_time_qualifier)


def mtaskrep(area : str,
             task : str,
             originator : str,
             report_type : str,
             start_utc : str,
             second_utc : str) -> str:

    return "MTASKREP/{}-{}/{}.{}/AREA:{}/{}/{}/{}/{}//\n" \
            .format(area,
                    task,
                    CTU_ORIGINATOR,
                    originator,
                    area,
                    NMW_TQ_MAP[ReportType.Start],
                    start_utc,
                    NMW_TQ_SECOND_MAP[report_type],
                    second_utc)


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

    if (number_of_tracks == 0):
        return ""

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


def trckhist(equipment: str,
             utc: str,
             fix: str,
             sensor_altitude: str,
             speed: str,
             heading: str) -> str:

    return "TRCKHIST/{}/{}/{}/{}/{}/{}//\n" \
            .format(equipment,
                    utc,
                    fix,
                    sensor_altitude,
                    speed,
                    heading)


def milecrep(utc: str,
             fix: str,
             circular_error_probability: str,
             sonar_type: str,
             comment: str,
             image_name: str) -> str:

    return "MILECREP/{}/WGE/{}/{}/{}/{}/{}//\n" \
           .format(utc,
                   fix,
                   circular_error_probability,
                   sonar_type,
                   comment,
                   image_name)


def milcorep(contact_reference_number: str,
             utc: str,
             fix: str,
             circular_error_probability: str,
             sonar_type: str,
             sonar_confidence_level: str,
             comment: str,
             image_name: str) -> str:

    return "MILCOREP/{}/{}/WGE/{}/{}/{}/{}/-/{}/{}//\n" \
           .format(contact_reference_number,
                   utc,
                   fix,
                   circular_error_probability,
                   sonar_type,
                   sonar_confidence_level,
                   comment,
                   image_name)


def nonmilcorep(contact_reference_number: str,
                utc: str,
                fix: str,
                circular_error_probability: str,
                sonar_type: str,
                sonar_confidence_level) -> str:

    return "NONMILCOREP/{}/{}/WGE/{}/{}/{}/{}//\n" \
           .format(contact_reference_number,
                   utc,
                   fix,
                   circular_error_probability,
                   sonar_type,
                   sonar_confidence_level)


def mdetrep(detection_means: str,
            utc: str,
            unit_name: str,
            fix: str,
            circular_error_probability: str,
            image_name: str,
            mine_reference_number: str) -> str:

    return "MDETREP/SIGHTED/{}/{}/-/{}/WGE/{}/{}/-/SEE IMAGE {}/{}//\n" \
           .format(detection_means,
                   utc,
                   unit_name,
                   fix,
                   circular_error_probability,
                   image_name,
                   mine_reference_number)


def narr(time_in_water: float,
         pma_detection_and_processing_time: float,
         pma_classification_and_processing_time: float,
         pma_recovery_and_processing_time: float) -> str:

    return "NARR/{}H/{}H/{}H/{}H//\n" \
           .format(time_in_water,
                   pma_detection_and_processing_time,
                   pma_classification_and_processing_time,
                   pma_recovery_and_processing_time)

