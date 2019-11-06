from StageMachine import StageMachine
from Entity import Entity
from S_State import entity_state
import itertools
import random
import numpy as np
import logging
from config import *
from multiprocessing import Pool
import os 

def simulation(machine_num, RNG, waiting_queue=25):
    # generate waiting_queue and machine
    waiting_queue = [Entity() for i in range(MAX_WAITING_QUEUE)]
    machine_list = []
    machine_list += [StageMachine(RNG[0], entity_state.Weaving)
                     for i in range(machine_num[0])]
    machine_list += [StageMachine(RNG[1], entity_state.Finishing)
                     for i in range(machine_num[1])]
    machine_list += [StageMachine(RNG[2], entity_state.Packing)
                     for i in range(machine_num[2])]
    machine_list += [StageMachine(RNG[3], entity_state.Final)
                     for i in range(machine_num[3])]
    # set init value
    t = 0
    count = 0
    final_entity = []
    end_t = 24*60*7*60
    # simulation -- a week
    while t < end_t: 
        logging.debug('\n'+"T="+str(t))
        # step 1: release all machine
        for i in machine_list:
            i.release(t)
        # step 2: detect all final entity and replace by a new one
        for i, cur_entity in enumerate(waiting_queue):
            if (not cur_entity.isProcessing()) and (cur_entity.state is entity_state.Final):
                #if flag:
                #    logging.debug("First entity finished, T = "+str(t))
                #    end_t+=t
                #    flag = not flag
                final_entity.append(cur_entity)
                waiting_queue[i] = Entity()
        # step 3: process entity as much as possible
        for i in waiting_queue:
            # find the entity which is not processing
            if i.isProcessing():
                continue
            # find if some machine is idle
            for m in machine_list:
                if m.isIdle() and m.type is i.state.next():
                    m.process(i, t)
                    break
            # end
        # step 4: collect all next idle time
        next_idle_time = INTMAX
        for i in machine_list:
            next_idle_time = min(next_idle_time,i.release(t))
        
        # step 5: update all machine
        for i in machine_list:
            i.update(t)

        # step 6: change t
        if next_idle_time>t:
            t = next_idle_time
        else:
            t = t+1
        count+=1
    print(len(final_entity))
    print(str(machine_num)+" "+str(count))
    return



if __name__ == "__main__":
    # config
    logging.basicConfig(format='[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=OUTPUTLEVEL)
    p = Pool()
    for i in range(1,11):
        p.apply_async(simulation,args=((i,i,i,i),RV_list,))
    p.close()
    p.join()