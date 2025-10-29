import tkinter as tk
import const
import sounddevice as sd
from synthengine import SynthEngine

def key_press(event,synth):
    #print("press", event.char, event.keysym, event.keycode)
    try:
        k = event.char
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_on(k, const.KEY_TO_MIDI[k])

def key_released(event,synth):
    #print("release" , event.char, event.keysym, event.keycode)
    try:
        k = event.char
    except AttributeError:
        return
    if k in const.KEY_TO_MIDI:
        synth.note_off(k, const.KEY_TO_MIDI[k])

def main():
    synth = SynthEngine()

    stream = sd.OutputStream(channels=1, callback=synth.audio_callback,
                             samplerate=const.SAMPLE_RATE, blocksize=const.BLOCK_SIZE)
    stream.start()

    root = tk.Tk()
    root.title("Sample Tkinter App")


    x = root.winfo_screenwidth() // 2 - 250
    y = int(root.winfo_screenheight() * 0.1)
    root.geometry('500x600+' + str(x) + '+' + str(y))

    frame1 = tk.Frame(root, width=500, height=600, bg="#3d6466")
    frame1.grid(row=0, column=0)


    root.bind('<KeyPress>', lambda event:key_press(event,synth))
    root.bind('<KeyRelease>', lambda event:key_released(event,synth) )

    root.mainloop()

if __name__ == "__main__": main()