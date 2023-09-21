# Types used in REPMUS 2023 APP-11 report generation.

# Library imports
import enum


# Report type enum
class ReportType(enum.Enum):
    Start       = "start"
    Stop        = "stop"
    Interrupt   = "interrupt"
    Resume      = "resume"
    Cancel      = "cancel"
    Complete    = "complete"

    def __str__(self):
        return self.name.upper()

