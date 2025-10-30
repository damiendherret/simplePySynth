import threading
import numpy as np
import const

class Voice:
    def __init__(self, freq, waveform='Sine', adsr=(0.02, 0.05, 1, 0.5), sample_rate=const.SAMPLE_RATE, harmonics=[]):
        self.freq = freq
        self.phase = 0.0
        self.waveform = waveform
        self.adsr = adsr  # (attack, decay, sustain, release) en secondes
        self.env = 0.0
        self.state = 'attack'
        self.active = True
        self.lock = threading.Lock()

        self.harmonics = harmonics

        self.attack, self.decay, self.sustain, self.release = adsr
        self.sample_rate = sample_rate

    def note_off(self):
        with self.lock:
            if self.active:
                self.state = 'release'
                self.release_start_env = self.env

    def is_active(self):
        with self.lock:
            return self.active

    def render(self, nframes):
        t = np.arange(nframes)
        # oscillateur simple (sine)
        
        phase_increments =[]
        
        phase_increment = 2 * np.pi * self.freq / self.sample_rate
        phase_increments.append(phase_increment)  # fundamental
        
        for h in self.harmonics:
            phase_increments.append(phase_increment * (h+2))  # harmonics start from H2

        
        waves = np.zeros(nframes)


        for i, phase_inc in enumerate(phase_increments):
            phases = self.phase + phase_inc * t
            if self.waveform == 'Sine':
                waves += 0.1 * np.sin(phases)
            elif self.waveform == 'Square':
                # carré simple : +1 pour la moitié positive, -1 pour la moitié négative
                waves += 0.1 * np.where(np.sin(phases) >= 0.0, 1.0, -1.0)
            elif self.waveform == 'Saw':
                waves += 0.1 * 2.0 * (np.mod(phases, 2.0 * np.pi) / (2.0 * np.pi)) - 1.0
            else:
                waves += 0.1 * np.sin(phases)  # placeholder pour d'autres formes
        


        # phases = self.phase + phase_increment * t
        # if self.waveform == 'Sine':
        #     waves = np.sin(phases)
        # elif self.waveform == 'Square':
        #     # carré simple : +1 pour la moitié positive, -1 pour la moitié négative
        #     waves = np.where(np.sin(phases) >= 0.0, 1.0, -1.0)
        # elif self.waveform == 'Saw':
        #     waves = 2.0 * (np.mod(phases, 2.0 * np.pi) / (2.0 * np.pi)) - 1.0
        # else:
        #     waves = np.sin(phases)  # placeholder pour d'autres formes

        # enveloppe ADSR (simplifiée, linéaire)
        env = np.zeros(nframes)
        for i in range(nframes):
            if self.state == 'attack':
                self.env += (1.0 / max(1, int(self.attack * self.sample_rate)))
                if self.env >= 1.0:
                    self.env = 1.0
                    self.state = 'decay'
            elif self.state == 'decay':
                self.env -= (1.0 - self.sustain) / max(1, int(self.decay * self.sample_rate))
                if self.env <= self.sustain:
                    self.env = self.sustain
                    self.state = 'sustain'
            elif self.state == 'sustain':
                self.env = self.sustain
            elif self.state == 'release':
                self.env -= self.sustain / max(1, int(self.release * self.sample_rate))
                if self.env <= 0.0:
                    self.env = 0.0
                    self.active = False
            env[i] = self.env

        self.phase = phases[-1]  # mise à jour du phasor
        return waves * env