from __future__ import division
from scipy.io import wavfile
import clipboard
FILE = "/home/marvin/hello/C/MSP/Door_Alarm/seinfeld-8000.wav"

# def freq(file, start_time, end_time):
#     sample_rate, data = wavfile.read(file)

#     start_point = int(sample_rate * start_time / 1000)
#     end_point = int(sample_rate * end_time / 1000)
#     length = (end_time - start_time) / 1000

#     counter = 0
#     for i in range(start_point, end_point):
#         if data[i] < 0 and data[i + 1] > 0:
#             counter += 1

#     return counter / length

'''
def freq(file, start_time, end_time):
    sample_rate, data = wavfile.read(file)

    start_point = int(sample_rate * start_time / 1000)
    end_point = int(sample_rate * end_time / 1000)
    length = (end_time - start_time) / 1000

    counter = 0
    for i in range(start_point, end_point):
        if data[i] < 0 and data[i + 1] > 0:
            counter += 1

    return counter / length


fList = []
cnt = 0

sample_rate, data = wavfile.read("/home/marvin/hello/C/MSP/Door_Alarm/seinfeldTheme-8000hz.wav")
counter = 0
for i in range(len(data)):
    try:
        if data[i] < 0 and data[i + 1] > 0:
            fList.append(1)
    except IndexError:
        pass


# while True:
#     try:
#         fList.append(freq("/home/marvin/hello/C/MSP/Door_Alarm/seinfeldTheme-8000hz.wav", cnt, cnt + 1))
#         cnt += 1
#     except IndexError:
#         break

print(str(fList))
clipboard.copy(str(fList))
# print(wavfile.read('/home/marvin/hello/C/MSP/Door_Alarm/seinfeldTheme-8000hz.wav')[0])

'''
'''
#!/usr/bin/env python

# import librosa
import sys
import numpy as np
import matplotlib.pyplot as plt
# import librosa.display



np.set_printoptions(threshold=sys.maxsize)

filename = FILE
Fs = 8000
clip, sample_rate = librosa.load(filename, sr=Fs)

n_fft = 1024  # frame length
start = 0

hop_length=512

#commented out code to display Spectrogram
X = librosa.stft(clip, n_fft=n_fft, hop_length=hop_length)
#Xdb = librosa.amplitude_to_db(abs(X))
#plt.figure(figsize=(14, 5))
#librosa.display.specshow(Xdb, sr=Fs, x_axis='time', y_axis='hz')
#If to pring log of frequencies
#librosa.display.specshow(Xdb, sr=Fs, x_axis='time', y_axis='log')
#plt.colorbar()

#librosa.display.waveplot(clip, sr=Fs)
#plt.show()

#now print all values

t_samples = np.arange(clip.shape[0]) / Fs
t_frames = np.arange(X.shape[1]) * hop_length / Fs
#f_hertz = np.arange(N / 2 + 1) * Fs / N       # Works only when N is even
f_hertz = np.fft.rfftfreq(n_fft, 1 / Fs)         # Works also when N is odd

#example
print('Time (seconds) of last sample:', t_samples[-1])
print('Time (seconds) of last frame: ', t_frames[-1])
print('Frequency (Hz) of last bin:   ', f_hertz[-1])

print('Time (seconds) :', len(t_samples))

#prints array of time frames
print('Time of frames (seconds) : ', t_frames)
#prints array of frequency bins
print('Frequency (Hz) : ', f_hertz)

print('Number of frames : ', len(t_frames))
print('Number of bins : ', len(f_hertz))

#This code is working to printout frame by frame intensity of each frequency
#on top line gives freq bins
curLine = 'Bins,'
for b in range(1, len(f_hertz)):
    curLine += str(f_hertz[b]) + ','
print(curLine)

curLine = ''
for f in range(1, len(t_frames)):
    curLine = str(t_frames[f]) + ','
    for b in range(1, len(f_hertz)): #for each frame, we get list of bin values printed
        curLine += str("%.02f" % np.abs(X[b, f])) + ','
        #remove format of the float for full details if needed
        #curLine += str(np.abs(X[b, f])) + ','
        #print other useful info like phase of frequency bin b at frame f.
        #curLine += str("%.02f" % np.angle(X[b, f])) + ','
    print(curLine)
'''


# Good one


import numpy as np

