import tkinter as tk

class VentanaModule:

    SLIDERS = []

    def __init__(self, root:tk.Tk, octava:int,
                 updateOctavaFunc:callable,
                 updateArmonicosFunc:callable,
                 updateAddArmonicFunc:callable,
                 updateDelArmonicFunc:callable):
        self.ROOT = root
        self.OCTAVA = octava
        self.UpdateOctavaFunc = updateOctavaFunc
        self.UpdateArmonicosFunc = updateArmonicosFunc
        self.UpdateAddArmonicFunc = updateAddArmonicFunc
        self.UpdateDelArmonicFunc = updateDelArmonicFunc

    def __armoInit(self):
        new_slide = tk.Scale(
            from_=100,
            to=0,
            length=200,
            orient="vertical",
            resolution=5,
            relief="groove",
        )
        new_slide.config(
            command= lambda value: (self.UpdateArmonicosFunc(float(value),0))
        )
        new_slide.place(x=50, y=50)
        self.SLIDERS.append(new_slide)

    def __oct_change(self, n:int, label:tk.Label):
        if n == 1 and self.OCTAVA != 8:
            self.OCTAVA += 1
        elif n == 2 and self.OCTAVA != 1:
            self.OCTAVA -= 1
        label.config(text=str(self.OCTAVA))
        self.UpdateOctavaFunc(self.OCTAVA)

    def poner_armo(self):
        index = len(self.SLIDERS)
        self.UpdateAddArmonicFunc()

        if index == 14:
            None
        else:
            new_slide = tk.Scale(
                from_=100,
                to=0,
                length=200,
                orient="vertical",
                resolution=5,
                relief="groove",
            )
            new_slide.config(
                command= lambda value: (self.UpdateArmonicosFunc(float(value),index))
            )
            new_slide.place(x=50 + index * 70, y=50)
            self.SLIDERS.append(new_slide)

    def quitar_armo(self):
        if len(self.SLIDERS) > 1:
            self.UpdateDelArmonicFunc()
            slide_remove = self.SLIDERS.pop()
            slide_remove.destroy()


    def drawKeys(self, notas_negras:list[str], notas_freq:dict[float], botones:dict[tk.Button], frame:tk.Tk) -> None:
        auxIdx = [1, 3, 6, 8, 10]
        for idx, key in enumerate(notas_freq):
            btn = tk.Button(
                frame,
                text=key.upper(),
                bg="black" if key in notas_negras else "white",
                fg="white" if key in notas_negras else "black",
                activebackground="grey",
                height=8,
                width= 5,
                relief="solid",
                borderwidth=1,
                state="disabled"
            )
            botones[key] = btn
            btn.place(x=30 + idx * 50,
                      y= 330 if idx in auxIdx else 430)  # space buttons horizontally
    
    def drawInterfaz(self):
        frame_top = tk.Frame(
            self.ROOT,
            width=1000,
            height=250,
            borderwidth=2,
            relief="solid"
        )

        octLbl = tk.Label(
            self.ROOT,
            text= str(self.OCTAVA),
            relief="groove",
            width=3,
            height=2,
        )

        octup = tk.Button(self.ROOT,
            text="+",
            bg="blue",
            fg="white",
            width=3,
            height=1,
            font=("Arial",15, "bold"),
            command=lambda: self.__oct_change(1, octLbl)
        )

        octdw = tk.Button(self.ROOT,
            text="-",
            bg="blue",
            fg="white",
            width=3,
            height=1,
            font=("Arial",15, "bold"),
            command=lambda: self.__oct_change(2, octLbl)
        )

        arma = tk.Button(self.ROOT,
            text="+",
            bg="red",
            fg="black",
            width=3,
            height=1,
            font=("Arial",15, "bold"),
            command= lambda: self.poner_armo()
        )

        armq = tk.Button(self.ROOT,
            text="-",
            bg="red",
            fg="black",
            width=3,
            height=1,
            font=("Arial",15, "bold"),
            command= lambda: self.quitar_armo()
        )

        self.__armoInit()

        frame_top.place(x=30,y=30)

        octdw.place(x=950,y=475)
        octup.place(x=1000,y=475)

        octLbl.place(x=945, y=425)

        arma.place(x=450, y=284)
        armq.place(x=500, y=284)

        label = tk.Label(self.ROOT,
                         text="Añade armónicos con los botones Rojos\nCambia la octava con los botones azules"
                        )
        label.pack(pady=20)
