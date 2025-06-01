import tkinter as tk
import sounddevice as sd
import numpy as np
from src import Audio
#from src import Ventana

def drawKeys(notas_negras:list[str],notas_freq:dict[float], botones:dict[tk.Button], frame:tk.Tk) -> None:
    for idx, key in enumerate(notas_freq):
        btn = tk.Button(
            frame,
            text=key.upper(),
            bg="black" if key in notas_negras else "white",
            fg="white" if key in notas_negras else "black",
            activebackground="grey",
            width=5,
            height=8,
            relief="solid",
            borderwidth=1,
        )
        botones[key] = btn
        btn.place(x=30 + idx * 50, y=330)  # space buttons horizontally

def cambioDeOctava(n:int, label:tk.Label):
    global oct
    if n == 1 and oct != 8:
        oct += 1
    elif n == 2 and oct != 1:
        oct -= 1
    label.config(text=str(oct))


if __name__ == "__main__":
    GLOBAL_OCTAVA = 5

    AudioControler = Audio.AudioModule()
    AudioControler.sfx_updateOctava(GLOBAL_OCTAVA)

    root = tk.Tk()
    root.geometry("1075x600")
    root.title("Sintetizador de Teclado")

    drawKeys(AudioControler.NOTAS_NEGRAS ,AudioControler.NOTAS, AudioControler.UI_BTN_NOTAS, root)

    root.bind("<KeyPress>", AudioControler.sfx_on_key_press)
    root.bind("<KeyRelease>", AudioControler.sfx_on_key_release)

    root.mainloop()