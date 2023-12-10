from dataclasses import dataclass
from typing import Self

@dataclass
class Node:
    left: Self = None
    right: Self = None

