from S_State import entity_state

class entity_count():
    count = 0
class Entity(entity_count):
    def __init__(self):
        self.state = entity_state.Spinning
        self.start_time = []
        self.end_time = []
        self.processing = False
        self.id = entity_count.count
        entity_count.count +=1

    def finish(self,cur_time):
        self.state = self.state.next()
        self.end_time.append(cur_time)
        self.processing = not self.processing
        return self.state
    
    def start(self,cur_time):
        self.start_time.append(cur_time)
        self.processing = not self.processing
        return self.state

    def stage(self):
        return self.stage

    def isProcessing(self):
        return self.processing

    def getName(self):
        return "entity-"+str(self.id)


