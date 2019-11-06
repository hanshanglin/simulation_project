import Entity
from S_State import machine_state
import logging
from config import *

logging.basicConfig(handlers=[logging.FileHandler("test1.log", encoding="utf-8",mode="w")],format='[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=OUTPUTLEVEL)
class machine_count():
    count = 0
class StageMachine(machine_count):
    def __init__(self, RV_generater, machine_type):
        self.RV = RV_generater
        self.type = machine_type
        self.state = machine_state.Idle
        self.next_idle_time = 0
        self.idle_time = 0
        self.entity = None
        self.last_idle_time = 0
        self.id = machine_count.count 
        machine_count.count += 1
        
    def update(self,cur_time):
        if self.state == machine_state.Idle:
            self.idle_time += cur_time - self.last_idle_time
            self.last_idle_time = cur_time
        else:
            if cur_time>=self.next_idle_time:
                logging.debug(str(self.type)+str(self.id)+" finish: "+self.entity.id)
                self.entity.finish(cur_time)
                self.state = machine_state.Idle
                self.entity = None
        return self.state
    
    def release(self,cur_time):
        '''release finished entity, update last idle time as cur_time  
            if the machine is idle return INF(no need to update)  
            if the machine is working return the time when the current work is finished
        '''
        if self.state == machine_state.Work:
            if cur_time>self.next_idle_time:
                print("ERROR: the machine update time is wrong")
                exit(1)
            # if the current processing is done, finish the entity
            if cur_time==self.next_idle_time:
                # change the machine state
                self.state = machine_state.Idle
                # update the idle time
                self.last_idle_time = cur_time
                # logging
                logging.debug("{:<20}          finish{:>15}".format(self.getName(),self.entity.getName()))
                # update the entity
                self.entity.finish(cur_time)
                self.entity = None

                return INTMAX
            else:
                return self.next_idle_time
        else:
            return INTMAX

    def process(self,entity,cur_time):
        ''' process an entity and update the idle time.  
        Notice: machine idle time only will be updated in this function
        '''
        if(self.type != entity.state.next()):
            print("ERROR:TYPE UNMATCHED")
            exit(1)
        if(not self.isIdle):
            print("ERROR:entity double processed")
            exit(1)
        # get a new RV as the time that process need
        rv = self.RV()
        # store the finish time
        self.next_idle_time = cur_time+rv
        # change the machine state to work
        self.state = machine_state.Work
        # biding the entity
        self.entity = entity
        self.entity.start(cur_time)
        # update the idle time
        self.idle_time += cur_time-self.last_idle_time

        logging.debug("{:<20}start processing{:>15} rv:{:>5} next:{:>10}".format(self.getName(),self.entity.getName(),str(rv),str(self.next_idle_time)))
        return 0

    def isIdle(self):
        return self.state == machine_state.Idle

    def getName(self):
        return str(self.type.name)+"-"+str(self.id)

    def getIdleTime(self,cur_time):
        if self.state == machine_state.Work:
            # the idle time is already updated in the last "process"
            return self.idle_time
        else:
            # the idle time need to be updated from last "release" to cur time
            return self.idle_time + (cur_time - self.last_idle_time)

