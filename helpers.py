from math import sqrt

colour = ['green', 'grey', 'indigo', 'khaki', 'lavender', 'olive', 'orange', 'wheat', 'ivory', 'plum', 'salmon', 'yellow']


def dist(x, y, a, b):
	return sqrt((x-a) * (x-a) + (y-b) * (y-b))