def spectral_properties(y: np.ndarray, fs: int) -> dict:
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    spec = np.abs(spec)
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    sd = np.sqrt(np.sum(amp * ((freq - mean) ** 2)))
    amp_cumsum = np.cumsum(amp)
    median = freq[len(amp_cumsum[amp_cumsum <= 0.5]) + 1]
    mode = freq[amp.argmax()]
    Q25 = freq[len(amp_cumsum[amp_cumsum <= 0.25]) + 1]
    Q75 = freq[len(amp_cumsum[amp_cumsum <= 0.75]) + 1]
    IQR = Q75 - Q25
    z = amp - amp.mean()
    w = amp.std()
    skew = ((z ** 3).sum() / (len(spec) - 1)) / w ** 3
    kurt = ((z ** 4).sum() / (len(spec) - 1)) / w ** 4

    result_d = {
        'mean': mean,
        'sd': sd,
        'median': median,
        'mode': mode,
        'Q25': Q25,
        'Q75': Q75,
        'IQR': IQR,
        'skew': skew,
        'kurt': kurt
    }

    return result_d


import sys
from aubio import source, pitch

win_s = 4096
hop_s = 1 #512

s = source(FILE, 8000, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    pitches += [pitch]
    confidence = pitch_o.get_confidence()
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

ans = list(np.array(pitches))
print("Average frequency =", ans, "hz")

clipboard.copy(str(ans))

# sample_rate, data = wavfile.read(FILE)
# print(spectral_properties(data, 8000))










'''

from numpy.fft import rfft
from numpy import argmax, mean, diff, log, nonzero
from scipy.signal import blackmanharris, correlate
from time import time
import sys
try:
    import soundfile as sf
except ImportError:
    from scikits.audiolab import flacread

import parabolic


def freq_from_crossings(sig, fs):
    """
    Estimate frequency by counting zero crossings
    """
    # Find all indices right before a rising-edge zero crossing
    indices = nonzero((sig[1:] >= 0) & (sig[:-1] < 0))[0]

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    # crossings = indices

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever

    # return fs / mean(diff(crossings))
    return [ i / 1 for i in diff(crossings)]


# def freq_from_fft(sig, fs):
#     """
#     Estimate frequency from peak of FFT
#     """
#     # Compute Fourier transform of windowed signal
#     windowed = sig * blackmanharris(len(sig))
#     f = rfft(windowed)

#     # Find the peak and interpolate to get a more accurate peak
#     i = argmax(abs(f))  # Just use this for less-accurate, naive version
#     true_i = parabolic.ExplicitEuler(log(abs(f)), i)[0]

#     # Convert to equivalent frequency
#     return fs * true_i / len(windowed)


# def freq_from_autocorr(sig, fs):
#     """
#     Estimate frequency using autocorrelation
#     """
#     # Calculate autocorrelation and throw away the negative lags
#     corr = correlate(sig, sig, mode='full')
#     corr = corr[len(corr)//2:]

#     # Find the first low point
#     d = diff(corr)
#     start = nonzero(d > 0)[0][0]

#     # Find the next peak after the low point (other than 0 lag).  This bit is
#     # not reliable for long signals, due to the desired peak occurring between
#     # samples, and other peaks appearing higher.
#     # Should use a weighting function to de-emphasize the peaks at longer lags.
#     peak = argmax(corr[start:]) + start
#     px, py = parabolic.ExplicitEuler(corr, peak)

#     return fs / px


# def freq_from_HPS(sig, fs):
#     """
#     Estimate frequency using harmonic product spectrum (HPS)
#     """
#     windowed = sig * blackmanharris(len(sig))

#     from pylab import subplot, plot, log, copy, show

#     # harmonic product spectrum:
#     c = abs(rfft(windowed))
#     maxharms = 8
#     subplot(maxharms, 1, 1)
#     plot(log(c))
#     for x in range(2, maxharms):
#         a = copy(c[::x])  # Should average or maximum instead of decimating
#         # max(c[::x],c[1::x],c[2::x],...)
#         c = c[:len(a)]
#         i = argmax(abs(c))
#         true_i = parabolic(abs(c), i)[0]
#         print('Pass %d: %f Hz' % (x, fs * true_i / len(windowed)))
#         c *= a
#         subplot(maxharms, 1, x)
#         plot(log(c))
#     show()


filename = FILE

print('Reading file "%s"\n' % filename)
try:
    signal, fs = sf.read(filename)
except NameError:
    signal, fs, enc = flacread(filename)

# print('Calculating frequency from FFT:', end=' ')
# start_time = time()
# print('%f Hz' % freq_from_fft(signal, fs))
# print('Time elapsed: %.3f s\n' % (time() - start_time))

print('Calculating frequency from zero crossings:', end=' ')
start_time = time()
ans = freq_from_crossings(signal, fs)
print(f'{ans} Hz')
print('Time elapsed: %.3f s\n' % (time() - start_time))
clipboard.copy(str(ans))

# print('Calculating frequency from autocorrelation:', end=' ')
# start_time = time()
# print('%f Hz' % freq_from_autocorr(signal, fs))
# print('Time elapsed: %.3f s\n' % (time() - start_time))

# print('Calculating frequency from harmonic product spectrum:')
# start_time = time()
# freq_from_HPS(signal, fs)
# print('Time elapsed: %.3f s\n' % (time() - start_time))

'''