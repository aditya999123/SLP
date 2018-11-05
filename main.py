from yard import Yard
from protocols import CyclicRouting

import random

yard = Yard (
	l = 200, # length of the yard 
	b = 200, # breadth of the yard
	# init = 0.45, # initial energy of each node
	# free_space = 0.0000005,
	# multi_path = 0.00000000012,
	# grid_side_length = 20,
)

# populate with 100 nodes at random locations
yard.modify_sink_location(80, 120)
yard.populate(100)

# for node in yard.nodes:
# 	print node, node.id

# print yard.sink.energy
# print yard.energy



panda_x = random.randint(0, yard.l)
panda_y = random.randint(0, yard.b)

yard.clustering()

yard.evaluate(panda_x, panda_y)
cyclic_routing = CyclicRouting(yard)
cyclic_routing.execute(panda_x, panda_y)
