""" FFT calculation for wood nondestructive evaluation
"""

from numpy.fft import fft
from numpy import arange, ceil, log10
from scipy.signal import butter, lfilter


def kayufft_db(signal, rate):
    """ Perform FFT for wood's longitudinal stress wave signal
        Inputs:
        Acoustic signal in time domain and the sampling rate
        Returns:
        Signal in ferquency domain with unit in dB
    """
    signal_length = len(signal)
    fft_result = fft(signal)
    uniq_points = int(ceil((signal_length + 1) / 2.0)) #only takes one side of FFT result
    fft_result = fft_result[0:uniq_points]
    fft_result = abs(fft_result)
    fft_result = fft_result / float(signal_length)
    fft_result = fft_result**2
    if signal_length % 2 > 0:
        fft_result[1:len(fft_result)] = fft_result[1:len(fft_result)] * 2
    else:
        fft_result[1:len(fft_result) - 1] = fft_result[1:len(fft_result) - 1] * 2
    fft_abscissa = arange(0, uniq_points, 1.0) * (rate / signal_length)
    fft_ordinate = 10 * log10(fft_result)
    return fft_ordinate, fft_abscissa

def argmax_p(fft_ordinate, rate):
    """ Find an argmax of fft result
    """
    upper_thresh_freq = 4100
    lower_thresh_freq = 800
    upper_thresh = int(len(fft_ordinate) / (rate / 2) * upper_thresh_freq)
    lower_thresh = int(len(fft_ordinate) / (rate / 2) * lower_thresh_freq)
    # return fft_ordinate.argmax()
    return fft_ordinate[lower_thresh:upper_thresh].argmax()

def max_p(fft_ordinate, rate):
    """ Find an argmax of fft result
    """
    upper_thresh_freq = 4100
    lower_thresh_freq = 800
    upper_thresh = int(len(fft_ordinate) / (rate / 2) * upper_thresh_freq)
    lower_thresh = int(len(fft_ordinate) / (rate / 2) * lower_thresh_freq)
    # return max(fft_ordinate)
    return max(fft_ordinate[lower_thresh:upper_thresh])

def butter_bandpass(lowcut, highcut, sampling_freq, order=5):
    """ Butterworth with default order of 5
    """
    nyq = 0.5 * sampling_freq
    low = lowcut / nyq
    high = highcut / nyq
    numerator, denominator = butter(order, [low, high], btype='band')
    return numerator, denominator

def butter_bandpass_filter(signal, lowcut, highcut, sampling_freq, order=5):
    """ Butterworth filter with default order of 5
    """
    numerator, denominator = butter_bandpass(lowcut, highcut, sampling_freq, order=order)
    y_array = lfilter(numerator, denominator, signal)
    return y_array

def kayu_damping_filter(signal, p_db, rate, range_pm=100):
    """ Adaptive Butterworth filter for measuring wood's modulus of elasticity
    """
    center_f = argmax_p(p_db, rate)
    lowcut = center_f - range_pm
    highcut = center_f + range_pm
    filtered_signal = butter_bandpass_filter(signal, lowcut, highcut, rate, order=3)
    return filtered_signal

def damping_envelope(filtered_signal, rate, size=1764):
    """ find the envelope of exponential decay of wood's longitudinal stress wave signal
    """
    # TO - DO: Implement the envelope fitting
    start_point = filtered_signal.argmax() # starting point dari envelope
    time_array = arange(0, filtered_signal.shape[0], 1)
    time_array = time_array / rate
    time_array = time_array * 1000  # scale to milliseconds
