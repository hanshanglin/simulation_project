from S_State import entity_state
class Entity(object):
    def __init__(self):
        self.state = entity_state.Spinning
        self.start_time = []
        self.end_time = []
        self.processing = False

    def finish(self,cur_time):
        self.state = self.state.next()
        self.end_time.append(cur_time)
        return self.state
    
    def start(self,cur_time):
        self.start_time.append(cur_time)
        return self.state

    def stage(self):
        return self.stage

    def isProcessing(self):
        return self.processing


