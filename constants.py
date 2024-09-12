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
