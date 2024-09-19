from enum import IntFlag


class ExitCode(IntFlag):
    Success = 0
    Failure = 1
    Aborted = 2

