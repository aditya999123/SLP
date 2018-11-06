from math import sqrt
from helpers import dist, colour
from Yard import Yard
from Packet import Packet
import matplotlib.pyplot as plt 

class CyclicRouting:
	iteration = 0

	def __init__(self, yard):
		self.yard = yard
		self.rings = {}

	def eval_rings(self):
		rings = max(self.yard.l/self.yard.grid_size, self.yard.b/self.yard.grid_size) + 1

		for i in range(0, rings):
			self.rings[i] = []

		for row in self.yard.grid:
			for cell in row:
				if cell.head is None:
					continue
				d_x = abs(cell.row - self.yard.sink.cell.row)
				d_y = abs(cell.col - self.yard.sink.cell.col)

				ring = max(d_x, d_y)
				self.rings[ring].append(cell)
				cell.head.ring = ring

		# need to rethink this
		# self.rings[0] = [self.yard.sink.cell]

		for x, cells in self.rings.items():
			print x, [cell.head.id for cell in cells]

	def sense(self, sensors, panda_x, panda_y):
		sensor_range = sqrt(5)*self.yard.grid_size
		
		for sensor_node in self.yard.nodes:
			if (sensor_node.energy > 0
				and dist(sensor_node.x, sensor_node.y, panda_x, panda_y) <= sensor_range
				):
				
				sensors.append(sensor_node)

		print "len", len(sensors)
		return len(sensors) > 0

	def execute(self, panda_x, panda_y):
		packet = Packet()
		self.eval_rings()
		
		sensors = []
		while self.sense(sensors, panda_x, panda_y):
			CyclicRouting.iteration += 1

			cluster_heads = []
			for node in sensors:
				print "abc", node, node.energy
				# A cluster head maintains cache, therefore a cluster would trigger the ring only once
				if node.cell.head not in cluster_heads:
					cluster_heads.append(node.cell.head)

				print "nn1", node

				if(node.cell.head == node):
					continue
				
				print "nn", node

				node.send_data_non_ch(self.yard.energy, packet)

			rings = []
			for head in cluster_heads:
				# Panda detected from different cluster, can belong to same ring or other
				rings.append(head.ring)

			for ring in rings:
				for cell in self.rings[ring]:
					maxd = dist(0, 0, self.yard.l, self.yard.b)

					d_nodes = {
						 1: [maxd, None], # clockwise
						-1: [maxd, None]  # anti-clockwise
					}

					for node in self.rings[ring] :

						try: 
							val = ((node.head.x - self.yard.sink.x) / (self.yard.sink.x - cell.head.x) 
							- (node.head.y - self.yard.sink.y) / (self.yard.sink.y - cell.head.y))
						except:
							continue

						if val is 0:
							continue

						sign = val/abs(val)

						d = dist(node.head.x, node.head.y, cell.head.x, cell.head.y)
						if d < d_nodes[sign][0]:
							d_nodes[sign][0] = d
							d_nodes[sign][1] = node

					if d_nodes[1][1] is not None:
						cell.head.send_data_ch(self.yard.energy, packet, d_nodes[1][0])
						cell.head.receive_data(self.yard.energy, packet)

					if d_nodes[-1][1] is not None:
						cell.head.send_data_ch(self.yard.energy, packet, d_nodes[-1][0])
						cell.head.receive_data(self.yard.energy, packet)

					if d_nodes[1][1] is None and d_nodes[-1][1] is None:
						cell.head.energy = 0

				self.yard.clusterize()
				self.eval_rings()

			sensors = []

		print "iterations done: ", CyclicRouting.iteration



