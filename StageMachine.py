import numpy as np
import Entity
from S_State import machine
class StageMachine(object):
    def __init__(self, RV_generater, machine_type):
        self.RV = RV_generater
        self.type = machine_type
        self.state = machine.Idle
        self.next_idle_time = -1
        self.idle_time = 0
        self.entity = None
        
    def update(self,cur_time):
        if self.state == machine.Idle:
            self.idle_time +=1
        else:
            if cur_time>=self.next_idle_time:
                self.state = machine.Idle
                self.entity.finish(cur_time)
                self.entity = None
        return self.state
    
    def release(self,cur_time):
        if self.state == machine.Work:
            if cur_time>=self.next_idle_time:
                self.state = machine.Idle
                self.entity.finish(cur_time)
                self.entity = None
        return self.state

    def process(self,entity,cur_time):
        if(self.type != entity.state.next()):
            print("ERROR:TYPE UNMATCHED")
            exit(1)
        if(not self.isIdle):
            print("ERROR:entity double pocessed")
        rv = self.RV()
        self.next_idle_time = cur_time+rv
        self.state = machine.Work
        self.entity = entity
        self.entity.start(cur_time)
        return 0

    def isIdle(self):
        return self.state == machine.Idle

