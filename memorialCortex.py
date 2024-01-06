
class storage:
    
    def __init__(self, resolution, depth, count):
        
        self.resolution = resolution
        self.z = depth
        self.w = count
        self.size = (self.resolution ** 2) * self.z * self.w
        self.self = [[self.memoryNode(i,j,k,l)] for i,j,k,l in (range(self.resolution),range(self.resolution),range(self.z),range(self.w))]
    
    class memoryNode:
        
        def __init__(self, x, y, z, w, data):
            
            pass
        
    class group:
        
        def __init__(self):
            
            pass
        
        def averageClass(self):
            
            pass
        
        def addMem(self):
            
            pass
        
        def compareAverage(self):
            
            pass
        
    class memory:
        
        def __init__(self):
            
            pass
          
    def addMemory(self):
        
        pass
    
    def fetchMemory(self):
        
        pass
    
    def fetchMemories(self):
        
        pass
    
    def updateClasses(self):
        
        pass
    
    

