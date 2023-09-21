# Functions to generate APP-11 reports used in REPMUS 2023.

# Local imports
import app11
from constants import ESTATE_THROTTLE_DELTA_T, \
                      NMW_TQ_MAP, \
                      MILEC, \
                      MILCO, \
                      NONMILCO, \
                      MDET
from datatypes import ReportType
import utils


def create_filename(data: dict) -> str:

    return app11.filename(data['report type'],
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
        utc                         = utils.getMineDTG(line)
        fix                         = utils.getMineFix(line)
        circular_error_probability  = utils.getMineCircularErrorProbability(line)
        contact_reference_number    = utils.getMineContactReferenceNumber(line)
        reference_number            = utils.getMineReferenceNumber(line)
        sonar_confidence_level      = utils.getMineSonarConfidenceLevel(line)
        image_name                  = utils.getMineImageName(line)

        detection_type = line[5].lower()
        if detection_type == MILEC:
            body += app11.milecrep(utc,
                                   fix,
                                   circular_error_probability,
                                   data['sonar type'].upper(),
                                   "UNCERTAIN",
                                   image_name)
        if detection_type == MILCO:
            body += app11.milcorep(contact_reference_number,
                                   utc,
                                   fix,
                                   circular_error_probability,
                                   data['sonar type'].upper(),
                                   sonar_confidence_level,
                                   "LOOKS LIKE A MINE",
                                   image_name)
        if detection_type == NONMILCO:
            body += app11.nonmilcorep(contact_reference_number,
                                      utc,
                                      fix,
                                      circular_error_probability,
                                      data['sonar type'].upper(),
                                      sonar_confidence_level)
        if detection_type == MDET:
            body += app11.mdetrep("VISUAL",
                                  utc,
                                  "DIVER",
                                  fix,
                                  circular_error_probability,
                                  image_name,
                                  contact_reference_number)

    body += "\n"

    return body


def create_trckhist(data):

    estimated_state_data = data['estimated state data']

    if len(estimated_state_data) == 0:
        return ""

    estimated_state_data = utils.throttleData(estimated_state_data, ESTATE_THROTTLE_DELTA_T)
    body = ""

    for line in estimated_state_data:
        body += app11.trckhist(data['vehicle name'],
                               utils.extractAndFormatDTG(line),
                               utils.extractAndFormatFix(line),
                               utils.extractAndFormatSensorAltitude(line),
                               utils.extractAndFormatSpeed(line),
                               utils.extractAndFormatHeading(line))

    body += "\n"
    
    return body


def create_body(data: dict) -> str:

    report_type = data['report type']
    second_utc = ""

    if report_type == ReportType.Start:
        second_utc = data['etc utc']
    if report_type == ReportType.Interrupt:
        second_utc = data['interrupt utc']
    if report_type == ReportType.Resume:
        second_utc = data['resume utc']
    if report_type == ReportType.Cancel:
        second_utc = data['cancel utc']
    if report_type == ReportType.Stop:
        second_utc = data['stop utc']
    if report_type == ReportType.Complete:
        second_utc = data['complete utc']

    body = ""
    body += "EXER/REPMUS 2023//\n"
    body += app11.msgid(data['originator'], data['message serial number'])
    body += app11.ref("A", "OPDIR", "SEP2023")
    body += app11.ref("B", "OPTASK NWM", data['reference utc'])
    body += "GEODATUM/WGE//\n"
    body += app11.nmwrepq(NMW_TQ_MAP[report_type])
    body += "HEADING/MCM//\n"
    body += app11.mtaskrep(data['area'], data['task'], data['originator'], report_type, data['start utc'], second_utc)
    body += "\n"

    if report_type == ReportType.Complete:
        body += app11.mcmpedat(data['area'],
                               data['task'],
                               int(data['mission sonar range']),
                               float(data['classification probability']),
                               float(data['probability undetected burial']),
                               float(data['probability undetected seabed']),
                               int(data['mission number of rows']),
                               float(data['mission grid step']))
        body += create_trckhist(data)
        body += create_mines(data) 
        body += app11.narr(data['vehicle time in water'],
                           data['pma detection and processing'],
                           data['pma classification and processing'],
                           data['pma recovery and processing'])

    body += "\n"

    return body


def create_file(filename: str,
                content: str) -> None:

    file = open(filename, 'w')
    file.write(content)
    file.close()


def create_report(data: dict,
                  directory: str) -> tuple[str, str]:

    content = ""
    content += app11.header(data['originator'])
    content += app11.begin()
    content += create_body(data)
    content += app11.end()

    filename = create_filename(data)
    filepath = directory + filename + ".txt"
    create_file(filepath, content)

    return filepath, filename
