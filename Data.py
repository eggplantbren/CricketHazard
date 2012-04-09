import numpy as np

"""
An object of this class is a single player's career.
Just a chronological list of integer scores and 
boolean flags for out (True)/not out (False).
"""
class Career:
	"""
	Constructor: just sets scores and outFlags to
	empty arrays.
	"""
	def __init__(self):
		self.clear()
	
	"""
	Set scores and outFlags to empty arrays.
	"""
	def clear(self):
		self.scores = np.array([])
		self.outFlags = np.array([])

	"""
	Load from file. Parses * notation for not-outs.
	"""
	def load(self, filename):
		scores = []
		outFlags = []
		f = open(filename, "r")
		lines = f.readlines()
		for line in lines:
			line = line.strip()
			if len(line) > 0:
				if line[-1] == "*":
					outFlags.append(False)
					line = line[0:(len(line)-1)]
				else:
					outFlags.append(True)
				scores.append(int(line))
		self.scores = np.array(scores)
		self.outFlags = np.array(outFlags)

	"""
	Turn a single innings to a string.
	"""
	def toString(self, i):
		result = `self.scores[i]`
		if not self.outFlags[i]:
			result += '*'
		return result

	"""
	Convert a whole career to a string.
	"""
	def __str__(self):
		return ''.join([self.toString(i) + ' ' for i in xrange(0, self.scores.size)])


"""
Simple main, for testing
"""
if __name__ == '__main__':
	data = Career()
	data.load("fake_data.txt")
	print(data)

