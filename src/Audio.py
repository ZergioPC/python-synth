import numpy as np
import sounddevice as sd
import threading

class AudioModule:

    # Frecuencia de las notas musicales
    NOTAS_OG = {
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

    NOTAS_NEGRAS = ["w","e","t","y","u"]

    NOTAS = NOTAS_OG
    UI_BTN_NOTAS = {}

    KEYS_PRESSED_COUNTER = 0
    SAMPLE_RATE = 44100

    ARMONICOS = [0]

    # Estado de las teclas
    isKeyPress = {key: False for key in NOTAS}

    # Almacena los streams activos por tecla
    active_streams = {}

    def UI_armonico_add(self) -> None:
        self.ARMONICOS.append(0)
    
    def UI_armonico_del(self) -> None:
        self.ARMONICOS.pop()

    def UI_armonico_update(self, pos:int, value:int) -> None:
        self.ARMONICOS[pos] = value

    def sfx_frecuenciaMusical(self, nota:float, octava:int) -> float:
        """ 
        Retorna la frecuencia de la nota musical según
        la octava
        """
        return (nota)*(2**(octava))
    
    def sfx_updateOctava(self, octava:int) -> None:
        self.NOTAS = {key: self.sfx_frecuenciaMusical(self.NOTAS_OG[key],octava) for key in self.NOTAS_OG}

    def sfx_seriefourier(self, t:list, nota:float, armonicos:list, keyCounter:int) -> float:
        """ 
        Serie de Armónicos de Fourier para obtener el
        timbre de un instrumento
        """
        suma = 0.0
        for i, amp in enumerate(armonicos, start=1):
            suma += amp * np.sin(i * 2*np.pi*nota * t / self.SAMPLE_RATE)

        return (suma*0.1)/max(1,keyCounter)
    
    def sfx_play_loop(self, key:str) -> None:
        """
        Inicia la reproducción continua de una nota musical correspondiente a la tecla presionada.

        Este método genera una onda producto de una serie de fourier en tiempo real usando la frecuencia asociada a la tecla
        proporcionada. La onda es generada dentro de un callback que alimenta directamente al 
        dispositivo de salida de audio mediante sounddevice. La reproducción se mantiene en bucle 
        mientras la tecla esté presionada.

        Parámetros:
            key (str): Tecla presionada, que debe coincidir con una entrada en el diccionario self.NOTAS.

        Notas:
            - Usa una fase acumulada para mantener la continuidad de la onda entre llamadas al callback.
            - El audio se genera directamente en el callback, lo que evita la necesidad de precargar buffers.
            - El resultado se almacena en self.active_streams para poder detenerlo posteriormente.
            - Se espera que la variable global KEYS_PRESSED_COUNTER sea usada para controlar el volumen dinámicamente.
        """
        freq = self.NOTAS[key]
        phase = 0.0
        phase_inc = 2 * np.pi * freq / self.SAMPLE_RATE

        def callback(outdata, frames, time, status) -> None:
            nonlocal phase
            t = phase + np.arange(frames) * phase_inc
            onda = self.sfx_seriefourier(t, freq, self.ARMONICOS, self.KEYS_PRESSED_COUNTER)    # Generar la Onda con Series de Fourier
            #onda = np.sin(t)                                                                   # Prueba de funcionamiento correcto de las frecuencias
            outdata[:] = onda.reshape(-1, 1).astype(np.float32)                                 # Formato para que lo lea soundevice
            phase = t[-1] + phase_inc

        stream = sd.OutputStream(samplerate=self.SAMPLE_RATE, channels=1, callback=callback, blocksize=512, latency='low')
        self.active_streams[key] = stream
        stream.start()

    def sfx_on_key_press(self, event) -> None:
        key = event.char.lower()
        if key in self.NOTAS and not self.isKeyPress[key]:
            self.isKeyPress[key] = True
            self.KEYS_PRESSED_COUNTER += 1
            threading.Thread(target=self.sfx_play_loop, args=(key,), daemon=True).start()
            self.UI_BTN_NOTAS[key].config(bg="grey")

    def sfx_on_key_release(self, event) -> None:
        key = event.char.lower()
        if key in self.NOTAS:
            self.isKeyPress[key] = False
            self.KEYS_PRESSED_COUNTER -= 1
            if key in self.active_streams:
                self.active_streams[key].stop()
                self.active_streams[key].close()
                del self.active_streams[key]
            if key in self.NOTAS_NEGRAS:
                self.UI_BTN_NOTAS[key].config(bg="black")
            else:
                self.UI_BTN_NOTAS[key].config(bg="white")

if __name__ == "__main__":
    import tkinter as tk

    AudioControler = AudioModule()
    AudioControler.sfx_updateOctava(5)

    root = tk.Tk()
    root.title("Sintetizador de Teclado")

    label = tk.Label(root, text="Presiona teclas (a - k) para tocar notas.")
    label.pack(pady=20)

    root.bind("<KeyPress>", AudioControler.sfx_on_key_press)
    root.bind("<KeyRelease>", AudioControler.sfx_on_key_release)

    root.mainloop()