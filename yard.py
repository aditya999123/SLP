from nodes import Node
from math import sqrt
from helpers import dist, colour

import matplotlib.pyplot as plt 
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

		# energy for Data Aggregation 
		self.data_aggr = 5*0.000000001
		if kwargs.get('data_aggr'):
			self.data_aggr = kwargs['data_aggr']

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
	rings = 10
	def __init__(self, l = 100, b = 100, *args, **kwargs):
		self.l = l # length of the yard
		self.b = b # breadth of the yard
		
		self.nodes = []
		self.energy = Energy(kwargs) # initialize all values for energy calculations
		self.grid_side_length = 20
		if kwargs.get('grid_side_length'):
			self.grid_side_length = kwargs['grid_side_length']

		# 1st node with id = 0 is used as sink, initially placed at center
		self.sink = Node(self.l/2, self.b/2, self.energy.init)
		
		self.ring = {
		}
		
		for i in range(1, Yard.rings+1):
			self.ring[i] = []


	# modify location of the sink
	def modify_sink_location(self, x, y):
		self.sink.x = x
		self.sink.y = y


	# populate the yard with num nodes at random locations with initial energy
	def populate(self, num):
		for i in range(num):
			
			x = random.randint(0, self.l)
			y = random.randint(0, self.b)

			self.nodes.append(Node(x, y, self.energy.init, self.grid_side_length))


	# determining ring numbers to the corressponding nodes
	def evaluate(self, panda_x, panda_y):

		maxd = dist(0, 0, self.l, self.b)
		ring_size = int(maxd/Yard.rings);

		for node in self.nodes:
			ring_no = round((dist(node.x, node.y, self.sink.x, self.sink.y) + ring_size - 1)/ring_size)

			self.ring[ring_no].append(node)

		self.show_rings_on_graph(panda_x, panda_y)

		# determining the event ring
		panda_ring_no = round((dist(panda_x, panda_y, self.sink.x, self.sink.y) + ring_size - 1)/ring_size);
		
		print (panda_ring_no)


	# show nodes on rings
	def show_rings_on_graph(self, panda_x, panda_y):
		
		for ring_no, nodes in self.ring.items():
			x = []
			y = []

			for node in nodes:
				x.append(node.x)
				y.append(node.y)

			plt.scatter(x, y, label = "ring %d" % ring_no, color= colour[ring_no], marker= "*", s=30)


		# show sink on graph
		x = [self.sink.x]
		y = [self.sink.y]

		plt.scatter(x, y, label = "sink", color = 'black', marker = "s", s=30)

		#plot panda
		x = [panda_x]
		y = [panda_y]

		plt.scatter(x, y, label = "panda", color = 'purple', marker = "X", s=60)
		plt.legend()
		
		plt.grid(True)
		plt.show()


	# determining Cluster Heads
	def clustering(self):
		l = self.l
		b = self.b
		g = self.grid_side_length
		num_grid = (l*b)/(g*g)
		num_col = l/g
		num_row = b/g
		num_grid += 1
		cluster_heads = [[0,0] for _ in range(num_grid)]

		# determining the cluster head in a grid on the basis of max energy
		for node in self.nodes :
			grid_id = node.grid['row_num']*num_col + node.grid['col_num']
			if cluster_heads[grid_id][0] < node.energy :
				cluster_heads[grid_id][0] = node.energy
				cluster_heads[grid_id][1] = node.id

		# assigning corressponding Cluster Head to all the Nodes
		for node in self.nodes:
			grid_id = node.grid['row_num']*num_col + node.grid['col_num']
			head = cluster_heads[grid_id][1]
			node.has_head(head)
			if cluster_heads[grid_id][1] == node.id :
				node.make_cluster_head()
		# for node in self.nodes:
		# 	print node.is_cluster_head


class Packet:
	
	def __init__(self, packet_length = 4000, ctr_packet_length = 4000, dummy_packet_length = 4000):
		self.packet_length = packet_length
		self.ctr_packet_length = ctr_packet_length
		self.dummy_packet_length = dummy_packet_length
