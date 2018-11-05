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

	def send_data_non_ch(self, yard, packet, d0):
		
		# determining nearest cluster_node
		min_dis = sqrt((yard.l)**2 + (yard.b)**2)
		for node in yard.nodes :
			if node.is_cluster_head == True :
				distance = dist(self.x, self.y, node.x, node.y)
				if min_dis > distance :
					min_dis = distance
					cluster_node = node

		if min_dis > d0 :
			self.energy = self.energy - (packet.ctr_packet_length*yard.energy.trans + yard.energy.multi_path*packet.packet_length*(min_dis ** 4)) 
		else :
			self.energy = self.energy - (packet.ctr_packet_length*yard.energy.trans + yard.energy.free_space*packet.packet_length*(min_dis ** 2)) 
		
		return cluster_node				


	def send_data_ch(self, yard, packet, d0):
		distance = dist(self.x, self.y, yard.sink.x, yard.sink.y)
		if distance >= d0 :
			self.energy = self.energy - 2*((yard.energy.trans + yard.energy.data_aggr)*packet.packet_length + yard.energy.multi_path*packet.packet_length*(distance ** 4))
		else :
			self.energy = self.energy - 2*((yard.energy.trans + yard.energy.data_aggr)*packet.packet_length + yard.energy.free_space*packet.packet_length*(distance ** 2)) 
		

	def recieve_data(self, yard, packet):
		self.energy = self.energy - (yard.energy.rec + yard.energy.data_aggr)*packet.packet_length


	def __str__(self):
		return "x = %d, y = %d" % (self.x, self.y)

	# Mark as a cluster head
	def make_cluster_head(self):
		self.is_cluster_head = True

	# This node has head_id as its cluster head
	def has_head(self):
		self.is_cluster_head = False
