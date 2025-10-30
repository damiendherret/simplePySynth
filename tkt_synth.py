import tkinter as tk
import customtkinter
import const
import sounddevice as sd
from synthengine import SynthEngine
from OscShapeSelector import OscShapeSelector


class SynthApp(customtkinter.CTk):
    def __init__(self):
        
        
        # Initialize SynthEngine and audio stream
        self.synth = SynthEngine()
        self.stream = sd.OutputStream(
            channels=1, 
            callback=self.synth.audio_callback,
            samplerate=const.SAMPLE_RATE, 
            blocksize=const.BLOCK_SIZE)
        self.stream.start()

        # Initialize the main window
        super().__init__()
        self.title("Tkt SYNTH")
        self.geometry("600x600")
        self.configure(fg_color=const.BG_DARK)
        
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        #self.grid_rowconfigure(2, weight=2)

        # OSC Frame 
        self.osc_frame = customtkinter.CTkFrame(self,fg_color=const.BG_FRAME)
        self.osc_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.osc_label = customtkinter.CTkLabel(
            self.osc_frame, text="OSC", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.GLOBAL_FONT, 14, "bold"))
        self.osc_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.mainOscShapeSelector = OscShapeSelector(self.osc_frame)
        self.mainOscShapeSelector.grid(row=1, column=0, sticky="nw")

        # Harmonic Frame 
        self.harmonics_frame = customtkinter.CTkFrame(self,fg_color=const.BG_FRAME)
        self.harmonics_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.harmonics_label = customtkinter.CTkLabel(
            self.harmonics_frame, text="Harmonics", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.GLOBAL_FONT, 14, "bold"))
        self.harmonics_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw", columnspan=2)

        self.harmonicValues = ["H1", "H2", "H3", "H4", "H5", "H5"]
        self.harmonicCheckboxes = []

        j=0
        for i, value in enumerate(self.harmonicValues):
            checkbox = customtkinter.CTkCheckBox(
                self.harmonics_frame,
                text=value,
                text_color=const.GLOBAL_FONT_COLOR,
                border_color=const.GLOBAL_LINE_COLOR,
                hover_color=const.BG_FLASHY,
                fg_color=const.BG_FLASHY
            )
            checkbox.grid(row=j+1, column=i-(2*j), padx=2, pady=2, sticky="w")
            if (i+1) % 2 == 0:
                j += 1
            self.harmonicCheckboxes.append(checkbox)

        # LFO Frame
        self.lfo_frame = customtkinter.CTkFrame(self,fg_color=const.BG_FRAME)
        self.lfo_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew", rowspan=2)

        self.lfo_frame.grid_columnconfigure(0, weight=1)

        self.lfo_label = customtkinter.CTkLabel(
            self.lfo_frame, text="LFO", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.GLOBAL_FONT, 14, "bold"))
        self.lfo_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lfoOscShapeSelector = OscShapeSelector(self.lfo_frame)
        self.lfoOscShapeSelector.grid(row=1, column=0, sticky="nw")

        self.lfoSegmented_button = customtkinter.CTkSegmentedButton(
            self.lfo_frame, 
            values=["Amp", "Pitch"],
            selected_color = const.BG_FLASHY,
            unselected_color = const.GLOBAL_LINE_COLOR,
            fg_color = const.GLOBAL_LINE_COLOR,
            selected_hover_color = const.BG_FLASHY,
            #,command=segmented_button_callback
            )
        self.lfoSegmented_button.set("Amp")
        self.lfoSegmented_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.lfo_speed_label = customtkinter.CTkLabel(
            self.lfo_frame, text="Speed : ", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.GLOBAL_FONT, 12))
        self.lfo_speed_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")

        self.lfo_speed_slider = customtkinter.CTkSlider(self.lfo_frame, 
                                         from_=0, 
                                         to=100,
                                         button_color=const.BG_FLASHY,
                                         button_hover_color=const.BG_FLASHY_PLUS,
                                         fg_color=const.GLOBAL_LINE_COLOR,
                                         progress_color=const.BG_FLASHY
                                         #, command=slider_event
                                         )

        self.lfo_speed_slider.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.lfo_mix_label = customtkinter.CTkLabel(
            self.lfo_frame, text="Mix : ", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.GLOBAL_FONT, 12))
        self.lfo_mix_label.grid(row=5, column=0, padx=5, pady=5, sticky="nw")

        self.lfo_mix_slider = customtkinter.CTkSlider(self.lfo_frame, 
                                         from_=0, 
                                         to=100,
                                         button_color=const.BG_FLASHY,
                                         button_hover_color=const.BG_FLASHY_PLUS,
                                         fg_color=const.GLOBAL_LINE_COLOR,
                                         progress_color=const.BG_FLASHY
                                         #, command=slider_event
                                         )

        self.lfo_mix_slider.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # Man Frame
        self.man_frame = customtkinter.CTkFrame(self,fg_color=const.BG_FRAME)
        self.man_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.man_frame.grid_columnconfigure(0, weight=1)
        self.man_frame.grid_rowconfigure(0, weight=1)

        self.manlabel_label = customtkinter.CTkLabel(
            self.man_frame, text="|  | r|  | t|  |  | u|  | i|  | o|  |  |  \n|  |__|  |__|  |  |__|  |__|  |__|  |  |_ \n|  d |  f |  g |  h |  j  |  k  | l |  m |\n|____|____|____|____|_____|_____|___|____|\n", fg_color="transparent", 
            text_color=const.GLOBAL_FONT_COLOR, font=(const.FIXED_FONT, 16))
        self.manlabel_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


        # Keyboard bind
        self.bind('<KeyPress>', lambda event:self.key_press(event, self.synth))
        self.bind('<KeyRelease>', lambda event:self.key_released(event, self.synth) )

    def button_callback(self):
        print("button pressed")

    def key_press(self,event,synth):
        #print("press", event.char, event.keysym, event.keycode)
        try:
            k = event.char
        except AttributeError:
            return
        if k in const.KEY_TO_MIDI:
            synth.note_on(k, const.KEY_TO_MIDI[k])

    def key_released(self,event,synth):
        #print("release" , event.char, event.keysym, event.keycode)
        try:
            k = event.char
        except AttributeError:
            return
        if k in const.KEY_TO_MIDI:
            synth.note_off(k, const.KEY_TO_MIDI[k])



def main():
    app = SynthApp()
    app.mainloop()

if __name__ == "__main__": main()