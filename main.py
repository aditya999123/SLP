from yard import Yard

yard = Yard(100, 200)
yard.populate(100)

for node in yard.nodes:
	print node