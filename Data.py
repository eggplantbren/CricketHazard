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

	def fetch(self,playerID=8180,record_class=1):
		"""Fetch a player's ODI batting record from ESPN and
		parse it into the Career instance.

		Input: playerID on cricinfo (can be found with search_playerID)
		       record_class: Test (default), ODI, T20, combined

		Defaults to the Test record of Shane 'Watto' Watson."""

		try:
			from bs4 import BeautifulSoup
			from urllib2 import urlopen
		except ImportError:
			print("You require beautifulsoup4 to do this.")
			return

		# Select class of batting data
		if type(record_class)==str:
			if record_class.lower() == 'test':
				record_class = 1
			elif record_class.lower() == 'odi':
				record_class = 2
			elif record_class.lower() == 't20':
				record_class = 3
			elif record_class.lower() == 'all':
				record_class = 11
			else:
				print "Can't parse batting record class. Defaulting to Test."
				record_class = 1
		elif type(record_class)==int:
			if record_class not in [1,2,3,11]:
				print "Can't parse batting record class. Defaulting to Test."
				record_class = 1
		else:
			print "Can't parse batting record class. Defaulting to Test."
			record_class = 1


		# Fetch webpage data
		pre = 'http://stats.espncricinfo.com/ci/engine/player/'
		post1 = '.html?class='
		post2 = ';template=results;type=batting;view=innings'
		webstr = pre + str(playerID) + post1 + str(record_class) + post2
		soup = BeautifulSoup(urlopen(webstr))

		# Get full innings list, including DNBs
		innings_table = soup('table','engineTable')[3] # Get innings table
		innings_rows = innings_table('tr')[1:] # Cut header row
		innings_list = [innings('td')[0].text for innings in innings_rows]

		# Chop DNBs
		batting_list = [score for score in innings_list if 'DNB' not in score] # :-)

		# Find not-outs
		self.outFlags = np.array( ['*' not in s for s in batting_list] )

		# Strip '*' from not out scores and set score list
		self.scores = np.array( [int(score.strip('*')) for score in batting_list] )
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

def search_playerID(name='Ponting',output=True,returndict=False):
	"""Search ESPN database by name and return possible
	player IDs.
	"""
	try:
		from bs4 import BeautifulSoup
		from urllib2 import urlopen
	except ImportError:
		print("You require beautifulsoup4 to do this.")
		return
		
	# Fetch result from web
	pre = 'http://stats.espncricinfo.com/ci/engine/stats/analysis.html?search='
	search_str = pre + name
	soup = BeautifulSoup( urlopen(search_str) )

	# Parse result data into names and IDs
	searchdiv = soup('div',id='gurusearch_player')
	player_entries = searchdiv[0]('tr')[0::2]
	names = [' '.join([str(s.text) for s in entry('span')]) for entry in player_entries]
	ids = [int(entry('a')[0].attrs['href'].split('.')[0].split('/')[-1]) for entry in player_entries]
	
	# Print formatted list
	if output:
		print "{0:>6} {1:<25}".format("ID","Name")
		for i in range(len(names)):
			print "{0:>6} {1:<25}".format(ids[i],names[i])
	if returndict:
		return dict(zip(ids,names))
	else:
		return

if __name__ == '__main__':
	"""
	Simple main, for testing
	"""
	data = Population()
	data.load(["fake_data.txt"])
	print(data)

