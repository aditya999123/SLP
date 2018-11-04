class Node:
	total_nodes = 0 # Static variable of the class, used as a counter
	def __init__(self, x, y, energy = 0):
		self.id = Node.total_nodes # unique id for each node
		Node.total_nodes += 1
		self.x = x
		self.y = y

		self.energy = energy

		self.is_cluster_head = False
		self.head = -1 # if it is not a cluster head then it should belong to some cluster head

	def send_data(len = 0):
		self.energy -= 0 # will be modified

	def recieve_data(len = 0):
		self.energy -= 0 # will be modified

	def __str__(self):
		return "x = %d, y = %d" % (self.x, self.y)

	# Mark as a cluster head
	def make_cluster_head(self):
		self.is_cluster_head = True
		self.head = -1

	# This node has head_id as its cluster head
	def has_head(head):
		self.is_cluster_head = False
		self.head = head.id