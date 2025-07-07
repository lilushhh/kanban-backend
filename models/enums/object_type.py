from enum import Enum as PyEnum

class ObjectType(str, PyEnum):
    PROJECT = "project"
    TASK = "task"