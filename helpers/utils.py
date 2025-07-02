from enum import Enum
from typing import Optional
from uuid import UUID

def to_serializable(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Enum):
        return obj.value
    return str(obj)
