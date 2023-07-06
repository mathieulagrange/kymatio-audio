# kymatio-audio

A repository for audio related processing tools based on the [kymatio](https://www.kymat.io) library.

The scattering audio distance (SAD) aims at providing an 'artificial ear' i.e. a computational proxy for assessing the auditory distance between two sounds.

Main advantages of the SAD:
 - conceptual equivalence to modern physiological models of the first layers of the human auditory system
 - strong mathematical grounding
 - controllable levels of invariance at each layers

## Compute the SAD

```
from kymatio_audio import scattering_audio_distance as sad

scattering_distances = sad.scattering_audio_distance(audio, sampling_rate)
```
where `audio` is a list of 1d arrays with audio sampled at the same `sampling_rate`, and `scattering_distances` is a square and symmetric matrix of pairwise SAD distances.

## Demonstrations

A series of jupyter notebooks are available for demonstrating the potential of the SAD with respect to the Multi-Scale Spectral (MSS) Loss. See the [notebooks](notebooks/) directory.

For each demonstration
 - a set of sounds is considered
 - the MSS and the SAD distances are computed for every pairs
 - a multidimensional scaling is done to project the sounds on a 2d plane for visual inspection.

### Noise resilience

In this experiment, we consider two vowels an *a* and a *i* that is buried in white noise of decreasing level. It is expected that on the 2d plane, the sounds with the *a* and *i* are far apart and the ones with the lower SNR are closer to each other than the ones with high SNR. [listen](assets/noise.wav)

![MSS](assets/noise_mss.png)
![SAD](assets/noise_sad.png)

MSS and SAD perform similarly in this case, which is expected since no modulations are involved for discriminability.

### Vocalic triangle

In this experiment, we consider a set of vowels recorded by [Bruce P. Hayes](https://linguistics.ucla.edu/people/hayes), made available [here](https://linguistics.ucla.edu/people/hayes/103/Charts/VChart). The audio data as well as the reference chart below are used with permission. Please [listen](assets/vowel.wav) to the set of vowels sequenced from *i* to *u*.

![MSS](assets/vowel.jpeg)
![MSS](assets/vowel_mss.png)
![SAD](assets/vowel_sad.png)

While the MSS retrieves correctly organization along the first format, the SAD retrieves it better along the second formant, achieving an organization close to the reference vocalic triangle.

### McAdams Timbre dataset

In this experiment, we consider . [listen](assets/mcadams.wav)

![MSS](assets/mcadams_mss.png)
![SAD](assets/mcadams_sad.png)

### 

In this experiment, we consider . [listen](assets/instrument.wav)

![MSS](assets/instrument_mss.png)
![SAD](assets/instrument_sad.png)

### 

In this experiment, we consider . [listen](assets/.wav)

![MSS](assets/technique_mss.png)
![SAD](assets/technique_sad.png)

### 

In this experiment, we consider . [listen](assets/texture.wav)

![MSS](assets/texture.png)

![MSS](assets/texture_mss.png)
![SAD](assets/texture_sad.png)

## Future work:
 - use audio type for determining the kymatio frontend
 - provide a series of default parametrizations for standard tasks
