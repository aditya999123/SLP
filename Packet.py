class Packet:
	def __init__(self, packet_length = 4000, ctr_packet_length = 4000, dummy_packet_length = 4000):
		self.packet_length = packet_length
		self.ctr_packet_length = ctr_packet_length
		self.dummy_packet_length = dummy_packet_length
