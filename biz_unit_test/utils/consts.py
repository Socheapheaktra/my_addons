from strenum import StrEnum


class Colors(StrEnum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AssertStatus(StrEnum):
    FAIL = "FAILED"
    PASS = "PASSED"


class Formats(StrEnum):
    DATE = "%Y-%m-%d"
    DATETIME = "%Y-%m-%d %H:%M:%S"
