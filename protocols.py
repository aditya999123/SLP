from math import sqrt
from helpers import dist

import matplotlib.pyplot as plt 

class CyclicRouting:
	rings = 6
	def __init__(self, yard):
		self.yard = yard
		self.ring = {
		}

		for i in range(CyclicRouting.rings+1):
			self.ring[i] = []

	def evaluate(self, panda_x, panda_y):
		maxd = dist(0, 0, self.yard.l, self.yard.b)
		ring_size = int(maxd/CyclicRouting.rings);

		for node in self.yard.nodes:
			ring_no = int((dist(node.x, node.y, self.yard.sink.x, self.yard.sink.y) + ring_size - 1)/ring_size);

			self.ring[ring_no].append(node.id)

	def __str__(self):
		for x, y in self.ring.items():
			print "ring", x, y

		return ""