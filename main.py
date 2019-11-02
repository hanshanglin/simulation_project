from StageMachine import StageMachine
from Entity import Entity
from S_State import entity_state
from simulation_random import two_normal_ran, exp_ran
import itertools


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
    final_entity = []
    # simulation
    while t < 24*60*7:
        # step 1: release all machine
        for i in machine_list:
            i.release(t)
        # step 2: detect all final entity and replace by a new one
        for i, cur_entity in enumerate(waiting_queue):
            if (not cur_entity.isProcessing()) and (cur_entity.state is entity_state.Final):
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
        # step 4: update all machine
        for i in machine_list:
            i.update(t)
        t += 1
    return


if __name__ == "__main__":
    # config
    MAX_WAITING_QUEUE = 25
    MAX_MACHINE_NUM = 10

    def SPINNING_RV(): return two_normal_ran(240, 120)[0]

    def WEAVING_RV(): return two_normal_ran(480, 200)[0]

    def FINISHING_RV(): return exp_ran(1/120)

    def PACKING_RV(): return exp_ran(1/360)
    RV_list = [SPINNING_RV, WEAVING_RV, FINISHING_RV, PACKING_RV]
    machine_num = [0]*4
    # do all simulation for each step num[1...10]
    for machine_num in itertools.product(range(1, MAX_MACHINE_NUM+1), repeat=4):
        simulation(machine_num, RV_list)
