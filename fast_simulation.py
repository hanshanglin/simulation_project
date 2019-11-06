from StageMachine import StageMachine
from Entity import Entity
from S_State import entity_state
import itertools
import random
import numpy as np
import logging
from config import *
from multiprocessing import Pool, cpu_count, freeze_support
import os
import pandas as pd


def simulation(machine_num, RNG, waiting_queue=25):
    # generate waiting_queue and machine
    waiting_queue = [Entity(0) for i in range(MAX_WAITING_QUEUE)]
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
    final_entity = []
    end_t = 24*60*7*60
    end_flag = True
    # simulation -- a week
    while end_flag:
        logging.debug('\n'+"T="+str(t))
        # control the end time to end_t
        if t > end_t:
            t = end_t
            end_flag = False

        # step 1: release all machine
        for i in machine_list:
            i.release(t)

        # step 2: detect all final entity and replace by a new one
        for i, cur_entity in enumerate(waiting_queue):
            # entity not in prcessed and the state is Final
            if (not cur_entity.isProcessing()) and (cur_entity.state is entity_state.Final):
                # all finished entity collected in final_entity
                final_entity.append(cur_entity)
                # add new entity in the origin place
                waiting_queue[i] = Entity(t)

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
        next_idle_time = end_t
        for i in machine_list:
            next_idle_time = min(next_idle_time, i.release(t))
        logging.debug("next T="+str(next_idle_time))
        # # step 5: update all machine
        # for i in machine_list:
        #     i.update(t)

        # step 6: change t
        if next_idle_time > t:
            t = next_idle_time
        else:
            t = t+1

    # since the waitting cost is update by "start", update the entity which didn't "start"
    for e in waiting_queue:
        if(not e.isProcessing()):
            e.update_waitting_time(t)
    # get idle time:
    machine_idle_result = [0]*4
    for i, m in enumerate(machine_list):
        if i < machine_num[0]:
            machine_idle_result[0] += m.getIdleTime(t)
        elif i < sum(machine_num[:2]):
            machine_idle_result[1] += m.getIdleTime(t)
        elif i < sum(machine_num[:3]):
            machine_idle_result[2] += m.getIdleTime(t)
        elif i < sum(machine_num[:]):
            machine_idle_result[3] += m.getIdleTime(t)
        else:
            print("ERROR")
    # get waitting cost:
    waiting_cost_result = [0]*4
    for e in map(lambda x: x.getWaitingTime(), final_entity):
        waiting_cost_result[0] += e[0]
        waiting_cost_result[1] += e[1]
        waiting_cost_result[2] += e[2]
        waiting_cost_result[3] += e[3]
    for e in map(lambda x: x.getWaitingTime(), waiting_queue):
        waiting_cost_result[0] += e[0]
        waiting_cost_result[1] += e[1]
        waiting_cost_result[2] += e[2]
        waiting_cost_result[3] += e[3]

    print("machine_num: {0[0]:<3}{0[1]:<3}{0[2]:<3}{0[3]:<3} finish entity number:{1:<5}\
    machine idle time: {2[0]:<12}{2[1]:<12}{2[2]:<12}{2[3]:<12}  \
    waitting cost:{3[0]:<12}{3[1]:<12}{3[2]:<12}{3[3]:<12} sum:{4:<12} endT:{5}".format(machine_num, len(final_entity), machine_idle_result, waiting_cost_result, sum(waiting_cost_result), end_t))
    return machine_num, machine_idle_result, waiting_cost_result, len(final_entity)


def pall_task(n):
    machine_num_list = []
    machine_idle_list = []
    waitting_time_list = []
    finish_number_list = []

    for machine_num in itertools.product(range(1, MAX_MACHINE_NUM+1), repeat=3):
        num = (n, machine_num[0], machine_num[1], machine_num[2])
        record = simulation(num, RV_list)
        machine_num_list.append(record[0])
        machine_idle_list.append(record[1])
        waitting_time_list.append(record[2])
        finish_number_list.append(record[3])

    df = pd.DataFrame(
    {"machine_number": machine_num_list, 
    "machine1_idle": [i[0] for i in machine_idle_list], 
    "machine2_idle": [i[1] for i in machine_idle_list],
    "machine3_idle": [i[2] for i in machine_idle_list], 
    "machine4_idle": [i[3] for i in machine_idle_list],
    "waitting1":[i[0] for i in waitting_time_list],
    "waitting2":[i[1] for i in waitting_time_list],
    "waitting3":[i[2] for i in waitting_time_list],
    "waitting4":[i[3] for i in waitting_time_list],
    "finish_number":finish_number_list
    })
    df.to_csv("save_"+str(n)+".csv")


if __name__ == "__main__":
    # config
    logging.basicConfig(handlers=[logging.FileHandler("test1.log", encoding="utf-8", mode="w")], format='[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=OUTPUTLEVEL)
    # simulation((1,1,1,1),RV_list)
    freeze_support()
    p = Pool()
    for i in range(1, 11):
        p.apply_async(pall_task, args=(i,))
    p.close()
    p.join()
