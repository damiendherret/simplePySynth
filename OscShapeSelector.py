import customtkinter
import const

class OscShapeSelector(customtkinter.CTkFrame):

    def __init__(self, master, default_value="Sine", command=None):
        super().__init__(master)
        self.configure(fg_color=const.BG_FRAME)
        self.grid_columnconfigure(0, weight=1)

        self.variable = customtkinter.StringVar(value=default_value)

        values = ["Sine", "Square", "Saw"]


        for i, value in enumerate(values):
            self.osc_radio_1 = customtkinter.CTkRadioButton(self, 
                                                    text=value,
                                                    variable=self.variable,
                                                    value=value,
                                                    radiobutton_width=const.RADIOBUTTON_WIDTH_HEIGHT,
                                                    radiobutton_height=const.RADIOBUTTON_WIDTH_HEIGHT,
                                                    text_color=const.GLOBAL_FONT_COLOR,
                                                    border_color=const.GLOBAL_LINE_COLOR,
                                                    hover_color=const.BG_FLASHY,
                                                    fg_color=const.BG_FLASHY,
                                                    command=command)
            self.osc_radio_1.grid(row=i + 1, column=0, padx=10, sticky="w")

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)