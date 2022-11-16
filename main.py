import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.9f}'.format


# for isub in [1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
# missing files = [3, 8, 12, 15, 16, 17, 19]
# 
for isub in [1, 2, 4, 5, 6, 7, 9, 10, 11, 13, 14, 18, 20, 21, 22, 23, 24, 25, 26, 27]:	
	substr = str(isub).zfill(2)
	print('______________')
	print('Subject #: ' + substr)
	print('______________')

	fig, axs = plt.subplots(5+3+3, 3, figsize=(20,12))


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
		
		# print(EEGchannels, ACCchannels, GYROchannels)

		##
		##-----
		##-----

		#load data into MNE
		#Filter
		#spectra
		#average over subjects
		#plot




		##-----
		#----

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
	


	plt.suptitle(['subject:', substr])
	plt.show()
