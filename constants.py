# Constants used in REPMUS 2023 APP-11 report generation.

# Local imports
from datatypes import ReportType


# Filenames
PARAMETERS_FILE_NAME       = "parameters.ini"
ESTIMATED_STATE_FILE_NAME  = "EstimatedState.csv"
MINE_DETECTION_FILE_NAME   = "Mines.csv"

# NMW time qualifiers (see table 1220/22)
NMW_TQ_CANCEL        = "CXL"
NMW_TQ_COMPLETE      = "CPT"
NMW_TQ_ETC           = "ETC"
NMW_TQ_INTERRUPT     = "INTRPT"
NMW_TQ_RESUME        = "RESMD"
NMW_TQ_START         = "START"
NMW_TQ_STOP          = "STOP"

# MSG ID QUALIFIER (see table 1130/3)
MSG_ID_AMPLIFYING    = "AMP"
MSG_ID_BLOCK         = "BLK"
MSG_ID_CHANGE        = "CHG"
MSG_ID_DEVIATION     = "DEV"
MSG_ID_FINAL         = "FIN"
MSG_ID_FOLLOW_UP     = "FUP"
MSG_ID_INITIAL       = "INI"
MSG_ID_NEW           = "NEW"
MSG_ID_PERMANENT     = "PER"
MSG_ID_REQUEST       = "REQ"
MSG_ID_UPDATE        = "UPD"

# MINE STATUS IDENTIFIER (see table 1609/1)
MSI_MINE_LEFT_IN_PLACE   = "LIPLA"
MSI_DRIFTING_MINE        = "DRIFT"
MSI_FLOATING_MINE        = "FLOAT"
MSI_FOULED_MINE          = "FOULED"
MSI_NOT_DEALT_WITH_MINE  = "NDEALT"
MSI_SUNK_MINE            = "SUNK"
MSI_SWEPT_MINE           = "SWEPT"
MSI_DISPOSED_MINE        = "DISP"
MSI_COUNTERMINED_MINE    = "CMINED"
MSI_NEUTRALIZED_MINE     = "NEUTR"
MSI_MARKED_MINE          = "MARK"
MSI_REMOVED_MINE         = "RMVD"
MSI_RECOVERED_MINE       = "RECVD"
MSI_RENDERED_SAFE_MINE   = "RSAFE"
MSI_EXPLODED_MINE        = "EXPLD"
MSI_ACTIVATED_MINE       = "ACTIV"

# MINE CASE (see table 1141/1)
MC_NO_INFORMATION_ON_THE_MINE_BODY  = "0"
MC_MOORED_MINE                      = "1"
MC_SHALLOW_MOORED_MINE              = "2"
MC_DEEP_MOORED_MINE                 = "3"
MC_GROUND_MINE                      = "4"
MC_STEALTH_MINE                     = "5"
MC_SELF_PROPELLED_MINE              = "6"
MC_RISING_MINE                      = "7"
MC_UNEXPLODED_EXPLOSIVE_ORDNANCE    = "8"
MC_OBSTRUCTORS                      = "9"

# Mine status ID map
MINE_STATUS_ID_MAP = {
                      "LEFT-IN-PLACE"   : "LIPLA",
                      "DRIFTING"        : "DRIFT",
                      "FLOATING"        : "FLOAT",
                      "FOULED"          : "FOULED",
                      "NOT-DEALT-WITH"  : "NDEALT",
                      "SUNK"            : "SUNK",
                      "SWEPT"           : "SWEPT",
                      "DISPOSED"        : "DISP",
                      "COUNTERMINED"    : "CMINED",
                      "NEUTRALIZED"     : "NEUTR",
                      "MARKED"          : "MARK",
                      "REMOVED"         : "RMVD",
                      "RECOVERED"       : "RECVD",
                      "RENDERED-SAFE"   : "RSAFE",
                      "EXPLODED"        : "EXPLD",
                      "ACTIVATED"       : "ACTIV"
                     }

# Mine case map
MINE_CASE_MAP = {
                 "NO-INFO"              : "0",
                 "MOORED-MINE"          : "1",
                 "SHALLOW-MOORED-MINE"  : "2",
                 "DEEP-MOORED-MINE"     : "3",
                 "GROUND-MINE"          : "4",
                 "STEALTH-MINE"         : "5",
                 "SELF-PROPELLED-MINE"  : "6",
                 "RISING-MINE"          : "7",
                 "UNEXPLODED-EXPLOSIVE-ORDNANCE" : "8",
                 "OBSTRUCTORS"          : "9"
                }

# Map of report type to NMW time qualifier
NMW_TQ_MAP = {
              ReportType.Start     : NMW_TQ_START,
              ReportType.Interrupt : NMW_TQ_INTERRUPT,
              ReportType.Resume    : NMW_TQ_RESUME,
              ReportType.Cancel    : NMW_TQ_CANCEL,
              ReportType.Stop      : NMW_TQ_STOP,
              ReportType.Complete  : NMW_TQ_COMPLETE
             }

# Map of report type to NMW time qualifier
NMW_TQ_SECOND_MAP = {
                     ReportType.Start     : NMW_TQ_ETC,
                     ReportType.Interrupt : NMW_TQ_INTERRUPT,
                     ReportType.Resume    : NMW_TQ_RESUME,
                     ReportType.Cancel    : NMW_TQ_CANCEL,
                     ReportType.Stop      : NMW_TQ_STOP,
                     ReportType.Complete  : NMW_TQ_COMPLETE
                    }

# Map of report type to MSG ID QUALIFIER
MSG_ID_MAP = {
              ReportType.Start     : MSG_ID_INITIAL,
              ReportType.Interrupt : MSG_ID_UPDATE,
              ReportType.Resume    : MSG_ID_UPDATE,
              ReportType.Cancel    : MSG_ID_UPDATE,
              ReportType.Stop      : MSG_ID_UPDATE,
              ReportType.Complete  : MSG_ID_FINAL
             }

# Estimated State Throttle Delta T
ESTATE_THROTTLE_DELTA_T = 15.0

# Mine detection codes
MILECREP    = "MILECREP"
MILCOREP    = "MILCOREP"
NONMILCOREP = "NONMILCOREP"
MDETREP     = "MDETREP"
NOMBOINFO   = "NOMBOINFO"
MINEINFO    = "MINEINFO"
