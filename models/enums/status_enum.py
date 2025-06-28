from enum import Enum

class StatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    DONE = "done"