import CustodianLobe.memorialCortex as mc
mem = mc.storage(4,4,4,2)
mem.fill()
mems = mem.fetchMemory(0,0)
mem.addMemory([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],2,1)
print(mem.retMemories())