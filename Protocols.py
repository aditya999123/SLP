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

				self.rings[max(d_x, d_y)].append(cell)

		# need to rethink this
		# self.rings[0] = [self.yard.sink.cell]

		for x, cells in self.rings.items():
			print x, [cell.head.id for cell in cells]

	def sense(self, cluster_heads, panda_x, panda_y):
		sensor_range = sqrt(5)*self.yard.grid_size
		
		for sensor_node in self.yard.nodes:
			if (sensor_node.energy > 0
				and dist(sensor_node.x, sensor_node.y, panda_x, panda_y) <= sensor_range
				and sensor_node.cell.head not in cluster_heads
				):
				
				cluster_heads.append(sensor_node.cell.head)

		return cluster_heads

	def execute(self, panda_x, panda_y) :
		panda_ring = self.eval_rings()
		packet = Packet()

		d0 = sqrt(self.yard.energy.free_space / self.yard.energy.multi_path)

		cluster_heads = []
		while self.sense(cluster_heads, panda_x, panda_y):
			for head in cluster_heads:
				pass
			print cluster_heads
			break

	
	def execute2(self, panda_x, panda_y):
		num_cluster = 0
		num_nodes = 0
		
		for node in self.yard.nodes:
			num_nodes += 1
			if node.is_cluster_head == True :
				num_cluster += 1


		for sensor_node in self.yard.ring[panda_ring_no] :
			# alive nodes
			if sensor_node.energy > 0 :
				# determining the energy of Non-CH Nodes
				if sensor_node.is_cluster_head == False :					
					distance = dist(sensor_node.x, sensor_node.y, panda_x, panda_y)
					source_factor = 1
					if distance <= comm_range :
						sensor_node_factor = 2

					min_dis = maxd

					# determining nearest cluster_node
					for node in self.yard.nodes :
						if node.is_cluster_head == True :
							distance = dist(sensor_node.x, sensor_node.y, node.x, node.y)
							if min_dis > distance :
								min_dis = distance
								cluster_node = node

					# total energy dissipitated for transmission
					if min_dis > d0 :
						sensor_node.energy = sensor_node.energy - source_factor*(ctr_packet_length*trans + multi_path*packet_length*(min_dis ** 4)) 
					else :
						sensor_node.energy = sensor_node.energy - source_factor*(ctr_packet_length*trans + free_space*packet_length*(min_dis ** 4)) 
					
					# total energy dissipitated while receiving packets
					if cluster_node.energy > 0 :
						cluster_node.energy = cluster_node.energy - (rec + data_aggr)*packet_length

				# determining the energy of CH Nodes
				else :
					distance = dist(sensor_node.x, sensor_node.y, self.yard.sink.x, self.yard.sink.y)
					
					# total energy dissipitated for transmission + data aggregation
					if distance >= d0 :
						sensor_node.energy = sensor_node.energy - ((trans + data_aggr)*packet_length + multi_path*packet_length*(distance ** 4))
					else :
						sensor_node.energy = sensor_node.energy - ((trans + data_aggr)*packet_length + free_space*packet_length*(distance ** 4)) 

					# total energy dissipitated while receiving packets 
					sensor_node.energy = sensor_node.energy - rec*ctr_packet_length*(round(num_nodes/num_cluster))

		# for node in self.yard.ring[panda_ring_no] :
		# 	print node.energy, node.is_cluster_head


