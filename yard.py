from nodes import Node
import random

class Yard:
	def __init__(self, l = 100, b = 100):
		self.l = l
		self.b = b
		self.sink = Node(self.l/2, self.b/2)
		self.nodes = []

	def sink_modify(self, x, y):
		self.sink.x = x
		self.sink.y = y

	def populate(self, num):
		for i in range(num):
			
			x = random.randint(0, self.l)
			y = random.randint(0, self.b)

			self.nodes.append(Node(x, y))