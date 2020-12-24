from scipy.signal import butter, lfilter
from scipy.signal import freqs
import numpy as np

def butterworth_lowpass(data, cutoff, fs=1, order=4):
    b, a = butter(order, cutoff, btype='low', analog = False, fs=fs)
    y = lfilter(b, a, data)
    return y
