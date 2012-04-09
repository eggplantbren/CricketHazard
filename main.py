import numpy as np
import numpy.random as rng
import matplotlib.pyplot as plt
import copy
from Data import *
from HazardModel import *

def logLikelihood(career, model):
	"""
	Evaluate log p(career|hazard model)
	"""

	"""
	# Slow, loopy method
	logL = 0.0
	for i in xrange(0, career.scores.size):
		if career.outFlags[i]:
			logL += model.logf[career.scores[i]]
		else:
			logL += model.logG[career.scores[i]]
	"""

	# Vectorised - faster
	logLEachInnings = np.zeros(career.scores.size)
	logLEachInnings[career.outFlags] = model.logf[career.scores]
	logLEachInnings[np.logical_not(career.outFlags)] = model.logG[career.scores]
	logL = logLEachInnings.sum()
	return logL

if __name__ == "__main__":
	"""
	Do the inference for a single player.
	"""

	filename = "Data/lara.txt"
	data = Career()
	data.load(filename)

	# MCMC parameters. One step = one likelihood evaluation
	numParticles = 10
	steps = 1000000
	skip = 100

	# Keep track of acceptance rates
	accepts = np.array([0, 0]) # Acceptances for basic Metropolis and 
				   # stretch moves respectively
	tries = np.array([0, 0])   # As above, number of attempts

	# Array for keeping results
	keep = np.zeros((steps/skip, 5))

	# Initialise particles and their log likelihoods
	particles = []
	logLikelihoods = []
	for i in xrange(0, numParticles):
		p = HazardModel()
		p.fromPrior()
		particles.append(p)
		logLikelihoods.append(logLikelihood(data, p))

	# Labels for plotting
	labels = ["Initial ability", "Final ability",\
		 "Transition timescale", "Overall average", "Log likelihood"]

	# Open output file
	outputFile = open("sample.txt", mode="w")
	# Write header
	outputFile.write("# ")
	for label in labels:
		outputFile.write(label + ", ")
	outputFile.write("\n")

	plt.ion()
	plt.subplots(3, 2, figsize=(12, 12))
	for i in xrange(0, steps):
		# Choose a particle for plotting/updating
		which = rng.randint(numParticles)

		# Plotting/saving
		if i%skip == 0:
			# Save a particle to the keep array
			keep[i/skip, :] = np.array([particles[which].mu0\
		, particles[which].mu1, particles[which].L\
		, particles[which].average\
		, logLikelihoods[which]])
			line = str(keep[i/skip, :])
			line = line.replace("[", "")
			line = line.replace("]", "")
			line = line.replace("\n", "")
			outputFile.write(line + "\n")
			outputFile.flush()

			# Plot last 75% of keep array
			# (removing burn-in in an ad-hoc way)
			for k in xrange(0, len(labels)):
				plt.subplot(3,2,k+1)
				plt.hold(False)
				start = int(0.25*(i/skip+1))
				plt.plot(keep[start:(i/skip+1), k])
				plt.xlabel("Iteration")
				plt.ylabel(labels[k])
			plt.draw()
			print("Acceptance fractions = "\
			+ str(np.float64(accepts)/(tries+1)))

		# Update the particle
		proposal = copy.deepcopy(particles[which])
		method = rng.randint(2)
		if method == 0:
			# Plain metropolis
			logH = proposal.proposal()
		else:
			# Stretch move
			other = rng.randint(numParticles)
			while other == which:
				other = rng.randint(numParticles)
			logH = proposal.proposal(particles[other])
		tries[method] += 1

		loglProposal = logLikelihood(data, proposal)

		# Acceptance probability
		logA = loglProposal - logLikelihoods[which] + logH
		if logA > 0.0:
			logA = 0.0
		if rng.rand() <= np.exp(logA):
			particles[which] = proposal
			logLikelihoods[which] = loglProposal
			accepts[method] += 1

	outputFile.close()

	plt.ioff()
	plt.show()

