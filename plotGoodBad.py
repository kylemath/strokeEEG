import matplotlib.pyplot as plt
import pickle
import numpy as np

with open('outDictGoodBad.pickle', 'rb') as f:
    loaded_obj = pickle.load(f)

avgs = loaded_obj['avgs']
stds = loaded_obj['stds']
freqs = loaded_obj['freqs']
seshNames = ['Pre', 'Post', 'Late']
types = ['eeg', 'pulse', 'acc', 'gyro']
ch_names = loaded_obj['ch_names']

fig, axs = plt.subplots(1)
for idx, avg in enumerate(avgs):
	axs.plot(freqs[1:50], avgs[idx])
	axs.fill_between(freqs[1:50], avgs[idx]-stds[idx], avgs[idx]+stds[idx], alpha=0.2)

	axs.set_xlabel('Frequency (Hz)')
	axs.set_ylabel('Power (uV^2)')
	# title = 'Session:' + seshNames[isesh]
	# axs[isesh].set_title(title)

axs.plot([0, freqs[50]], [0, 0], 'k')
plt.legend(range(len(avgs*2)))
plt.show()