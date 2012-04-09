import numpy as np
import numpy.random as rng


class HazardModel:
	"""
	An object of this class is a point in the parameter
	space of hazard models.
	"""

	# A static variable, the x-axis
	x = np.arange(0, 1000)

	# Hyperparameters
	logMuMin = np.log(1.0)
	logMuMax = np.log(1E2)
	logMuRange = logMuMax - logMuMin
	logLMin = np.log(0.1)
	logLMax = np.log(1E2)
	logLRange = logLMax - logLMin

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
		self.mu0 = np.exp(HazardModel.logMuMin\
				 + HazardModel.logMuRange*rng.rand())
		self.mu1 = np.exp(HazardModel.logMuMin\
				 + HazardModel.logMuRange*rng.rand())
		self.L = np.exp(HazardModel.logLMin\
				 + HazardModel.logLRange*rng.rand())
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

	def proposal(self, other=None):
		"""
		Proposal for Metropolis-Hastings updates.
		Prior should be implicit in this.
		Return value: log of a hastings factor.
		Optional argument: another object, to do a stretch move
		"""

		logH = 0.0
		if other == None:
			# Standard Metropolis proposal
			which = rng.randint(3)
			if which==0:
				param = self.mu0
				lower = HazardModel.logMuMin
				scale = HazardModel.logMuRange
			elif which==1:
				param = self.mu1
				lower = HazardModel.logMuMin
				scale = HazardModel.logMuRange
			else:
				param = self.L
				lower = HazardModel.logLMin
				scale = HazardModel.logLRange

			param = np.log(param)
			param += scale*10.0**(1.5 - 6.0*rng.rand())\
					*rng.randn()
			param = np.mod(param - lower, scale) + lower
			param = np.exp(param)

			if which==0:
				self.mu0 = param
			elif which==1:
				self.mu1 = param
			else:
				self.L = param
			
				
		else:
			# Slight inefficiency (not cached), shouldn't matter
			logp_old = self.logPrior
		
			# Stretch move
			Z = 0.5*(1.0 + rng.rand())**2
			self.mu0 = Z*self.mu0 + (1.0 - Z)*other.mu0
			self.mu1 = Z*self.mu1 + (1.0 - Z)*other.mu1
			self.L = Z*self.L + (1.0 - Z)*other.L

			logp_new = self.logPrior
			if logp_new == -np.inf:
				logH = -np.inf
			else:
				logH += 2*np.log(Z) # (N-1)logZ
				logH += logp_new - logp_old

		if logH != -np.inf:
			self.compute()
		return logH

	@property
	def logPrior(self):
		""" Evaluate the prior density at the current point.
		Stretch moves need this."""
		if self.mu0 < np.exp(HazardModel.logMuMin)\
		or self.mu0 > np.exp(HazardModel.logMuMax)\
		or self.mu1 < np.exp(HazardModel.logMuMin)\
		or self.mu1 > np.exp(HazardModel.logMuMax)\
		or self.L   < np.exp(HazardModel.logLMin) \
		or self.L   > np.exp(HazardModel.logLMax):
			return -np.inf
		return 0.0

	def __str__(self):
		"""
		Turns the parameters into a string.
		"""
		return str(self.mu0) + " " + str(self.mu1) + " " + str(self.L)
		

if __name__ == '__main__':
	"""
	A simple main for testing
	Explores the prior via stretch moves
	"""
	import matplotlib.pyplot as plt
	import time
	import copy

	# Create particles
	numParticles = 10
	particles = []
	for i in xrange(0, numParticles):
		m = HazardModel()
		m.fromPrior()
		particles.append(m)

	plt.ion()
	plt.hold(False)
	for i in xrange(0, 100):
		# Update one using stretch move
		which = rng.randint(numParticles)
		other = rng.randint(numParticles)
		while which==other:
			other = rng.randint(numParticles)
		proposal = copy.deepcopy(particles[which])
		logA = proposal.proposal(particles[other])
		if rng.rand() <= np.exp(logA):
			particles[which] = proposal

		plt.plot(HazardModel.x, particles[which].mu)
		plt.title("Prior over a player's effective average curve")
		plt.axis([0, 100, 0, 100])
		plt.xlabel('Current Score')
		plt.ylabel('Effective Average')
		plt.draw()
		#time.sleep(0.5)
	plt.ioff()
	plt.show()

