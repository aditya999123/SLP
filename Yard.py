from nodes import Node
from Grid import Grid
from Energy import Energy
from Packet import Packet

import random

class Yard:
	def __init__(self, l = 100, b = 100, *args, **kwargs):
		self.l = l # length of the yard
		self.b = b # breadth of the yard
		
		self.nodes = []

		# initialize all values for energy calculations
		self.energy = Energy(kwargs)
		self.packet = Packet()

		self.grid_size = kwargs.get('grid_size', 20)

		cols = self.l  / self.grid_size + 1
		rows = self.b  / self.grid_size + 1
		self.grid = [[Grid(row, col) for col in range(cols)] for row in range(rows)] #[0]energy, [1]id
		
		# 1st node with id = 0 is used as sink, initially placed at center
		sink_x = self.l / 2
		sink_y = self.b / 2
		sink_cell = self.grid[sink_x / self.grid_size][sink_y / self.grid_size]
		self.sink = Node(sink_x, sink_y, self.energy.init, sink_cell)

	# modify location of the sink
	def modify_sink_location(self, x, y):
		self.sink.x = x
		self.sink.y = y

	# populate the yard with num nodes at random locations with initial energy
	def populate(self, num):
		for i in range(num):
			
			x = random.randint(0, self.l - 1)
			y = random.randint(0, self.b - 1)

			cell = self.grid[x/self.grid_size][y/self.grid_size]
			self.nodes.append(Node(x, y, self.energy.init, cell))

		self.clusterize()

	# determine cluster heads
	def clusterize(self):
		# after every iteration cluster head needs to be calculated agagin
		for row in self.grid:
			for cell in row:
				cell.energy = 0
				cell.head = None

		for node in self.nodes :
			if node.cell.head is None or node.energy > node.cell.head.energy :
				node.cell.head = node

		for node in self.nodes :
			if node.cell.head is not None and node == node.cell.head:
				node.make_cluster_head()
			else:
				node.has_head()

		print "clusterized"

		# for row in self.grid:
		# 	for cell in row:
		# 		if cell.head is not None:
		# 			print cell.head.id