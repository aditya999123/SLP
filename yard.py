from nodes import Sink

class Yard:
	def __init__(self, x = 100, y = 100):
		self.x = x
		self.y = y
		self.sink = Sink(x/2, y/2)

	def sink_modify(self, x, y):
		self.sink.x = x
		self.sink.y = y