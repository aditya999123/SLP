class Sink:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "sink: x = %d, y = %d" % (self.x, self.y)