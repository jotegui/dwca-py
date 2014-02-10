class Flag():
    
    def __init__(self, name, flags):
        self.name = name
        self.flags = flags
    
    def flagged(self):
        return [i for i in list(range(len(self.flags))) if self.flags[i]==1]
    
    def nonFlagged(self):
        return [i for i in list(range(len(self.flags))) if self.flags[i]==0]
