# Constants used in REPMUS 2023 APP-11 report generation.

# Local imports
from datatypes import ReportType


# Filenames
PARAMETERS_FILE_NAME       = "parameters.ini"
ESTIMATED_STATE_FILE_NAME  = "EstimatedState.csv"
MINE_DETECTION_FILE_NAME   = "Mines.csv"

# CTU Originator
CTU_ORIGINATOR = "446.02.02"

# NMW time qualifiers (see table 1220/22)
NMW_TQ_CANCEL        = "CXL"
NMW_TQ_COMPLETE      = "CPT"
NMW_TQ_ETC           = "ETC"
NMW_TQ_INTERRUPT     = "INTRPT"
NMW_TQ_RESUME        = "RESMD"
NMW_TQ_START         = "START"
NMW_TQ_STOP          = "STOP"

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

# Estimated State Throttle Delta T
ESTATE_THROTTLE_DELTA_T = 15.0

# Mine detection codes
MILEC = "milec"
MILCO = "milco"
NONMILCO = "nonmilco"
MDET  = "mdet"
