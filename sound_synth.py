import numpy as np
import sounddevice as sd
from pynput import keyboard
from voice import Voice
from synthengine import SynthEngine
import threading
import const

# Flag to control the program's execution
running = True

def main():
    synth = SynthEngine()


    print("|  | r|  | t|  |  | u|  | i|  | o|  |  |   ")
    print("|  |__|  |__|  |  |__|  |__|  |__|  |  |_  ")
    #print("|    |    |    |    |     |     |   |    | ") 
    print("|  d |  f |  g |  h |  j  |  k  | l |  m | ")
    print("|____|____|____|____|_____|_____|___|____|")
    print("")
    print("Press any key to play. Press 'esc' to exit.")


    # Démarrer le flux audio
    stream = sd.OutputStream(channels=1, callback=synth.audio_callback,
                             samplerate=const.SAMPLE_RATE, blocksize=const.BLOCK_SIZE)
    stream.start()

    # Listerner clavier (en thread séparé)
    listener = keyboard.Listener(on_press=lambda k: on_press(k, synth),
                                 on_release=lambda k: on_release(k, synth))
    listener.start()





    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        stream.stop()
        stream.close()






def on_press(key, synth):
    try:
        k = key.char
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_on(k, const.KEY_TO_MIDI[k])

def on_release(key, synth):
    try:
        k = key.char
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_off(k, const.KEY_TO_MIDI[k])
    # Quit on Escape
    if key == keyboard.Key.esc:
        running = False
        return False

def my_function():
    print("Key pressed! Function executed.")

def white_noise(
    duration : float=1.0,
    amplitude : float=0.5,
    sample_rate : int=44100
    )-> np.ndarray:
    
    #calculate the number of samples
    n_samples = int(duration * sample_rate)
    #generate white noise
    noise = np.random.uniform(low=-1.0, high=1.0, size=n_samples)
    #scale by amplitude
    noise *= amplitude
    return noise


def sine_tone(
    frequency: int=440,
    duration : float=1.0,
    amplitude : float=0.5,
    sample_rate : int=44100
    )-> np.ndarray:
    
    #calculate the number of samples
    n_samples = int(duration * sample_rate)

    #array of time points
    time_points = np.linspace(0, duration, n_samples, endpoint=False)

    #create the sine wave
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time_points)

    return sine_wave


def apply_enveloppe(
        sound: np.array,
        adsr: list,
        sample_rate: int=44100
    )-> np.ndarray:

    sound = sound.copy()
    attack_samples = int(adsr[0] * sample_rate)
    decay_samples = int(adsr[1] * sample_rate)
    relase_samples = int(adsr[3] * sample_rate)
    sustain_samples = len(sound) - (attack_samples + decay_samples + relase_samples)

    #attack phase
    sound[:attack_samples] *= np.linspace(0, 1, attack_samples)

    #decay phase
    sound[attack_samples:attack_samples+decay_samples] *= np.linspace(1, adsr[2], decay_samples)

    #sustain phase
    sound[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] *= adsr[2]

    #release phase
    sound[attack_samples+decay_samples+sustain_samples:] *= np.linspace(adsr[2], 0, relase_samples)

    return sound


if __name__ == "__main__": main()
