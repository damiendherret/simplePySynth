import threading
import numpy as np
import const

class LFO:
    def __init__(self, freq, waveform='sine', factor=0.3, sample_rate=const.SAMPLE_RATE):
        self.freq = freq
        self.phase = 0.0
        self.waveform = waveform
        self.lock = threading.Lock()
        self.factor = factor
        self.sample_rate = sample_rate
        

    def render(self, nframes):
        t = np.arange(nframes)
        # oscillateur simple (sine)
        phase_increment = 2 * np.pi * self.freq / self.sample_rate
        phases = self.phase + phase_increment * t
        if self.waveform == 'sine':
            waves = 0.5 + (0.5 * self.factor * np.sin(phases))
        else:
            waves = 0.5 + (0.5 * self.factor * np.sin(phases))  # placeholder pour d'autres formes
        self.phase = phases[-1]  # mise à jour du phasor

        return waves