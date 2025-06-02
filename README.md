# 🎹 Python Synth

**Python Synth** es un sintetizador de audio en tiempo real desarrollado en Python. Utiliza `sounddevice`, `numpy` y `tkinter` para generar sonidos mediante síntesis aditiva con armónicos personalizados. Cuenta con una interfaz gráfica que permite tocar notas desde el teclado o mediante botones interactivos.

---

## 🚀 Características

* ✅ Reproducción de notas musicales en tiempo real.
* ✅ Síntesis aditiva basada en series de Fourier.
* ✅ Interfaz gráfica con botones que responden a eventos de teclado y mouse.

---

## 🖥️ Requisitos

* Python 3.8 o superior

Instala las dependencias utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### En caso de no estar Tkinter instalado ⚠️

* **Windows**

  ```bash
  pip install tk
  ```

* **Debian/Ubuntu**

  ```bash
  sudo apt update
  sudo apt install python3-tk
  ```

* **Fedora**

  ```bash
  sudo dnf install python3-tkinter
  ```

* **Arch Linux**

  ```bash
  sudo pacman -S tk
  ```

* **CentOS/RHEL**

  ```bash
  sudo yum install python3-tkinter
  ```

* **macOS (con Homebrew)**

  ```bash
  brew install python-tk
  ```

---

## 🎛️ Uso

1. Clona el repositorio:

   ```bash
   git clone https://github.com/ZergioPC/python-synth.git
   cd python-synth
   ```

2. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

3. Interactúa con la interfaz gráfica:

   * Presiona las teclas asignadas para tocar notas.
   * Haz clic en los botones para generar sonidos.

---

## 📬 Contacto

Hecho por:

* 🦊 Juan Pablo Zorro
* 🧑🏻‍💻 Sergio Danilo Palacios

Para preguntas o sugerencias, puedes abrir un [Issue](https://github.com/ZergioPC/python-synth/issues) en el repositorio.