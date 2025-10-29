import numpy as np
import sounddevice as sd
from voice import Voice
from synthengine import SynthEngine
import threading
import const


import keyboard

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


    while True:
        # Wait for the next event.
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting...")
                break
            else:
                on_press(event, synth)
            #print(event.name, ' was pressed')
        if event.event_type == keyboard.KEY_UP:
            # print(event.name, ' was upped')
            on_release(event, synth)



def on_press(event, synth):
    try:
        k = event.name
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_on(k, const.KEY_TO_MIDI[k])

def on_release(event, synth):
    try:
        k = event.name
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_off(k, const.KEY_TO_MIDI[k])









if __name__ == "__main__": main()
