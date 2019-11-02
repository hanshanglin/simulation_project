from StageMachine import StageMachine
import Entity
import random
from S_State import *
from simulation_random import *







if __name__ == "__main__":
    # config
    MAX_WAITING_QUEUE = 25
    MAX_MACHINE_NUM = 10
    # TODO: change the prob generater into hand by methoud
    SPINNING_RV = lambda: two_normal_ran(240, 120)[0]
    WEAVING_RV = lambda: two_normal_ran(480, 200)[0]
    FINISHING_RV = lambda: exp_ran(1/120)
    PACKING_RV = lambda: exp_ran(1/360)

    # do all simulation for each step num[1...10]
    for s1_num in range(1, MAX_MACHINE_NUM + 1):
        for s2_num in range(1, MAX_MACHINE_NUM + 1):
            for s3_num in range(1, MAX_MACHINE_NUM + 1):
                for s4_num in range(1, MAX_MACHINE_NUM + 1):
                    """generate waiting_queue and machine"""
                    waiting_queue = [Entity.Entity() for i in range(MAX_WAITING_QUEUE)]
                    machine_list = []
                    machine_list += [
                        StageMachine(SPINNING_RV, entity.Weaving) for i in range(s1_num)
                    ]
                    machine_list += [
                        StageMachine(WEAVING_RV, entity.Finishing) for i in range(s2_num)
                    ]
                    machine_list += [
                        StageMachine(FINISHING_RV, entity.Packing) for i in range(s3_num)
                    ]
                    machine_list += [
                        StageMachine(PACKING_RV, entity.Final) for i in range(s4_num)
                    ]

                    """set init value """
                    t = 0
                    final_entity = []
                    """simulation"""
                    while t < 24*60*7:
                        # step 1: release all machine
                        for i in machine_list:
                            i.release(t)
                        # step 2: detect all final entity and replace by a new one
                        for i in range(0, len(waiting_queue)):
                            if (not waiting_queue[i].isProcessing()) and waiting_queue[i].state is entity.Final:
                                final_entity.append(waiting_queue[i])
                                waiting_queue[i] = Entity.Entity()
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
                        # step 4: update all machine
                        for i in machine_list:
                            i.update(t)
                        t += 1
                    break
                break
            break
        break
