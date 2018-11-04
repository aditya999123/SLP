from yard import Yard

yard = Yard (
	l = 100, # length of the yard 
	b = 200, # breadth of the yard
	# init = 0.45, # initial energy of each node
	# free_space = 0.0000005,
	# multi_path = 0.00000000012,
)

# populate with 100 nodes at random locations
yard.populate(100)

for node in yard.nodes:
	print node, node.id

print yard.sink.energy
print yard.energy