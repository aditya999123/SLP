from math import sqrt
from helpers import dist, colour

import matplotlib.pyplot as plt 

class CyclicRouting:
	rings = 10
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
			ring_no = round((dist(node.x, node.y, self.yard.sink.x, self.yard.sink.y) + ring_size - 1)/ring_size);

			self.ring[ring_no].append(node)

		self.show_rings_on_graph()

	def show_rings_on_graph(self):
		for ring_no, nodes in self.ring.items():
			x = []
			y = []

			for node in nodes:
				x.append(node.x)
				y.append(node.y)

			plt.scatter(x, y, label = "ring %d" % ring_no, color= colour[ring_no], marker= "*", s=30)

		x = [self.yard.sink.x]
		y = [self.yard.sink.y]

		plt.scatter(x, y, label = "sink", color = 'black', marker = "s", s=30)

		plt.show()