from Yard import Yard
from Protocols import CyclicRouting

import random

yard = Yard (
	l = 500, # length of the yard 
	b = 500, # breadth of the yard
	init = 0.5, # initial energy of each node
	# free_space = 0.0000005,
	# multi_path = 0.00000000012,
	# grid_size = 20,
)

yard.modify_sink_location(80, 120)

# populate with 100 nodes at random locations
yard.populate(100)


panda_x = random.randint(0, yard.l)
panda_y = random.randint(0, yard.b)


cyclic_routing = CyclicRouting(yard)
cyclic_routing.execute(panda_x, panda_y)
