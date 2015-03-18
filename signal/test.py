from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt
from utility import pcm2float
from numpy import *

fs, sig = wavfile.read('Jack.wav')
fs2, sig2 = wavfile.read('Paul.wav')

sigNorm = pcm2float(sig, 'float32')
sig2Norm = pcm2float(sig2, 'float32')

print sigNorm
print len(sigNorm)
#print a
#corr = signal.correlate(sig, sig2, mode = 'valid')
lags, c, line, b = plt.xcorr(sigNorm, sig2Norm)
print c
print lags
print line
#can use Mel Frequency Cepstral Coefficents
