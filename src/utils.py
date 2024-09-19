# Utils used in REPMUS 2023 APP-11 report generation.

# Library imports
import datetime
import math
from pathlib import Path
import time

# Local imports
from src.constants import MINE_STATUS_ID_MAP, MINE_CASE_MAP


def timeToZulu(time_str):
    date = datetime.datetime.strptime(time_str, '%Y%m%d-%H%M')
    return date.strftime('%d%H%MZ%b%Y').upper()


def degreesToDDM(deg):
    if (deg >= 0.0):
        deg_int = math.floor(deg)
    else:
        deg_int = math.ceil(deg)
    deg_rem = deg - deg_int
    deciminutes = deg_rem * 60
    return 100 * deg_int + (deg_rem * 60)


def radiansToDDM(radians):
    return degreesToDDM(math.degrees(radians))


def currentDatetime():
    time = datetime.datetime.now(datetime.timezone.utc)
    return "{}".format(time.strftime('%d%H%MZ%b%Y')).upper()


def formatFix(lat, lon):
    round(lat, 4)
    round(lon, 4)

    lat_sep = 'N' if lat>0.0 else 'S'
    lat_val = format(abs(lat), '.4f').zfill(9)
    lon_sep = 'E' if lon>0.0 else 'W'
    lon_val = format(abs(lon), '.4f').zfill(10)

    return "{}{}-{}{}".format(lat_val, lat_sep, lon_val, lon_sep)


def throttleData(data, delta_t):
    throttled_data = []

    start_t = float(data[0][0])
    for i in range(0, len(data) - 1):
        row = data[i]
        row_t = float(row[0])
        if (row_t - start_t) > delta_t:
            throttled_data.append(row)
            start_t = row_t

    return throttled_data


def extractAndFormatDTG(line):
    time = datetime.datetime.fromtimestamp(float(line[0]))
    return "{}".format(time.strftime('%d%H%MZ%b%Y')).upper()


def extractAndFormatFix(line):
    return formatFix(radiansToDDM(float(line[3])),
                     radiansToDDM(float(line[4])))


def extractAndFormatSensorAltitude(line):
    return "ALT:{}".format(math.floor(float(line[22])))


def extractAndFormatSpeed(line):
    vx = float(line[15])
    vy = float(line[16])
    total_speed = math.floor(math.sqrt(vx ** 2 + vy ** 2) * 1.94384)
    return "{}".format(total_speed)


def extractAndFormatHeading(line):
    yaw = float(line[11]);
    return "{}".format(math.floor(math.degrees(yaw) % 360)).zfill(3)


def createTrckHist(data, equipment):
    f = open("trckhist.txt", "w")
    for line in data:
        f.write("TRCKHIST/{}/{}/{}/{}/{}/{}//\n".format(
                                equipment,
                                extractAndFormatDTG(line),
                                extractAndFormatFix(line),
                                extractAndFormatSensorAltitude(line),
                                extractAndFormatSpeed(line),
                                extractAndFormatHeading(line)))
    print("Wrote TRCKHIST to trckhist.txt")
    f.close();


def getMineContactReferenceNumber(line):
    return "{}".format(line[1]).upper()


def getMineReferenceNumber(line):
    return "{}".format(line[2]).upper()


def getMineNOMBOIdentification(line):
    return "{}".format(line[3]).upper()


def getMineDTG(line):
    return timeToZulu(line[4])


def getMineFix(line):
    return formatFix(degreesToDDM(float(line[6])),
                     degreesToDDM(float(line[5])))


def getMineCircularErrorProbability(line):
    return "{}".format(int(line[7]))


def getMineSonarConfidenceLevel(line):
    return "{}".format(int(math.floor((float(line[8]) * 100) / 25.0)) + 1)


def getMineDetectionEquipment(line):
    return line[9]


def getMineStatusIdentifier(line):
    return MINE_STATUS_ID_MAP[line[10]]


def getMineCase(line):
    return MINE_CASE_MAP[line[11]]


def getMineIdentity(line):
    return "{}".format(line[12]).upper()


def getMineDepth(line):
    return "{}".format(int(line[13]))


def getMineImageName(line):
    path = Path(line[14])
    return "{}".format(path.name).upper()
