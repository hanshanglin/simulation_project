from enum import Enum, unique


@unique
class machine(Enum):
    Idle = 0  
    Work = 1


@unique
class entity(Enum):
    Spinning = 1
    Weaving = 2
    Finishing = 3
    Packing = 4
    Final = 5

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]
