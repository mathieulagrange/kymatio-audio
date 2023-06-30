import numpy as np
import librosa as lr
from scipy.spatial import distance as dist
from kymatio.numpy import TimeFrequencyScattering

import auraloss
import torch

# MIT license
# talk about time support
# todo median like norm

TARGET_SR = 22050

def multiscale_audio_distance(audio, sr):

    audio = fix_audio(audio, sr)

    aura_fn = auraloss.freq.MultiResolutionSTFTLoss(
        fft_sizes=[1024, 2048, 8192],
        hop_sizes=[256, 512, 2048],
        win_lengths=[1024, 2048, 8192],
        scale="mel",
        n_bins=128,
        sample_rate=sr,
        perceptual_weighting=True,
    )

    mss_distances = np.zeros((len(audio), len(audio)))
    for s_ii, s_i in enumerate(audio):
        for s_jj, s_j in enumerate(audio): 
            if s_jj>s_ii:
                sit = torch.unsqueeze(torch.unsqueeze(torch.tensor(s_i, dtype=torch.float32), 0), 0)
                sjt = torch.unsqueeze(torch.unsqueeze(torch.tensor(s_j, dtype=torch.float32), 0), 0)
                mss_distances[s_ii, s_jj] = aura_fn(sit, sjt).numpy()
                mss_distances[s_jj, s_ii] = mss_distances[s_ii, s_jj]
    
    return mss_distances

def scattering_audio_distance(audio, sr, normalization=1e-6):
    
    c = scattering_audio(audio, sr)
    c = np.delete(c, 0, 1)
    c = np.log1p(c/normalization)
    p = dist.squareform(dist.pdist(c))
    return p
    
def scattering_audio(audio, sr):

    audio = fix_audio(audio, sr, size='power_log')

    jtfs = TimeFrequencyScattering(
        shape = audio[0].shape[0],
        Q=(8, 2), # quality factors for first and second order scattering
        J=12, # maximum wavelet scale for time scattering
        J_fr=3, # maximum wavelet scale for frequential scattering
        Q_fr=2, # quality factor for frequential scattering
        T='global', # global averaging over time,
        format='time'
        )
    
    print('Time support: '+str(jtfs.shape[0]/TARGET_SR)+' seconds.')
    
    c = np.zeros((len(audio), jtfs.output_size()))
    for a_i, a in enumerate(audio):
        c[a_i, :] = np.squeeze(jtfs(a))
    return c

def power_log(x):
    return int(2**(np.ceil(np.log2(x))))

def fix_audio(audio, sr, size=None):

    a_l = 0
    for a in audio:
        if a_l<a.shape[0]:
            a_l = a.shape[0]
    
    print('Max num samples '+str(a_l))
    print('Max duration '+str(a_l/sr)+' seconds.')

    if size=='power_log':
        a_l=power_log(a_l)

    for a_i, a in enumerate(audio):
        lr.util.valid_audio(a, mono=True)
        if sr != TARGET_SR:
            a = lr.resample(a, orig_sr=sr, target_sr=TARGET_SR)
        audio[a_i] = lr.util.fix_length(a, size=a_l)
    return audio

if __name__ == "__main__":
    i, sr = lr.load('../audio/speech/i.wav')
    o, sr = lr.load('../audio/speech/o.wav')

    multiscale_audio_distance([i, o], sr)
    scattering_audio_distance([i, o], sr)
    

