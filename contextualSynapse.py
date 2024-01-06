class context:
    def __init__(self,memories,ids):
        self.memories = memories
        self.ids = ids
        self.self = [[i,"",[],[]] for i,j in enumerate(self.ids)]
        self.classes = []
    def update_memories(self,memories,ids):
        self.memories = memories
        self.ids = ids
c = context([0,0,0],[0,0,0])