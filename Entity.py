from S_State import entity_state

class entity_count():
    count = 0
class Entity(entity_count):
    def __init__(self,cur_time):
        self.state = entity_state.Spinning
        self.start_time = []
        self.end_time = []
        self.processing = False
        self.last_finish_time = cur_time
        self.waiting_record = []
        self.id = entity_count.count
        self.last_waitting_update = cur_time
        entity_count.count +=1

    def finish(self,cur_time):
        '''finish an entity, change the state to next state and start to record waitting time'''
        # change state
        self.state = self.state.next()
        # record end_time use for debug TODO: delete 
        self.end_time.append(cur_time)
        # change the entity to not processing
        self.processing = False
        # record the time start to wait
        self.last_finish_time = cur_time
        return self.state
    
    def start(self,cur_time):
        '''start to precess an entity,record the waitting time from last finished'''
        # record start_time use for debug TODO: delete 
        self.start_time.append(cur_time)
        # change the entity to processing
        self.update_waitting_time(cur_time)
        self.processing = True
        return self.state

    def update_waitting_time(self,cur_time):
        '''update the time in waiting'''
        if not self.processing:
            # only entity not in processing can be updated 
            self.waiting_record.append(cur_time-self.last_finish_time)
            self.last_finish_time = cur_time

    def stage(self):
        return self.stage

    def isProcessing(self):
        return self.processing

    def getWaitingTime(self):
        while len(self.waiting_record)<4:
            self.waiting_record.append(0)
        return self.waiting_record

    def getName(self):
        return "entity-"+str(self.id)


