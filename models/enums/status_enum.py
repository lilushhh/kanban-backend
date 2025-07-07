from enum import Enum as PyEnum

class StatusEnum(str, PyEnum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    DONE = "done"