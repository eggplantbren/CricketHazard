import numpy as np
import numpy.random as rng

class HazardModel:
	"""
	An object of this class is a point in the parameter
	space of hazard models.
	"""

	# A static variable, the x-axis
	x = np.arange(0, 500)

	def __init__(self, mu0=40.0, mu1=40.0, L=5.0):
		"""
		Can pass in values for the
		parameters, otherwise sensible defaults are used.
		"""
		self.mu0, self.mu1, self.L = mu0, mu1, L
		self.compute()

	def fromPrior(self):
		"""
		Draw the parameters from the prior. Currently using
		an ignorant prior.
		"""
		self.mu0 = np.exp(np.log(1.0) + np.log(1E2)*rng.rand())
		self.mu1 = np.exp(np.log(1.0) + np.log(1E2)*rng.rand())
		if self.mu1 < self.mu0:
			self.mu0, self.mu1 = self.mu1, self.mu0
		self.L = np.exp(np.log(0.1) + np.log(1E3)*rng.rand())
		self.compute()

	def compute(self):
		"""
		Compute various properties 
		"""
		# Effective average
		self.mu = self.mu1 + (self.mu0 - self.mu1)*\
		np.exp(-HazardModel.x/self.L)
		# Log of reversed cumulative distribution
		self.logG = np.zeros(HazardModel.x.shape)
		self.logG[1:] = np.cumsum(np.log(self.mu[0:-1])\
				 - np.log(self.mu[0:-1] + 1.0))
		# Log of probability distribution
		self.logf = self.logG - np.log(self.mu + 1.0)
		# Numerically compute actual average
		# Note: can be underestimated due to range of HazardModel.x!
		self.average = np.sum(HazardModel.x*np.exp(self.logf))

	def __str__(self):
		return str(self.mu0) + " " + str(self.mu1) + " " + str(self.L)
		

if __name__ == '__main__':
	"""
	A simple main for testing
	"""
	import matplotlib.pyplot as plt
	import time

	m = HazardModel()

	plt.ion()
	plt.hold(False)
	for i in xrange(0, 100):
		m.fromPrior()
		plt.plot(HazardModel.x, m.mu)
		plt.title("Prior over a player's effective average curve")
		plt.axis([0, 100, 0, 100])
		plt.xlabel('Current Score')
		plt.ylabel('Effective Average')
		plt.draw()
		time.sleep(0.5)
	plt.ioff()
	plt.show()

