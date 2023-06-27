import numpy as np
import librosa as lr
from scipy.spatial import distance as dist
from kymatio import TimeFrequencyScattering as jtfs_module
from presets import Preset

# MIT license

TARGET_SR = 22050

jtfs_preset = Preset(jtfs_module)
jtfs_preset['Q'] = (8, 2) # quality factors for first and second order scattering
jtfs_preset['J'] = 12 # maximum wavelet scale for time scattering
jtfs_preset['J_fr'] = 3 # maximum wavelet scale for frequential scattering
jtfs_preset['Q_fr'] = 2 # quality factor for frequential scattering
jtfs_preset['T'] = 'global' # global averaging over time

jtfs = jtfs_preset()

# talk about time support

# todo median like norm

def scattering_audio_distance(audio, sr, normalization=1e-6):
    
    c = scattering_audio(audio, sr)
    c = np.log1p(c/normalization)
    p = dist.squareform(dist.pdist(c))
    return p
    
def scattering_audio(audio, sr):

    c = np.zeros((len(audio), jtfs.output_size()))
    for a_i, a in enumerate(audio):
        lr.util.valid_audio(a, mono=True)
        if sr != TARGET_SR:
            a = lr.resample(a, orig_sr=sr, target_sr=TARGET_SR)
        a = lr.util.fix_length(a, size=jtfs.shape[0])
        c[a_i, :] = jtfs(a)
    print('time support: '+str(jtfs.shape[0]*TARGET_SR)+' seconds.')
    return c