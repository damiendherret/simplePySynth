import threading
from voice import Voice
import numpy as np
import const
import LFO

class SynthEngine:

    def midi_key_to_freq(self, midi_note):
        return 440.0 * (2 ** ((midi_note - 69) / 12.0))

    def __init__(self):
        self.voices = []
        self.lock = threading.Lock()
        self.pressed_keys = set()
        self.LFO = LFO.LFO(freq=3.0, waveform='sine', factor= 0.4, sample_rate=const.SAMPLE_RATE)

    def note_on(self, key, midi_note):
        if not (key in self.pressed_keys) : 
            #print("New Key pressed:", key)
            freq = self.midi_key_to_freq(midi_note)
            with self.lock:
                if len(self.voices) >= const.MAX_VOICES:
                    return
                #print(f"Note ON: MIDI {midi_note}, freq {freq:.2f} Hz")
                v = Voice(freq)
                self.voices.append(v)
                self.pressed_keys.add(key)
        #else:
            #print("Key already pressed:", key)
                
            

    def note_off(self, key, midi_note):
        # On peut chercher la voix correspondante si on suit le MIDI,
        # ici on release toutes les voix actives (simplifié)
        with self.lock:
            if (key in self.pressed_keys) :
                #print("Key Off:", key)
                self.pressed_keys.remove(key) 
                for v in self.voices:
                    if v.freq == self.midi_key_to_freq(midi_note):
                        if v.is_active():
                            v.note_off()
                        else:
                            self.voices.remove(v)

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

        mix = mix * self.LFO.render(frames)

        out = np.expand_dims(mix, axis=1)
        outdata[:] = out