import threading
import numpy as np
import const

class LFO:
    def __init__(self, freq, waveform='Sine', factor=0.5, sample_rate=const.SAMPLE_RATE):
        self.freq = freq
        self.phase = 0.0
        self.waveform = waveform
        self.lock = threading.Lock()
        self.factor = factor
        self.sample_rate = sample_rate
        self.frames = []
        

    def render(self, nframes):
        t = np.arange(nframes)
        # oscillateur simple (sine)
        phase_increment = 2 * np.pi * self.freq / self.sample_rate
        phases = self.phase + phase_increment * t
        if self.waveform == 'Sine':
            waves = 0.5 + (0.5 * self.factor * np.sin(phases))
        if self.waveform == 'Square':
            waves = np.where(np.sin(phases) >= 0.0, 1, 1- self.factor)
        else:
            waves = 0.5 + (0.5 * self.factor * np.sin(phases))  # placeholder pour d'autres formes
        self.phase = phases[-1]  # mise à jour du phasor

        self.frames = waves

    

    def setfactor(self, factor):
        with self.lock:
            self.factor = factor

    def setfreq(self, freq):
        with self.lock:
            self.freq = freq
