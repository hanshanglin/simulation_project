from S_State import entity_state

class entity_count():
    count = 0
class Entity(entity_count):
    def __init__(self):
        self.state = entity_state.Spinning
        self.start_time = []
        self.end_time = []
        self.processing = False
        self.last_finish_time = 0
        self.waiting_record = []
        self.id = entity_count.count
        entity_count.count +=1

    def finish(self,cur_time):
        self.state = self.state.next()
        self.end_time.append(cur_time)
        self.processing = not self.processing
        self.last_finish_time = cur_time
        return self.state
    
    def start(self,cur_time):
        self.start_time.append(cur_time)
        self.processing = not self.processing
        self.waiting_record.append(cur_time-self.last_finish_time)
        return self.state

    def stage(self):
        return self.stage

    def isProcessing(self):
        return self.processing

    def getWaitingTime(self):
        return self.waiting_record

    def getName(self):
        return "entity-"+str(self.id)


