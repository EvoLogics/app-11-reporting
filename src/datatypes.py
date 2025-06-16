# Library imports
import enum


# Report type enum
class ReportType(enum.Enum):
    Start       = "start"
    Stop        = "stop"
    Complete    = "complete"

    def __str__(self):
        return self.name.upper()
