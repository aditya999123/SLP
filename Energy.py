class Energy:
	def __init__(self, kwargs):
		# initial energy of each node
		self.init = kwargs.get('init', 0.5)

		# energy for transferring of each bit 
		self.trans = kwargs.get('trans', 50*0.000000001)

		# energy for receiving of each bit 
		self.rec = kwargs.get('rec', 50*0.000000001)

		# energy for Data Aggregation 
		self.data_aggr = kwargs.get('data_aggr', 5*0.000000001)

		# energy for free space model
		self.free_space = kwargs.get('free_space', 10*0.000000000001)

		# energy for multi path model
		self.multi_path =  kwargs.get('multi_path', 0.0013*0.000000000001)

		# data aggregation energy
		self.aggr = kwargs.get('aggr', 5*0.000000001)

	def __str__(self):
		response = ""
		response += "init = %.1E\n" % self.init
		response += "trans = %.1E\n" % self.trans
		response += "rec = %.1E\n" % self.rec
		response += "free_space = %.1E\n" % self.free_space
		response += "multi_path = %.1E\n" % self.multi_path
		response += "aggr = %.1E\n" % self.aggr

		return response