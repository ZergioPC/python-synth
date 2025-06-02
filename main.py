import tkinter as tk
import sounddevice as sd
import numpy as np
from src import Audio
from src import Ventana

if __name__ == "__main__":
    GLOBAL_OCTAVA = 5

    AudioControler = Audio.AudioModule()
    AudioControler.sfx_updateOctava(GLOBAL_OCTAVA)

    root = tk.Tk()
    root.title("Sintetizador de Teclado")
    root.geometry("1075x600")

    def updateGlobalOctava(uiReff:int):
        global GLOBAL_OCTAVA
        GLOBAL_OCTAVA = uiReff
        AudioControler.sfx_updateOctava(GLOBAL_OCTAVA)

    def updateArmonicos(value:float, idx:int):
        AudioControler.ARMONICOS[idx] = value

    UiControler = Ventana.VentanaModule(
        root, GLOBAL_OCTAVA,
        updateGlobalOctava,
        updateArmonicos,
        AudioControler.UI_armonico_add,
        AudioControler.UI_armonico_del
        )
    UiControler.drawInterfaz()
    UiControler.drawKeys(
        AudioControler.NOTAS_NEGRAS,
        AudioControler.NOTAS,
        AudioControler.UI_BTN_NOTAS,
        root
    )

    root.bind("<KeyPress>", AudioControler.sfx_on_key_press)
    root.bind("<KeyRelease>", AudioControler.sfx_on_key_release)

    root.mainloop()