from math import sqrt
from helpers import dist, colour

class Node:
	total_nodes = 0 # Static variable of the class, used as a counter
	
	def __init__(self, x, y, energy, cell):
		self.id = Node.total_nodes # unique id for each node
		Node.total_nodes += 1
		self.x = x
		self.y = y

		self.energy = energy

		# Assigning this node to a cell on the grid
		self.cell = cell

		self.is_cluster_head = False

	def send_data_non_ch(self, energy, packet):
		d0 = sqrt(energy.free_space / energy.multi_path)
		
		# distance of sensor to its CH
		d = dist(self.x, self.y, self.cell.head.x, self.cell.head.y)

		if d > d0 :
			self.energy = self.energy - (packet.ctr_packet_length*energy.trans + energy.multi_path*packet.packet_length*(d ** 4)) 
		else :
			self.energy = self.energy - (packet.ctr_packet_length*energy.trans + energy.free_space*packet.packet_length*(d ** 2)) 				


	def send_data_ch(self, energy, packet, distance):
		d0 = sqrt(energy.free_space / energy.multi_path)

		if distance >= d0 :
			self.energy = self.energy - 2*((energy.trans + energy.data_aggr)*packet.packet_length + energy.multi_path*packet.packet_length*(distance ** 4))
		else :
			self.energy = self.energy - 2*((energy.trans + energy.data_aggr)*packet.packet_length + energy.free_space*packet.packet_length*(distance ** 2)) 
		

	def receive_data(self, energy, packet):
		self.energy = self.energy - (energy.rec + energy.data_aggr) * packet.packet_length


	def __str__(self):
		return "x = %d, y = %d, id = %d" % (self.x, self.y, self.id)

	# Mark as a cluster head
	def make_cluster_head(self):
		self.is_cluster_head = True

	# This node has head_id as its cluster head
	def has_head(self):
		self.is_cluster_head = False
