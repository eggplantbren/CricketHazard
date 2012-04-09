"""
Load sample.txt (output from main.py) and make nice plots
"""

import numpy as np
import matplotlib.pyplot as plt

sample = np.atleast_2d(np.loadtxt('sample.txt'))

# Remove burn-in (ad-hoc)
start = int(0.25*sample.shape[0])
sample = sample[start:, :]

plt.figure(figsize=(8,8))
plt.plot(sample[:,0], sample[:,1], 'b.', markersize=1)
plt.plot([0, 100], [0, 100], 'k')
plt.xlabel('$\mu_0$', fontsize=20)
plt.ylabel('$\mu_1$', fontsize=20)
plt.show()

