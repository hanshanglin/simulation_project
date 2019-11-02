from enum import Enum, unique


@unique
class machine_state(Enum):
    ''' Contain two states  
    "Idle" and "Work"
    '''
    Idle = 0
    Work = 1

    def next(self):
        ''' flip the machine state  
        Idle->Work  
        Work->idle
        '''
        cls = self.__class__
        members = list(cls)
        index = 1-members.index(self)
        return members[index]


@unique
class entity_state(Enum):
    '''contain 5 states   
    "Spinning" "Weaving" "Finishing" "Packing" and "Final"   
    '''
    Spinning = 1
    Weaving = 2
    Finishing = 3
    Packing = 4
    Final = 5

    def next(self):
        ''' return next state  
        "Spinning"->"Weaving"->"Finishing"->"Packing"->"Final"
        '''
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = index - 1
        return members[index]
