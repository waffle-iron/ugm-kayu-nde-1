""" Recording modules
"""

# pylint: disable=locally-disabled, C0330, W0612

import sys
import wave
import datetime as dt
import pyaudio
from scipy.io import wavfile as wav

# Global variables and const
# Configurations for the recording
# Sampling rate: 48000 Hz
RATE = 48000
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
if sys.platform == 'darwin':
    CHANNELS = 1

# Functions, Classes & Procedures:
def time_now():
    """ Get current time
	"""
    return dt.datetime.now().strftime("%Y%m%d%H%M")

def kayurecord_save(filename, frames, container):
    """ Save audio recording to wav file
    """
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(container.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

def kayurecord(woodname, duration):
    """ Record audio and save to wav file
    """
    filename = time_now() + "_" + woodname + ".wav"
    container = pyaudio.PyAudio()
    stream = container.open(format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		frames_per_buffer=CHUNK)
    print("* start recording...")
    data = []
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    container.terminate()
    print("* done recording!")
    kayurecord_save(filename, frames, container)

def kayuopen(woodname):
    """ Open wav file
    """
    rate, data = wav.read(woodname)
    data = data / (2.**15)
    try:
        ch1 = data[:, 0]
    except IndexError:
        ch1 = data
    return rate, ch1
