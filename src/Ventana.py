import numpy as np
import sounddevice as sd
import tkinter as tk
import threading

SAMPLE_RATE = 44100
KEYS_PRESSED_COUNTER = 0

KEY_FREQUENCIES = {
    'a': 261.63,  # Do
    's': 293.66,  # Re
    'd': 329.63,  # Mi
    'f': 349.23,  # Fa
    'g': 392.00,  # Sol
    'h': 440.00,  # La
    'j': 493.88,  # Si
    #'k': 523.25,  # Do (octava superior)
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
            KEY_BUTTONS[key].config(bg="white")

oct = 1

def oct_change(n):
    global oct
    if n == 1 and oct != 8:
        oct += 1
    elif n == 2 and oct != 1:
        oct -= 1
    octLbl.config(text=str(oct))

root = tk.Tk()
root.title("Sintetizador de Teclado")
root.geometry("1075x600")


for idx, key in enumerate(KEY_FREQUENCIES):
    btn = tk.Button(
        root,
        text=key.upper(),
        bg="white",
        activebackground="grey",
        width=15,
        height=15,
        relief="solid",
        borderwidth=1,
        state="disabled",
    )
    btn.place(x=30 + idx * 110, y=330)  # space buttons horizontally
    KEY_BUTTONS[key] = btn

frame_top = tk.Frame(
    root,
    width=1000,
    height=250,
    borderwidth=2,
    relief="solid"
)

frame_top.place(x=30,y=30)

slide = tk.Scale(
    from_=100,
    to=0,
    length=200,
    orient="vertical",
    resolution=10,
    relief="groove"
)

slide.place(x=50, y=50)

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

octLbl.place(x=985, y=425)

arma = tk.Button(root,

)

armq = tk.Button(root,

)

label = tk.Label(root, text="Presiona teclas (a - k) para tocar notas.")
label.pack(pady=20)

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

root.mainloop()
