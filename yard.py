from nodes import Node
import random

class Energy:
	def __init__(self, kwargs):
		self.init = 0.5
		if kwargs.get('init'):
			self.init = kwargs['init']

		self.trans = 50*0.000000001
		if kwargs.get('trans'):
			self.trans = kwargs['trans']

		self.rec = 50*0.000000001
		if kwargs.get('rec'):
			self.rec = kwargs['rec']

		self.free_space = 10*0.000000000001
		if kwargs.get('free_space'):
			self.free_space = kwargs['free_space']

		self.multi_path = 0.0013*0.000000000001
		if kwargs.get('multi_path'):
			self.multi_path = kwargs['multi_path']

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
		self.l = l
		self.b = b
		
		self.nodes = []
		self.energy = Energy(kwargs)

		self.sink = Node(self.l/2, self.b/2, self.energy.init)


	def sink_modify(self, x, y):
		self.sink.x = x
		self.sink.y = y

	def populate(self, num):
		for i in range(num):
			
			x = random.randint(0, self.l)
			y = random.randint(0, self.b)

			self.nodes.append(Node(x, y, self.energy.init))