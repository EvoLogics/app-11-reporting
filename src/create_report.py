# Functions to generate APP-11 reports used in REPMUS 2023.

# Local imports
from src.app11 import filename, \
                      header, \
                      begin, \
                      end, \
                      milecrep, \
                      milcorep, \
                      nonmilcorep, \
                      mdetrep, \
                      nomboinfo, \
                      mineinfo, \
                      trckhist, \
                      msgid, \
                      ref, \
                      nmwrepq, \
                      mtaskrep, \
                      mcmpedat, \
                      mcmpedat_short, \
                      narr, \
                      gentext

from src.constants import ESTATE_THROTTLE_DELTA_T, \
                          NMW_TQ_MAP, \
                          MILECREP, \
                          MILCOREP, \
                          NONMILCOREP, \
                          MDETREP, \
                          NOMBOINFO, \
                          MINEINFO, \
                          DETECTION_EQUIPMENT_MAP
from src.datatypes import ReportType
from src.utils import getMineDTG, \
                      getMineFix, \
                      getMineCircularErrorProbability, \
                      getMineContactReferenceNumber, \
                      getMineSonarConfidenceLevel, \
                      getMineImageName, \
                      getMineNOMBOIdentification, \
                      getMineReferenceNumber, \
                      getMineStatusIdentifier, \
                      getMineDetectionEquipment, \
                      getMineCase, \
                      getMineIdentity, \
                      getMineDepth, \
                      throttleData, \
                      extractAndFormatDTG, \
                      extractAndFormatFix, \
                      extractAndFormatSensorAltitude, \
                      extractAndFormatSpeed, \
                      extractAndFormatHeading, \
                      timeToZulu




def create_filename(report_type: ReportType,
                    data: dict) -> str:

    return filename(report_type,
                    data['originator'],
                    data['area'],
                    data['task'],
                    data['message serial number'])


def create_mines(data: dict) -> str:

    mine_data = data['mine data']

    if len(mine_data) == 0:
        return ""

    body = ""

    for line in mine_data:
        utc                         = getMineDTG(line)
        fix                         = getMineFix(line)
        circular_error_probability  = getMineCircularErrorProbability(line)
        contact_reference_number    = getMineContactReferenceNumber(line)
        sonar_confidence_level      = getMineSonarConfidenceLevel(line)
        image_name                  = getMineImageName(line)
        detection_vehicle           = getMineDetectionEquipment(line)

        detection_equipment         = DETECTION_EQUIPMENT_MAP[detection_vehicle].upper()

        detection_type = line[0].upper()
        if detection_type == MILECREP:
            body += milecrep(utc,
                             fix,
                             circular_error_probability,
                             detection_equipment,
                             "UNCERTAIN",
                             image_name)
        if detection_type == MILCOREP:
            body += milcorep(contact_reference_number,
                             utc,
                             fix,
                             circular_error_probability,
                             detection_equipment,
                             sonar_confidence_level,
                             "LOOKS LIKE A MINE",
                             image_name)
        if detection_type == NONMILCOREP:
            body += nonmilcorep(contact_reference_number,
                                utc,
                                fix,
                                circular_error_probability,
                                detection_equipment,
                                sonar_confidence_level,
                                "DOESN'T LOOK LIKE A MINE",
                                image_name)
        if detection_type == MDETREP:
            body += mdetrep("VISUAL",
                            utc,
                            "-",
                            "DIVER",
                            fix,
                            circular_error_probability,
                            "SEE IMAGE " + image_name)
        if detection_type == NOMBOINFO:
            nombo_id = getMineNOMBOIdentification(line)
            body += nomboinfo(contact_reference_number,
                              utc,
                              fix,
                              circular_error_probability,
                              nombo_id,
                              "SONAR",
                              image_name)
        if detection_type == MINEINFO:
            mine_reference_number = getMineReferenceNumber(line)
            mine_status_identifier = getMineStatusIdentifier(line)
            mine_case = getMineCase(line)
            mine_identity = getMineIdentity(line)
            mine_depth = getMineDepth(line)
            body += mineinfo(mine_reference_number,
                             utc,
                             fix,
                             circular_error_probability,
                             mine_status_identifier,
                             mine_case,
                             mine_identity,
                             "SONAR",
                             mine_depth,
                             image_name)

    body += "\n"

    return body


def create_trckhist(data):

    estimated_state_data = data['estimated state data']

    if len(estimated_state_data) == 0:
        return ""

    estimated_state_data = throttleData(estimated_state_data, ESTATE_THROTTLE_DELTA_T)
    body = ""

    for line in estimated_state_data:
        body += trckhist(data['vehicle name'],
                         extractAndFormatDTG(line),
                         extractAndFormatFix(line),
                         extractAndFormatSensorAltitude(line),
                         extractAndFormatSpeed(line),
                         extractAndFormatHeading(line))

    body += "\n"

    return body


def create_body(report_type: ReportType,
                data : dict,
                add_full_mcmpedat : bool,
                add_trckhist : bool,
                add_narr : bool) -> str:

    second_utc = ""

    if report_type == ReportType.Start:
        second_utc = timeToZulu(data['etc utc'])
        progress = 0
        comments = data['start comments']
    if report_type == ReportType.Stop:
        second_utc = timeToZulu(data['stop utc'])
        progress = data['stop progress']
        comments = data['stop comments']
    if report_type == ReportType.Complete:
        second_utc = timeToZulu(data['complete utc'])
        progress = data['stop progress']
        comments = data['complete comments']

    body = ""
    body += "EXER/REPMUS 2024//\n"
    body += msgid(data['originator'], data['message serial number'], report_type)
    body += "REF/A/TYPE:DOC/EXPLAN/COMMANDO NAVAL/09JUL2024//\n"
    body += "REF/B/TYPE:DOC/SRL PLAN ANNEX E/EXCON MCM/09JUL2024//\n"
    body += ref("C", "OPDIR", data['originator'], data['reference utc'])
    body += "GEODATUM/WGE//\n"
    body += nmwrepq(NMW_TQ_MAP[report_type])
    body += "HEADING/MCM//\n"
    body += mtaskrep(data['area'],
                           data['task'],
                           data['originator'],
                           report_type,
                           timeToZulu(data['start utc']),
                           second_utc)

    if report_type == ReportType.Complete:
        if add_full_mcmpedat:
            body += mcmpedat(data['area'],
                                   data['task'],
                                   int(data['mission sonar range']),
                                   float(data['classification probability']),
                                   float(data['probability undetected burial']),
                                   float(data['probability undetected seabed']),
                                   int(data['mission number of rows']),
                                   float(data['mission grid step']))
        if add_trckhist:
            body += create_trckhist(data)
        body += create_mines(data)
        if add_narr:
            body += narr(data['vehicle time in water'],
                               data['pma detection and processing'],
                               data['pma classification and processing'],
                               data['pma recovery and processing'])
    else:
        body += mcmpedat_short(data['area'], data['task'], progress)

    body += gentext(comments.upper())
    body += "\n"

    return body


def create_file(filename: str,
                content: str) -> None:

    file = open(filename, 'w')
    file.write(content)
    file.close()


def create_report(report_type: ReportType,
                  data: dict,
                  directory: str,
                  add_full_mcmpedat : bool,
                  add_trckhist : bool,
                  add_narr : bool) -> tuple [str, str]:

    content = ""
    content += header(data['originator'], data['destination'])
    content += begin()
    content += create_body(report_type, data, add_full_mcmpedat, add_trckhist, add_narr)
    content += end()

    filename = create_filename(report_type, data)
    filepath = directory / filename
    create_file(filepath, content)

    return filepath, filename
