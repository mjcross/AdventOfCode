from dataclasses import dataclass, field

@dataclass
class MyClass:
    children: set = field(default_factory=set)

instance = MyClass()
instance.children.add(42)

print(instance)