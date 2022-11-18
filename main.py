import pandas as pd
import matplotlib.pyplot as plt
import mne
import numpy as np
import time
pd.options.display.float_format = '{:.9f}'.format


# for isub in [1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
# missing files = [3, 8, 12, 15, 16, 17, 19]
# 
outPSD = []

for isub in [1, 2, 4, 5, 6, 7, 9, 10, 11, 13, 14, 18, 20, 21, 22, 23, 24, 25, 26, 27]:
	substr = str(isub).zfill(2)
	print('______________')
	print('Subject #: ' + substr)
	print('______________')

	# fig, axs = plt.subplots(5+3+3, 3, figsize=(20,12))

	subPSDs = []
	for isesh in range(1,4):
		print('Session:' + str(isesh))
		dfs = {}
		dataTypes = ['EEG', 'ACC', 'GYRO']
		for dataType in dataTypes:
			print('Reading:' + dataType)
			dfs[dataType] = pd.DataFrame()

			dfs[dataType] = pd.read_csv('./data/Pre_n_post_thrombectomy_studies/ID_'+ substr + '/' + substr + '_' + dataType + '_EVT_' + str(isesh) + '_stroke_study_updated.csv', engine='python')
			dfs[dataType].reset_index(inplace=True)
			if 12 <= isub <= 16:
				dfs[dataType].rename(columns = {'Timestamp (ms)':'timestamps'}, inplace = True)

		df = pd.merge_asof(dfs['EEG'], dfs['ACC'], on='timestamps')
		df = pd.merge_asof(df, dfs['GYRO'], on='timestamps')

		if 12 <= isub <= 16:
			EEGchannels = df.columns[2:7].tolist() #2:7, 9:12, 14:18
			ACCchannels = df.columns[10:13].tolist()
			GYROchannels = df.columns[16:19].tolist()
		else: # 1-11
			EEGchannels = df.columns[2:7].tolist() #2:8, 9:13, 14:18
			ACCchannels = df.columns[9:12].tolist()
			GYROchannels = df.columns[14:17].tolist()
		

		#create mne raw object from arrays
		#info object 
	
		# print(df)
		intervals = df['timestamps'].diff()
		# fig, axs = plt.subplots(1)
		# axs.plot(intervals)
		# plt.show()
		if 12 <= isub <= 16:
			srate = 256
		else: 
			srate = round(1/intervals.mean())
		print(srate)
		ch_names = ['TP9', 'AF7', 'AF8', 'TP10', 'Wrist', 'X_x', 'Y_x', 'Z_x', 'X_y', 'Y_y', 'Z_y']
		ch_types = ['eeg'] * 4 + ['ecg'] + ['bio'] * 6
		info = mne.create_info(ch_names, ch_types=ch_types, sfreq=srate)
		info.set_montage('standard_1020')

		if 12 <= isub <= 16:
			df = df.drop(['index_x', 'timestamps', 'info', 'index_y', 'sequenceId_x', 'Unnamed: 5_x', 'index', 'sequenceId_y', 'Unnamed: 5_y'], axis=1)
		else: 
			df = df.drop(['index_x', 'timestamps',  'Marker0_x', 'index_y', 'Marker0_y', 'index', 'Marker0'], axis=1)
		
		data = df.to_numpy().transpose()/1000000

		rawData = mne.io.RawArray(data, info)
		# rawData.plot(show_scrollbars=True, show_scalebars=True, block=True)
		picks = mne.pick_types(rawData.info, eeg=True, ecg=True,
                       bio=True)

		rawSpectra = rawData.compute_psd(picks=picks)
		psds, freqs = rawSpectra.get_data(return_freqs=True, picks=picks)

		# plot spectra
		# rawSpectra.plot(picks=picks)
		# input("Press Enter to continue...")

		#average over subjects
		print(psds.shape)
		print(len(freqs))

		#plot
		subPSDs.append(psds)

		##-----
		#Plot raw data for each subject

		# for ind, channel in enumerate(EEGchannels):
		# 	axs[ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
		# 	axs[ind, isesh - 1].set_xlabel('Time (ms)')
		# 	axs[ind, isesh - 1].set_ylabel('Voltage (uV)')
		# 	axs[ind, isesh - 1].set_title(channel)
		# for ind, channel in enumerate(ACCchannels):
		# 	axs[len(EEGchannels) + ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
		# 	axs[len(EEGchannels) + ind, isesh - 1].set_xlabel('Time (ms)')
		# 	axs[len(EEGchannels) + ind, isesh - 1].set_ylabel('Voltage (uV)')
		# 	axs[len(EEGchannels) + ind, isesh - 1].set_title(channel)

		# for ind, channel in enumerate(GYROchannels):
		# 	axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
		# 	axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_xlabel('Time (ms)')
		# 	axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_ylabel('Voltage (uV)')
		# 	axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_title(channel)	
	


	outPSD.append(subPSDs)
	

# plt.suptitle(['subject:', substr])
# plt.show()

print(np.shape(outPSD))
npOut = np.array(outPSD)

fig, axs = plt.subplots(3)
for isesh in range(3):
	axs[isesh].plot(freqs[:50], np.log10(npOut[:, isesh, :, :50].mean(axis=0).transpose()))
	axs[isesh].legend(ch_names)
	axs[isesh].set_xlabel('Frequency (Hz)')
	axs[isesh].set_ylabel('Power (uV^2)')
	title = 'Session #:' + str(isesh+1)
	axs[isesh].set_title(title)
plt.show()



