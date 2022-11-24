import matplotlib.pyplot as plt
import pickle
import numpy as np

with open('outDict.pickle', 'rb') as f:
    loaded_obj = pickle.load(f)

avgs = loaded_obj['avgs']
stds = loaded_obj['stds']
allAvgs = loaded_obj['allAvgs']
allStds = loaded_obj['allStds']
freqs = loaded_obj['freqs']
seshNames = ['Pre', 'Post', 'Late']
types = ['eeg', 'pulse', 'acc', 'gyro']
ch_names = loaded_obj['ch_names']

fig, axs = plt.subplots(1,3)
for isesh in range(3):
	axs[isesh].plot(freqs[1:50], avgs[isesh])
	for ichan in range(11):
		axs[isesh].fill_between(freqs[1:50], avgs[isesh][:, ichan]-stds[isesh][:, ichan], avgs[isesh][:, ichan]+stds[isesh][:, ichan], alpha=0.2)

	axs[isesh].set_xlabel('Frequency (Hz)')
	axs[isesh].set_ylabel('Power (uV^2)')
	title = 'Session:' + seshNames[isesh]
	axs[isesh].set_title(title)

axs[2].legend(ch_names, loc=7)
plt.show()

titles = ['Pre-Post', 'Pre-Late', 'Post-Late']
fig, axs = plt.subplots(4,3)
for icomp in range(3):
    axs[0,icomp].plot(freqs[1:50], allAvgs[icomp][:,0:4])
    axs[1,icomp].plot(freqs[1:50], allAvgs[icomp][:,4:5])
    axs[2,icomp].plot(freqs[1:50], allAvgs[icomp][:,5:8])
    axs[3,icomp].plot(freqs[1:50], allAvgs[icomp][:,8:11])

    for ichan in range(0,4):
        axs[0,icomp].fill_between(freqs[1:50], allAvgs[icomp][:, ichan]-allStds[icomp][:, ichan], allAvgs[icomp][:, ichan] + allStds[icomp][:, ichan], alpha=0.2)
    for ichan in range(4,5):
        axs[1,icomp].fill_between(freqs[1:50], allAvgs[icomp][:, ichan]-allStds[icomp][:, ichan], allAvgs[icomp][:, ichan] + allStds[icomp][:, ichan], alpha=0.2)
    for ichan in range(5,8):
        axs[2,icomp].fill_between(freqs[1:50], allAvgs[icomp][:, ichan]-allStds[icomp][:, ichan], allAvgs[icomp][:, ichan] + allStds[icomp][:, ichan], alpha=0.2)
    for ichan in range(8,11):
        axs[3,icomp].fill_between(freqs[1:50], allAvgs[icomp][:, ichan]-allStds[icomp][:, ichan], allAvgs[icomp][:, ichan] + allStds[icomp][:, ichan], alpha=0.2)

    axs[0,icomp].set_ylim([-.1, 1.5])
    axs[0,icomp].set_title(titles[icomp])
    for i in range(4):
        axs[i,icomp].plot([0, freqs[50]], [0, 0], 'k')
        axs[i,icomp].set_ylim([-.5, 1.5])
        if icomp == 0:
            axs[i,icomp].set_ylabel(types[i])

axs[0,2].legend(ch_names[0:4])
axs[1,2].legend(ch_names[4:5])
axs[2,2].legend(ch_names[5:8])
axs[3,2].legend(ch_names[8:11])

plt.show()