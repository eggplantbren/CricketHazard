class Data:
	def __init__(self):
		self.clear()
	
	def clear(self):
		self.scores = []
		self.outFlags = []

	def load(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		for line in lines:
			line = line.strip()
			print(line)
			if len(line) > 0:
				if line[-1] == "*":
					self.outFlags.append(False)
					line = line[0:(len(line)-1)]
				else:
					self.outFlags.append(True)
				self.scores.append(int(line))
		print self.scores
		print self.outFlags


if __name__ == '__main__':
	data = Data()
	data.load("fake_data.txt")

