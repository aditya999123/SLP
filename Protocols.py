from math import sqrt
from helpers import dist, colour
from Packet import Packet
from Yard import Yard

import matplotlib.pyplot as plt 

class CyclicRouting:
	def __init__(self, yard):
		self.yard = yard

		rings = max(self.yard.l/self.yard.grid_size, self.yard.b/self.yard.grid_size) + 1

		self.rings = {}
		for i in range(0, rings):
			self.rings[i] = []

	def eval_rings(self):
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

		return sensors

	def execute(self, panda_x, panda_y):
		panda_ring = self.eval_rings()
		packet = Packet()

		d0 = sqrt(self.yard.energy.free_space / self.yard.energy.multi_path)

		packet = Packet()
		
		sensors = []
		while self.sense(sensors, panda_x, panda_y):
			cluster_heads = []
			for node in sensors:
				# A cluster head maintains cache, therefore a cluster would trigger ring only once
				if node.cell.head not in cluster_heads:
					cluster_heads.append(node.cell.head)

				if(node.cell.head == node):
					continue
				# ###############################################
				# subtract energy - node to CH
				# ###############################################
				if node.energy > 0 :
					cluster_node = node.send_data_non_ch(self.yard, packet, d0)
					cluster_node.receive_data(yard, packet)

			rings = []
			for head in cluster_heads:
				# Panda detected from different cluster, can belong to same ring or other
				rings.append(head.ring)

			for ring in self.rings:
				for cell in self.rings[ring]:
					# print cell.head.id
					if cell.energy > 0:
						dis_clockwise = maxd
						dis_anticlockwise = maxd
						Sx = cell.x
						Sy = cell.y
						Ex = self.yard.sink.x
						Ey = self.yard.sink.y
						for node in self.rings[ring] :
							if node.energy > 0 :
								#clockwise
								if (node.y - Sy)*(Ex - Sx) > (node.x - Sx)*(Ey - Sy) :
									distance = dis(node.x, node.y, Sx, Sy)
									if dis_clockwise > distance :
										node_clockwise = node
								
								# anticlockwise
								else :
									distance = dis(node.x, node.y, Sx, Sy)
									if dis_anticlockwise > distance :
										node_anticlockwise = node
						cell.send_data_ch(self.yard, packet, d0)
						node_clockwise.receive_data(yard, packet)
						node_anticlockwise.receive_data(yard, packet)

			self.yard.clusterize()


