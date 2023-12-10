from dataclasses import dataclass, field
from typing import Self     # allow Node to have properties of type Node

@dataclass
class Node:
    left: Self = None
    right: Self = None
    isEndNode: bool = False
    name: str = None

    def __str__(self):
        return f'{self.name} = ({self.left.name}, {self.right.name})'
    
    def __repr__(self):
        return self.name

@dataclass
class Tree:
    startNodes: list[Node] = field(default_factory=list)
    endNodes: list[Node] = field(default_factory=list)