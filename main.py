from yard import Yard

yard = Yard(
	l = 100, 
	b = 200,
	# init = 0.45,
	# free_space = 0.0000005,
	# multi_path = 0.00000000012,
)

yard.populate(100)

# for node in yard.nodes:
# 	print node

print yard.sink.energy
print yard.energy