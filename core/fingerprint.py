import hashlib
import scipy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (binary_erosion,
                                      generate_binary_structure,
                                      iterate_structure)

import librosa
import librosa.display
import IPython.display as ipd
import pandas as pd
from statistics import mode
from collections import Counter

def fingerprint(x, fs):
    '''
    Implementation of fingerprinting.
    '''
    x = preprocess(x, fs)
    X = librosa.stft(x, n_fft = 4096, hop_length = 2048)
    peaks = get_2D_peaks(librosa.amplitude_to_db(abs(X), ref=np.max))
    
    return generate_hashes(peaks)

def preprocess(x, fs):
    '''
    Make sure the audio files are mono-channel and 
    sampled at 44100 Hz.
    '''
    if x.ndim==2:
        x = x[:,0].squeeze()
    if int(fs) != int(44100):
        x = scipy.signal.resample(x, int(x.size*44100/fs))
    return x
    
def get_2D_peaks(arr2D, plot=False, amp_min=-60):
    """
    Extract maximum peaks from the spectogram matrix (arr2D).
    :param arr2D: matrix representing the spectogram in dB (ref=np.max).
    :param plot: for plotting the results.
    :param amp_min: minimum amplitude in spectrogram in order to be considered a peak.
    :return: a list composed by a list of frequencies and times.
    """
    
    struct = generate_binary_structure(2, 2) 
    neighborhood = iterate_structure(struct, 10) #generate a 20 by 20 matrix of the boolean, True
    
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D # find local maximums in the arr2D
    # with in the predefined neighborhood
    background = (arr2D == 0)
    # apply erosion
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    # Boolean mask of arr2D with True at peaks (applying XOR on both matrices).
    detected_peaks = local_max != eroded_background
    # extract peaks
    amps = arr2D[detected_peaks]
    freqs, times = np.where(detected_peaks)
    # filter peaks
    amps = amps.flatten()
    # get indices for frequency and time
    filter_idxs = np.where(amps > amp_min)
    freqs_filter = freqs[filter_idxs]
    times_filter = times[filter_idxs]
  
    peaks = list(zip(freqs_filter, times_filter)) #(freq, time) coordinates of all the peaks
    
    # plotting the constellation map/reduced spectrogram (it's not really a spectrogram
    # since the magnitude of peaks are ignored. They are just marked using random value, 100 in this case)
    left = np.zeros(arr2D.shape)
    for coordinate in peaks:
        left[coordinate] = 100
        
    if plot:
        plt.figure(figsize=(15, 5))
        librosa.display.specshow(librosa.amplitude_to_db(abs(left),ref=np.max),sr=fs,hop_length=2048,y_axis='log', x_axis='time')
        plt.title('Constellation map')
        plt.tight_layout()

    return peaks


def generate_hashes(peaks, fan_value=25):
    """
    Hash list structure:
       sha1_hash[0:FINGERPRINT_REDUCTION]    time_offset
        [(e05b341a9b77a51fd26, 32), ... ]
    :param peaks: list of peak frequencies and times.
    :param fan_value: degree to which a fingerprint can be paired with its neighbors.
    :return: a list of hashes with their corresponding offsets.
    """
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if 0 <= t_delta <= 200:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8')) 
                    #sha1 hash gives a length-40 hexdigit number. we trimmed to only 20
                    #characters to save storage memory. This may increase the probability 
                    #of collisions but it's a nice trade-off.
                    hashes.append((h.hexdigest()[0:20], t1)) 
                    # a tuple (address, offset of the anchor point)

    return hashes