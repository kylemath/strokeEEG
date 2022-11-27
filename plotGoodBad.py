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

fig, axs = plt.subplots(1,3)
for idx in range(3):
    print(idx)
    axs[idx].plot(freqs[1:50], avgs[idx*2])
    axs[idx].plot(freqs[1:50], avgs[idx*2+1])
    axs[idx].plot([0, freqs[50]], [0, 0], 'k')

    axs[idx].fill_between(freqs[1:50], avgs[idx*2]-stds[idx*2], avgs[idx*2]+stds[idx*2], alpha=0.2)
    axs[idx].fill_between(freqs[1:50], avgs[idx*2+1]-stds[idx*2+1], avgs[idx*2+1]+stds[idx*2+1], alpha=0.2)

    axs[idx].set_xlabel('Frequency (Hz)')
    if idx == 0:
        axs[idx].set_ylabel('Good - Bad Hemisphere Power (uV^2)')

    axs[idx].legend(['Temporal', 'Frontal'])

    title = 'Session:' + seshNames[idx]
    axs[idx].set_title(title)
    axs[idx].set_ylim([-.20, .25])
plt.show()