from math import sqrt
from helpers import dist, colour
from Yard import Yard
from Packet import Packet
import time
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

	def plot_grid(self, plt_node_ch):
		for x in range(0, self.yard.l, self.yard.grid_size):
			y = self.yard.b
			plt_node_ch.plot([x, x], [0, y], linewidth = .3, color = 'black', linestyle = '-.')

		for y in range(0, self.yard.b, self.yard.grid_size):
			x = self.yard.l
			plt_node_ch.plot([0, x], [y, y], linewidth = .3, color = 'black', linestyle = '-.')

	def plot_nodes_ch(self, plt_node_ch, panda_x, panda_y):
		sensors_x = []
		sensors_y = []

		CH_x = []
		CH_y = []

		plt_node_ch.cla()
		self.plot_grid(plt_node_ch)

		for node in self.yard.nodes:
			if node.energy <= 0:
				continue
				
			if node.is_cluster_head:
				CH_x.append(node.x)
				CH_y.append(node.y)
			else:
				sensors_x.append(node.x)
				sensors_y.append(node.y)

		plt_node_ch.scatter(sensors_x, sensors_y, label = "sensor", color = "blue", marker = "*", s=30)
		plt_node_ch.scatter(CH_x, CH_y, label = "CH", color = "black", marker = "*", s=30)

		plt_node_ch.scatter([panda_x], [panda_y], label = "panda", color = "red", marker = "d", s=60)
		plt_node_ch.scatter([self.yard.sink.x], [self.yard.sink.y], label = "sink", color = "green", marker = "s", s=60)
		plt_node_ch.legend()
		# plt_node_ch

	def plot_energy(self, plt_energy):
		energy_y = []
		node_id = []

		plt_energy.cla()

		for node in self.yard.nodes:
			energy_y.append(max(node.energy, 0))
			node_id.append(node.id)

		plt_energy.bar(node_id, energy_y, align='center')	
		plt_energy.legend()	

	def execute(self, panda_x, panda_y):
		packet = Packet()
		self.eval_rings()
		
		sensors = []

		fig = plt.figure()
		plt.ion()
		plt.show()
		# plt.legend()
		plt_node_ch = fig.add_subplot(211)
		plt_energy = fig.add_subplot(212)

		while self.sense(sensors, panda_x, panda_y):
			self.plot_nodes_ch(plt_node_ch, panda_x, panda_y)
			self.plot_energy(plt_energy)

			plt.pause(1e-50)
			# time.sleep(0.1)

			CyclicRouting.iteration += 1

			cluster_heads = []
			for node in sensors:
				print "abc", node, node.energy
				# A cluster head maintains cache, therefore a cluster would trigger the ring only once
				if node.cell.head not in cluster_heads:
					cluster_heads.append(node.cell.head)

				print "nn1", node

				if node.is_cluster_head:
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
							val = 1

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

					#only one node remains in the ring || should be thought of
					if d_nodes[1][1] is None and d_nodes[-1][1] is None:
						cell.head.energy = 0

				self.yard.clusterize()
				self.eval_rings()

			sensors = []

		print "iterations done: ", CyclicRouting.iteration
		plt.show()
		plt.pause(10)