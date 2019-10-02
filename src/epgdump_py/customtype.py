from enum import Enum
from typing import Dict, Tuple

from .constant import TYPE_DEGITAL, TYPE_BS, TYPE_CS

ServiceMap = Dict[int, Tuple[str, int, int]]


class BType(Enum):
    digital = TYPE_DEGITAL
    bs = TYPE_BS
    cs = TYPE_CS
