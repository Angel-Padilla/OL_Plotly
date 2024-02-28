from enum import Enum, auto

class Axis(Enum):
    XMAIN = auto()
    XAUX = auto()
    YMAIN = auto()
    YAUX = auto()

class Marker(Enum):
    CIRCLE = auto()