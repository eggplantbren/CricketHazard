import numpy as np

class Career:
	"""
	An object of this class is a single player's career.
	Just a chronological array of integer scores and 
	boolean flags for out (True)/not out (False).
	"""

	def __init__(self):
		"""
		Constructor: just sets scores and outFlags to
		empty arrays.
		"""
		self.clear()
	
	def clear(self):
		"""
		Set scores and outFlags to empty arrays.
		"""
		self.scores = np.array([])
		self.outFlags = np.array([])

	def load(self, filename):
		"""
		Load from file. Parses * notation for not-outs.
		"""
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

	def fetch(self,playerID=8180):
		"""Fetch a player's batting record from ESPN and
		parse it into the Career instance.

		Defaults to Shane 'Watto' Watson."""

		from bs4 import BeautifulSoup
		from urllib2 import urlopen

		# Fetch webpage data
		pre = 'http://stats.espncricinfo.com/ci/engine/player/'
		post = '.html?class=1;template=results;type=batting;view=innings'
		webstr = pre + str(playerID) + post
		soup = BeautifulSoup(urlopen(webstr))

		return

	def toString(self, i):
		"""
		Turn a single innings to a string.
		"""
		result = str(self.scores[i])
		if not self.outFlags[i]:
			result += '*'
		return result

	def __str__(self):
		"""
		Convert a whole career to a string.
		"""
		return ''.join([self.toString(i) + ' ' for i in xrange(0, self.scores.size)])


class Population:
	"""
	Simply a list of Careers
	"""

	def __init__(self):
		"""
		Constructor: empty list
		"""
		self.careers = []

	def load(self, filenames):
		"""
		Load a bunch of careers from the specified files.
		`filenames`: list of strings
		"""
		for filename in filenames:
			c = Career()
			c.load(filename)
			self.careers.append(c)

	def __str__(self):
		"""
		Output one player's career per line.
		"""
		return ''.join([str(career) + '\n' for career in self.careers])

def get_playerID(name='Ponting'):
	"""Search ESPN database by name and return possible
	player IDs.
	
	This routine is not implemented at present, so
	one must manually search the ESPN website and input
	the ID to Career.fetch by hand."""
	return

if __name__ == '__main__':
	"""
	Simple main, for testing
	"""
	data = Population()
	data.load(["fake_data.txt"])
	print(data)

