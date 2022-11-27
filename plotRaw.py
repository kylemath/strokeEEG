import pandas as pd
import matplotlib.pyplot as plt
import mne
import numpy as np
import time
import pickle
pd.options.display.float_format = '{:.9f}'.format

outPSD = []
allSubjectNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
allSubjectNumber = [ 16]

for idx, isub in enumerate(allSubjectNumber):

	substr = str(isub).zfill(2)
	print('______________')
	print('Subject #: ' + substr)
	print('______________')

	fig, axs = plt.subplots(5+3+3, 3, figsize=(20,12))

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

			if (isub == 12) & (isesh == 3): 
				dfs[dataType] = dfs[dataType].astype({'timestamps':'float'})
				if (dataType == 'ACC'):
					dfs[dataType] = dfs[dataType].astype({'x':'float', 'y':'float', 'z':'float'})
				# print(dfs[dataType])

			if (isub == 15) & (isesh == 2): 
				# print(dfs[dataType])
				dfs[dataType] = dfs[dataType].astype({'timestamps':'float'})
				if (dataType == 'GYRO'):
					dfs[dataType] = dfs[dataType].astype({'x':'float', 'y':'float', 'z':'float'})
				# print(dfs[dataType])

			if (isub == 16) & (isesh == 3): 
				# print(dfs[dataType])
				dfs[dataType] = dfs[dataType].astype({'timestamps':'float'})
				if (dataType == 'GYRO'):
					dfs[dataType] = dfs[dataType].astype({'x':'float', 'y':'float', 'z':'float'})
				# print(dfs[dataType])

			if (isub == 17) & (isesh == 1): 
				print(dfs[dataType].columns)
				dfs[dataType] = dfs[dataType].astype({'timestamps':'float'})
				if (dataType == 'EEG'):
					dfs[dataType] = dfs[dataType].astype({'TP9':'float', 'AF7':'float', 'AF8':'float', 'TP10':'float', 'Right AUX':'float'})
				print(dfs[dataType]	)
				# print(dfs[dataType])
			if (isub == 3) & (dataType == 'GYRO') & (isesh == 2):
				dfs[dataType] = dfs[dataType].astype({'X':'float', 'Y':'float', 'Z':'float', 'timestamps':'float', 'Marker0':'float'})

		df = pd.merge_asof(dfs['EEG'], dfs['ACC'], on='timestamps')
		df = pd.merge_asof(df, dfs['GYRO'], on='timestamps')

		# print(df.columns)
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

		if 12 <= isub <= 17:
			srate = 256
		else: 
			srate = round(1/intervals.mean())

		#-----
		# Plot raw data for each subject

		for ind, channel in enumerate(EEGchannels):

			axs[ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
			axs[ind, isesh - 1].set_xlabel('Time (ms)')
			axs[ind, isesh - 1].set_ylabel('Voltage (uV)')
			axs[ind, isesh - 1].set_title(channel)
		for ind, channel in enumerate(ACCchannels):

			axs[len(EEGchannels) + ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
			axs[len(EEGchannels) + ind, isesh - 1].set_xlabel('Time (ms)')
			axs[len(EEGchannels) + ind, isesh - 1].set_ylabel('Voltage (uV)')
			axs[len(EEGchannels) + ind, isesh - 1].set_title(channel)
	
		for ind, channel in enumerate(GYROchannels):
			# if isesh == 2:
			# 	print(df[channel])	
			axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].plot(df['timestamps'], df[channel], 'r-', label=channel)
			axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_xlabel('Time (ms)')
			axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_ylabel('Voltage (uV)')
			axs[len(EEGchannels) + len(ACCchannels) + ind, isesh - 1].set_title(channel)	
	

	plt.suptitle(['subject:', substr])
	plt.show()



