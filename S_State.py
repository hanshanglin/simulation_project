from enum import Enum, unique


@unique
class machine_state(Enum):
    Idle = 0  
    Work = 1

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = 1-members.index(self)
        return members[index]


@unique
class entity_state(Enum):
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
            index = index - 1
        return members[index]
