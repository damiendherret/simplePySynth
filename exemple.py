import numpy as np
import sounddevice as sd
from math import sin, pi
from pynput import keyboard
import threading

# paramètres
SAMPLE_RATE = 44100
BLOCK_SIZE = 512  # nombre d'échantillons par callback
MAX_VOICES = 16

# mapping clavier -> note MIDI (exemple piano sur clavier AZERTY/ QWERTY)
KEY_TO_MIDI = {
    'a': 60,  # C4
    'w': 61,  # C#4
    's': 62,  # D4
    'e': 63,  # D#4
    'd': 64,  # E4
    'f': 65,  # F4
    't': 66,  # F#4
    'g': 67,  # G4
    'y': 68,  # G#4
    'h': 69,  # A4
    'u': 70,  # A#4
    'j': 71,  # B4
    'k': 72,  # C5
    'o': 73,  # C#5
    'l': 74,  # D5
    'p': 75,  # D#5
}

def midi_to_freq(n):
    return 440.0 * (2 ** ((n - 69) / 12.0))

class Voice:
    def __init__(self, freq, waveform='sine', adsr=(0.01, 0.2, 0.7, 0.3)):
        self.freq = freq
        self.phase = 0.0
        self.waveform = waveform
        self.adsr = adsr  # (attack, decay, sustain, release) en secondes
        self.env = 0.0
        self.state = 'attack'
        self.active = True
        self.lock = threading.Lock()

        self.attack, self.decay, self.sustain, self.release = adsr
        self.sample_rate = SAMPLE_RATE

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
        phase_increment = 2 * pi * self.freq / self.sample_rate
        phases = self.phase + phase_increment * t
        if self.waveform == 'sine':
            waves = np.sin(phases)
        else:
            waves = np.sin(phases)  # placeholder pour d'autres formes

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

class SynthEngine:
    def __init__(self):
        self.voices = []
        self.lock = threading.Lock()

    def note_on(self, midi_note):
        freq = midi_to_freq(midi_note)
        with self.lock:
            if len(self.voices) >= MAX_VOICES:
                return
            #print(f"Note ON: MIDI {midi_note}, freq {freq:.2f} Hz")
            v = Voice(freq)
            self.voices.append(v)
            

    def note_off(self, midi_note=None):
        # On peut chercher la voix correspondante si on suit le MIDI,
        # ici on release toutes les voix actives (simplifié)
        with self.lock:
            for v in self.voices:
                if v.is_active():
                    v.note_off()

    def audio_callback(self, outdata, frames, time, status):
        if status:
            # print('Status:', status)
            pass
        # mélanger toutes les voix actives
        mix = np.zeros(frames)
        with self.lock:
            self.voices = [v for v in self.voices if v.is_active()]
            for v in self.voices:
                mix += v.render(frames)

        # normalisation simple et écriture dans le buffer (mono vers stereo)
        mix = mix * 0.25  # ajustement du niveau
        out = np.expand_dims(mix, axis=1)
        outdata[:] = out

def on_press(key, synth):
    try:
        k = key.char
    except AttributeError:
        return
    if k in KEY_TO_MIDI:
        synth.note_on(KEY_TO_MIDI[k])

def on_release(key, synth):
    try:
        k = key.char
    except AttributeError:
        return
    if k in KEY_TO_MIDI:
        synth.note_off(KEY_TO_MIDI[k])
    # Quit on Escape
    if key == keyboard.Key.esc:
        # Arrêter proprement n'est pas montré ici; ja mais on peut lever un flag
        return False

def main():
    synth = SynthEngine()
    # Démarrer le flux audio
    stream = sd.OutputStream(channels=1, callback=synth.audio_callback,
                             samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE)
    stream.start()

    # Listerner clavier (en thread séparé)
    listener = keyboard.Listener(on_press=lambda k: on_press(k, synth),
                                 on_release=lambda k: on_release(k, synth))
    listener.start()

    print("Synthé en écoute. Touchees: A W S E D F T G Y H U J K O L P ; ESC pour quitter.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        stream.stop()
        stream.close()

if __name__ == '__main__':
    main()