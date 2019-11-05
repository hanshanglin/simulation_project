import Entity
from S_State import machine_state
import logging
from config import *

logging.basicConfig(format='[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=OUTPUTLEVEL)
class machine_count():
    count = 0
class StageMachine(machine_count):
    machine_id = 0
    def __init__(self, RV_generater, machine_type):
        self.RV = RV_generater
        self.type = machine_type
        self.state = machine_state.Idle
        self.next_idle_time = -1
        self.idle_time = 0
        self.entity = None
        self.id = machine_count.count 
        machine_count.count += 1
        
    def update(self,cur_time):
        if self.state == machine_state.Idle:
            self.idle_time +=1
        else:
            if cur_time>=self.next_idle_time:
                logging.debug(str(self.type)+str(self.id)+" finish: "+self.entity.id)
                self.entity.finish(cur_time)
                self.state = machine_state.Idle
                self.entity = None
        return self.state
    
    def release(self,cur_time):
        if self.state == machine_state.Work:
            if cur_time>=self.next_idle_time:
                self.state = machine_state.Idle
                logging.debug("{:<20}          finish{:>15}".format(self.getName(),self.entity.getName()))
                self.entity.finish(cur_time)
                self.entity = None
                return INTMAX
            else:
                return self.next_idle_time
        return INTMAX

    def process(self,entity,cur_time):
        if(self.type != entity.state.next()):
            print("ERROR:TYPE UNMATCHED")
            exit(1)
        if(not self.isIdle):
            print("ERROR:entity double processed")
        rv = self.RV()
        self.next_idle_time = cur_time+rv
        self.state = machine_state.Work
        self.entity = entity
        self.entity.start(cur_time)
        logging.debug("{:<20}start processing{:>15} rv:{:>5} next:{:>10}".format(self.getName(),self.entity.getName(),str(rv),str(self.next_idle_time)))
        return 0

    def isIdle(self):
        return self.state == machine_state.Idle

    def getName(self):
        return str(self.type.name)+"-"+str(self.id)
