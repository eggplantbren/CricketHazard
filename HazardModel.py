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
	logMuMax = np.log(2E2)
	logMuRange = logMuMax - logMuMin
	logLMin = np.log(0.1)
	logLMax = np.log(50.0)
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

	def logPrior(self):
		logP = 0.

		# Lognormal priors
		logP += -np.log(self.mu0) - 0.5*((np.log(self.mu0) - np.log(30.))/0.5)**2
		logP += -np.log(self.mu1) - 0.5*((np.log(self.mu1) - np.log(30.))/0.5)**2

		return logP

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

	def proposal(self):
		"""
		Proposal for Metropolis-Hastings updates.
		Prior should be implicit in this.
		Return value: log of a hastings factor.
		Optional argument: another object, to do a stretch move
		"""

		logH = -self.logPrior()

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
		param += scale*10.0**(1.5 - 3.0*rng.rand())\
				*rng.randn()
		param = np.mod(param - lower, scale) + lower
		param = np.exp(param)

		if which==0:
			self.mu0 = param
		elif which==1:
			self.mu1 = param
		else:
			self.L = param

		logH += self.logPrior()
		
		self.compute()
		return logH

	def __str__(self):
		"""
		Turns the parameters into a string.
		"""
		return str(self.mu0) + " " + str(self.mu1) + " " + str(self.L)

