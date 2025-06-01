import numpy as np
import sounddevice as sd
import tkinter as tk
import threading

SAMPLE_RATE = 44100
KEYS_PRESSED_COUNTER = 0

oct = 1

sliders = []

KEY_FREQUENCIES = {
    "a":32.7,   # Do
    "w":34.65,  # Do#
    "s":36.71,  # Re
    "e":38.89,  # Re#
    "d":41.2,   # Mi
    "f":43.65,  # Fa
    "t":46.25,  # Fa#
    "g":49.00,  # Sol
    "y":51.91,  # Sol#
    "h":55.00,  # La
    "u":58.27,  # La#
    "j":61.74,  # Si
    "k":65.42   # Do (Octava mayor)
}

KEY_BUTTONS = {}



# Estado de las teclas
isKeyPress = {key: False for key in KEY_FREQUENCIES}

# Almacena los streams activos por tecla
active_streams = {}

def generate_tone(frequency):
    t = np.linspace(0, 1, SAMPLE_RATE, False)
    wave = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    return wave

def play_loop(key):
    frequency = oct*KEY_FREQUENCIES[key]
    phase = 0.0
    phase_inc = 2 * np.pi * frequency / SAMPLE_RATE

    def callback(outdata, frames, time, status):
        nonlocal phase
        t = phase + np.arange(frames) * phase_inc
        #Aquí aplicar el volumen
        onda = np.sin(t)
        outdata[:] = onda.reshape(-1, 1).astype(np.float32) # Formato para que lo lea soundevice
        phase = t[-1] + phase_inc


    stream = sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=512, latency='low')
    active_streams[key] = stream
    stream.start()

def on_key_press(event):
    global KEYS_PRESSED_COUNTER
    key = event.char.lower()
    if key in KEY_FREQUENCIES and not isKeyPress[key]:
        isKeyPress[key] = True
        KEYS_PRESSED_COUNTER += 1
        threading.Thread(target=play_loop, args=(key,), daemon=True).start()

    if key in KEY_BUTTONS:
        KEY_BUTTONS[key].config(bg="grey")

def on_key_release(event):
    global KEYS_PRESSED_COUNTER
    key = event.char.lower()
    if key in KEY_FREQUENCIES:
        isKeyPress[key] = False
        KEYS_PRESSED_COUNTER -= 1
        if key in active_streams:
            active_streams[key].stop()
            active_streams[key].close()
            del active_streams[key]
        
        
        
        if key in KEY_BUTTONS:
            KEY_BUTTONS[key].config(bg=KEY_BUTTONS[key].original_bg)


def oct_change(n):
    global oct
    if n == 1 and oct != 8:
        oct += 1
    elif n == 2 and oct != 1:
        oct -= 1
    octLbl.config(text=str(oct))

def poner_armo():
    index = len(sliders)
    if index == 14:
        None
    else:
        new_slide = tk.Scale(
        from_=100,
        to=0,
        length=200,
        orient="vertical",
        resolution=5,
        relief="groove"
        )
        new_slide.place(x=50 + index * 70, y=50)
        sliders.append(new_slide)

def quitar_armo():
    if sliders:
        slide_remove = sliders.pop()
        slide_remove.destroy()

root = tk.Tk()
root.title("Sintetizador de Teclado")
root.geometry("1075x600")


for idx, key in enumerate(KEY_FREQUENCIES):
    if idx in [1, 3, 6, 8, 10]:
        bg_color = "black"
        act_color = "black"
    else:
        bg_color = "white"
        act_color = "grey"
    btn = tk.Button(
            root,
            text=key.upper(),
            bg=bg_color,
            width=8 if bg_color == "black" else 9,
            height=15,
            relief="solid",
            borderwidth=1,
            state="disabled"
        )
    btn.original_bg = bg_color
    btn.place(x=30 + idx * 60, y=330)  # space buttons horizontally
    KEY_BUTTONS[key] = btn

frame_top = tk.Frame(
    root,
    width=1000,
    height=250,
    borderwidth=2,
    relief="solid"
)

frame_top.place(x=30,y=30)



octup = tk.Button(root,
                  text="+",
                  bg="blue",
                  fg="black",
                  width=3,
                  height=1,
                  font=("Arial",15, "bold"),
                  command=lambda: oct_change(1)
)


octdw = tk.Button(root,
                  text="-",
                  bg="blue",
                  fg="black",
                  width=3,
                  height=1,
                  font=("Arial",15, "bold"),
                  command=lambda: oct_change(2)
)

octdw.place(x=950,y=475)
octup.place(x=1000,y=475)

octLbl = tk.Label(
    root,
    text= str(oct),
    relief="groove",
    width=3,
    height=2,
)

octLbl.place(x=945, y=425)

arma = tk.Button(root,
                text="+",
                bg="red",
                fg="black",
                width=3,
                height=1,
                font=("Arial",15, "bold"),
                command=poner_armo
)

armq = tk.Button(root,
                text="-",
                bg="red",
                fg="black",
                width=3,
                height=1,
                font=("Arial",15, "bold"),
                command=quitar_armo
)

arma.place(x=450, y=284)
armq.place(x=500, y=284)

label = tk.Label(root, text="Presiona teclas (a - k) para tocar notas.")
label.pack(pady=20)

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

root.mainloop()
