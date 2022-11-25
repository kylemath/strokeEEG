import pandas as pd
import matplotlib.pyplot as plt
import mne
import numpy as np
import time
import pickle
pd.options.display.float_format = '{:.9f}'.format

outPSD = []
allSubjectNumber = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
#R=1; L=2
strokeHemisphere = [2, 2, 2, 1,	2, 1, 2, 1,	1,	2,	1,	2,	1,	2,	1,	2,	1,	1,	1,	2,	2,	1]
surgerySucsScore = [1, 2, 3]

for idx, isub in enumerate(allSubjectNumber):

	substr = str(isub).zfill(2)
	print('______________')
	print('Subject #: ' + substr)
	print('______________')

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
		print(df.columns)
		if 12 <= isub <= 16:
			EEGchannels = df.columns[2:7].tolist() #2:7, 9:12, 14:18
			ACCchannels = df.columns[10:13].tolist()
			GYROchannels = df.columns[16:19].tolist()
		else: # 1-11
			EEGchannels = df.columns[2:7].tolist() #2:8, 9:13, 14:18
			ACCchannels = df.columns[9:12].tolist()
			GYROchannels = df.columns[14:17].tolist()
		
		intervals = df['timestamps'].diff()

		if 12 <= isub <= 16:
			srate = 256
		else: 
			srate = round(1/intervals.mean())


		# ch_names = ['TP7', 'AF9', 'AF8', 'TP10', 'Wrist', 'ACC_x', 'ACC_y', 'ACC_z', 'GYRO_x', 'GYRO_y', 'GYRO_z']
		# This is only correct if left hemisphere is bad (strokeHemisphere == 2
		# so need to switch columns for strokeHemisphere == 1 below)
		ch_names = ['TPBad', 'AFBad', 'AFGood', 'TPGood', 'Wrist', 'ACC_x', 'ACC_y', 'ACC_z', 'GYRO_x', 'GYRO_y', 'GYRO_z']

		ch_types = ['bio'] * 4 + ['ecg'] + ['bio'] * 6
		info = mne.create_info(ch_names, ch_types=ch_types, sfreq=srate)
		info.set_montage('standard_1020')

		if 12 <= isub <= 16:
			df = df.drop(['index_x', 'timestamps', 'info', 'index_y', 'sequenceId_x', 'Unnamed: 5_x', 'index', 'sequenceId_y', 'Unnamed: 5_y'], axis=1)
		else: 
			df = df.drop(['index_x', 'timestamps',  'Marker0_x', 'index_y', 'Marker0_y', 'index', 'Marker0'], axis=1)
		
		data = df.to_numpy().transpose()/1000000
		print(data.shape)
		if strokeHemisphere[idx] == 1: # if Right
			print('Switching data columns for Right hemisphere infarcts')
			# so need to switch columns for strokeHemisphere == 1 below)
			tempDataTP = data[0,:]
			tempDataAF = data[1,:]
			data[0,:] = data[3,:]
			data[1,:] = data[2,:]
			data[3,:] = tempDataTP
			data[2,:] = tempDataAF

		rawData = mne.io.RawArray(data, info)
		picks = mne.pick_types(rawData.info, eeg=True, ecg=True,
                       bio=True)

		rawSpectra = rawData.compute_psd(picks=picks)
		psds, freqs = rawSpectra.get_data(return_freqs=True, picks=picks)

		subPSDs.append(psds)
	outPSD.append(subPSDs)
	

npOut = np.array(outPSD)
seshNames = ['Pre', 'Post', 'Late']

preAll = np.log10(npOut[:, 0, :, 1:50])
postAll = np.log10(npOut[:, 1, :, 1:50])
lateAll = np.log10(npOut[:, 2, :, 1:50])

# subtract good - bad hemisphere for each subject and channel and spectra
preAllGoodBadTP = preAll[:,0,:]-preAll[:,3,:]
preAllGoodBadAF = preAll[:,1,:]-preAll[:,2,:]
postAllGoodBadTP = postAll[:,0,:]-postAll[:,3,:]
postAllGoodBadAF = postAll[:,1,:]-postAll[:,2,:]
lateAllGoodBadTP = lateAll[:,0,:]-lateAll[:,3,:]
lateAllGoodBadAF = lateAll[:,1,:]-lateAll[:,2,:]

preAllGoodBadTPavg =  preAllGoodBadTP.mean(axis=0).transpose()
preAllGoodBadAFavg =  preAllGoodBadAF.mean(axis=0).transpose()
postAllGoodBadTPavg = postAllGoodBadTP.mean(axis=0).transpose()
postAllGoodBadAFavg = postAllGoodBadAF.mean(axis=0).transpose()
lateAllGoodBadTPavg = lateAllGoodBadTP.mean(axis=0).transpose()
lateAllGoodBadAFavg = lateAllGoodBadAF.mean(axis=0).transpose()

preAllGoodBadTPstd =  preAllGoodBadTP.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))
preAllGoodBadAFstd =  preAllGoodBadAF.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))
postAllGoodBadTPstd = postAllGoodBadTP.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))
postAllGoodBadAFstd = postAllGoodBadAF.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))
lateAllGoodBadTPstd = lateAllGoodBadTP.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))
lateAllGoodBadAFstd = lateAllGoodBadAF.std(axis=0).transpose() / np.sqrt(len(strokeHemisphere))


avgs = [preAllGoodBadTPavg, preAllGoodBadAFavg, postAllGoodBadTPavg, postAllGoodBadAFavg, lateAllGoodBadTPavg, lateAllGoodBadAFavg]
stds = [preAllGoodBadTPstd, preAllGoodBadAFstd, postAllGoodBadTPstd, postAllGoodBadAFstd, lateAllGoodBadTPstd, lateAllGoodBadAFstd]
freqs = freqs

outDict = {	
			'avgs': avgs, 
			'stds': stds,  
			'freqs': freqs, 
			'ch_names': ch_names,
}

with open('outDictGoodBad.pickle', 'wb') as f:
    pickle.dump(outDict, f)



# prePostAll = np.subtract(preAll, postAll)
# preLateAll = np.subtract(preAll, lateAll)
# postLateAll = np.subtract(postAll, lateAll)

# prePostAllAvg = prePostAll.mean(axis=0).transpose()
# preLateAllAvg = preLateAll.mean(axis=0).transpose()
# postLateAllAvg = postLateAll.mean(axis=0).transpose()

# prePostAllStd = prePostAll.std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))
# preLateAllStd = preLateAll.std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))
# postLateAllStd = postLateAll.std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))

# preAvg = np.log10(npOut[:, 0, :, 1:50]).mean(axis=0).transpose()
# preAvgStd = np.log10(npOut[:, 0, :, 1:50]).std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))
# postAvg = np.log10(npOut[:, 1, :, 1:50]).mean(axis=0).transpose()
# postAvgStd =  np.log10(npOut[:, 1, :, 1:50]).std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))
# lateAvg = np.log10(npOut[:, 2, :, 1:50]).mean(axis=0).transpose()
# lateAvgStd =  np.log10(npOut[:, 2, :, 1:50]).std(axis=0).transpose()/np.sqrt(len(strokeHemisphere))


