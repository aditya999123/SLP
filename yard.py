from nodes import Node
import random

class Energy:
	def __init__(self, kwargs):
		# initial energy of each node
		self.init = 0.5
		if kwargs.get('init'):
			self.init = kwargs['init']

		# energy for transferring of each bit 
		self.trans = 50*0.000000001
		if kwargs.get('trans'):
			self.trans = kwargs['trans']

		# energy for receiving of each bit 
		self.rec = 50*0.000000001
		if kwargs.get('rec'):
			self.rec = kwargs['rec']

		# energy for free space model
		self.free_space = 10*0.000000000001
		if kwargs.get('free_space'):
			self.free_space = kwargs['free_space']

		# energy for multi path model
		self.multi_path = 0.0013*0.000000000001
		if kwargs.get('multi_path'):
			self.multi_path = kwargs['multi_path']

		# data aggregation energy
		self.aggr = 5*0.000000001
		if kwargs.get('aggr'):
			self.aggr = kwargs['aggr']

	def __str__(self):
		response = ""
		response += "init = %.1E\n" % self.init
		response += "trans = %.1E\n" % self.trans
		response += "rec = %.1E\n" % self.rec
		response += "free_space = %.1E\n" % self.free_space
		response += "multi_path = %.1E\n" % self.multi_path
		response += "aggr = %.1E\n" % self.aggr

		return response

class Yard:
	def __init__(self, l = 100, b = 100, *args, **kwargs):
		self.l = l # length of the yard
		self.b = b # breadth of the yard
		
		self.nodes = []
		self.energy = Energy(kwargs) # initialize all values for energy calculations

		# 1st node with id = 0 is used as sink, initially placed at center
		self.sink = Node(self.l/2, self.b/2, self.energy.init)


	# modify location of the sink
	def sink_modify_location(self, x, y):
		self.sink.x = x
		self.sink.y = y

	# populate the yard with num nodes at random locations with initial energy
	def populate(self, num):
		for i in range(num):
			
			x = random.randint(0, self.l)
			y = random.randint(0, self.b)

			self.nodes.append(Node(x, y, self.energy.init))