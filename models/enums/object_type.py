from enum import Enum

class ObjectType(str, Enum):
    PROJECT = "project"
    TASK = "task"