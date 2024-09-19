# Library imports
import textwrap


def parameterTemplate(area: str,
                      task_order_number: str,
                      originator: str,
                      destination: str,
                      date: str) -> str:
    return textwrap.dedent(
    f"""
    # NOTES:
    # - Fill in the appropriate values for each field.
    # - Datetimes should be in UTC, in format YYYYMMDD-HHMM.
    # - Progress should be a percentage (0 to 100).
    # - Comments are optional and can be left empty.

    [GENERAL]
    Originator                                = {originator}
    Destination                               = {destination}
    Area                                      = {area}
    Task Order Number                         = {task_order_number}
    Reference UTC Datetime                    = {date}-

    [START]
    Start UTC Datetime                        = {date}-
    Estimated Completion UTC Datetime         = {date}-
    Comments                                  =

    [STOP]
    Stop UTC Datetime                         = {date}-
    Progress                                  =
    Comments                                  =

    [COMPLETE]
    Complete UTC Datetime                     = {date}-
    Comments                                  =
    """)
