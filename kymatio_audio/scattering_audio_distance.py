import numpy as np
import librosa as lr
from scipy.spatial import distance as dist
import kymatio as kym

# MIT license

TARGET_SR = 22050



# talk about time support

# todo median like norm

def scattering_audio_distance(audio, sr, normalization=1e-6):
    
    c = scattering_audio(audio, sr)
    c = np.log1p(c/normalization)
    p = dist.squareform(dist.pdist(c))
    return p
    
def scattering_audio(audio, sr):

    a_l = 0
    for a in audio:
        if a_l<a.shape[0]:
            a_l = a.shape[0]
    
    print('Max num samples '+str(a_l))
    print('Max duration '+str(a_l/sr)+' seconds.')

    jtfs = kym.TimeFrequencyScattering(
        shape = power_log(a_l),
        Q=(8, 2), # quality factors for first and second order scattering
        J=12, # maximum wavelet scale for time scattering
        J_fr=3, # maximum wavelet scale for frequential scattering
        Q_fr=2, # quality factor for frequential scattering
        T='global' # global averaging over time
        )
    print('Time support: '+str(jtfs.shape[0]/TARGET_SR)+' seconds.')
    
    c = np.zeros((len(audio), jtfs.output_size()-1))
    for a_i, a in enumerate(audio):
        lr.util.valid_audio(a, mono=True)
        if sr != TARGET_SR:
            a = lr.resample(a, orig_sr=sr, target_sr=TARGET_SR)
        a = lr.util.fix_length(a, size=jtfs.shape[0])
        c[a_i, :] = np.squeeze(np.mean(jtfs(a), axis=1))
    return c

def power_log(x):
    return int(2**(np.ceil(np.log2(x))))

if __name__ == "__main__":
    i, sr = lr.load('../audio/i.wav')
    o, sr = lr.load('../audio/o.wav')

    scattering_audio_distance([i, o], sr)

