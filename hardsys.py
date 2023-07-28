import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import sys
import os

def is_bandit_installed():
    try:
        result = subprocess.run(["bandit", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def is_eslint_installed():
    try:
        result = subprocess.run(["eslint", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def is_safety_installed():
    try:
        result = subprocess.run(["safety", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def is_pyflakes_installed():
    try:
        result = subprocess.run(["pyflakes", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def install_bandit():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Instalando bandit...\n")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "bandit"], capture_output=True, text=True)
    result_text.insert(tk.END, result.stdout + result.stderr)
    result_text.insert(tk.END, "\nInstalación completada. Puedes analizar el código ahora.")
    result_text.config(state=tk.DISABLED)
    analyze_button.config(state=tk.NORMAL)

def install_eslint():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Instalando eslint...\n")
    result = subprocess.run([sys.executable, "-m", "npm", "install", "-g", "eslint"], capture_output=True, text=True)
    result_text.insert(tk.END, result.stdout + result.stderr)
    result_text.insert(tk.END, "\nInstalación completada. Puedes analizar el código JavaScript ahora.")
    result_text.config(state=tk.DISABLED)
    analyze_button.config(state=tk.NORMAL)

def install_safety():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Instalando safety...\n")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "safety"], capture_output=True, text=True)
    result_text.insert(tk.END, result.stdout + result.stderr)
    result_text.insert(tk.END, "\nInstalación completada. Puedes analizar la seguridad de las dependencias ahora.")
    result_text.config(state=tk.DISABLED)
    analyze_button.config(state=tk.NORMAL)

def install_pyflakes():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Instalando pyflakes...\n")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "pyflakes"], capture_output=True, text=True)
    result_text.insert(tk.END, result.stdout + result.stderr)
    result_text.insert(tk.END, "\nInstalación completada. Puedes analizar los módulos en el código Python ahora.")
    result_text.config(state=tk.DISABLED)
    analyze_button.config(state=tk.NORMAL)

def check_and_install_bandit():
    if not is_bandit_installed():
        answer = messagebox.askquestion("Instalación requerida", "bandit no está instalado en tu equipo. ¿Deseas instalarlo ahora?")
        if answer == "yes":
            install_bandit()
        else:
            messagebox.showerror("Error", "bandit es necesario para utilizar Hardsys. Por favor, instálalo manualmente.")
            sys.exit()

def check_and_install_eslint():
    if not is_eslint_installed():
        answer = messagebox.askquestion("Instalación requerida", "eslint no está instalado en tu equipo. ¿Deseas instalarlo ahora?")
        if answer == "yes":
            install_eslint()
        else:
            messagebox.showerror("Error", "eslint es necesario para analizar archivos JavaScript. Por favor, instálalo manualmente.")
            sys.exit()

def check_and_install_safety():
    if not is_safety_installed():
        answer = messagebox.askquestion("Instalación requerida", "safety no está instalado en tu equipo. ¿Deseas instalarlo ahora?")
        if answer == "yes":
            install_safety()
        else:
            messagebox.showerror("Error", "safety es necesario para analizar la seguridad de las dependencias. Por favor, instálalo manualmente.")
            sys.exit()

def check_and_install_pyflakes():
    if not is_pyflakes_installed():
        answer = messagebox.askquestion("Instalación requerida", "pyflakes no está instalado en tu equipo. ¿Deseas instalarlo ahora?")
        if answer == "yes":
            install_pyflakes()
        else:
            messagebox.showerror("Error", "pyflakes es necesario para analizar los módulos en el código Python. Por favor, instálalo manualmente.")
            sys.exit()

def analyze_code(code_path, args):
    if code_path.lower().endswith(".js"):
        if not is_eslint_installed():
            return "Error: eslint no está instalado. Instálalo para analizar archivos JavaScript."
        command = ["eslint", code_path] + args
    elif code_path.lower().endswith(".php"):
        command = ["php", "-l", code_path]
    elif code_path.lower().endswith(".sh"):
        command = ["bash", "-n", code_path]
    elif code_path.lower().endswith(".java"):
        command = ["javac", code_path]
    elif code_path.lower().endswith(".apk"):
        return "Análisis de archivos APK aún no soportado."
    elif code_path.lower().endswith(".py"):
        if not is_pyflakes_installed():
            return "Error: pyflakes no está instalado. Instálalo para analizar los módulos en el código Python."
        command = ["pyflakes", code_path]
    else:
        return "Error: Tipo de archivo no soportado. Hardsys admite archivos JavaScript (.js), PHP (.php), Bash (.sh), Java (.java), Python (.py) y APK (.apk) únicamente."
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        return "Error: No se pudo ejecutar el análisis. Asegúrate de tener las herramientas adecuadas instaladas."

def analyze_dependencies(code_path):
    try:
        result = subprocess.run(["safety", "check", "--file", code_path], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        return "Error: safety no está instalado. Instálalo para analizar la seguridad de las dependencias."

# Crear
def on_analyze_button_click():
    code_path = code_path_entry.get()
    args = args_entry.get()
    
    if not os.path.isfile(code_path):
        messagebox.showerror("Error", "El archivo seleccionado no existe.")
        return
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    
    result_text.insert(tk.END, "Analizando código...\n")
    result_text.update_idletasks()  # Actualiza la interfaz para mostrar el mensaje antes del análisis
    
    analysis_result = analyze_code(code_path, args.split())
    result_text.insert(tk.END, analysis_result)
    
    dependencies_result = analyze_dependencies(code_path)
    result_text.insert(tk.END, "\n\nAnálisis de dependencias:\n")
    result_text.insert(tk.END, dependencies_result)
    
    modules_result = analyze_modules(code_path)
    result_text.insert(tk.END, "\n\nAnálisis de módulos en código Python:\n")
    result_text.insert(tk.END, modules_result)
    
    result_text.insert(tk.END, "\nAnálisis completado.")

def on_open_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        code_path_entry.delete(0, tk.END)
        code_path_entry.insert(tk.END, file_path)

def on_save_button_click():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_text.get(1.0, tk.END))

def on_clear_button_click():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

# Crear ventana principal
window = tk.Tk()
window.title("Hardsys - Análisis de Código")
window.geometry("800x600")

# Etiqueta y entrada para el código
code_path_label = tk.Label(window, text="Ruta del archivo:")
code_path_label.pack(pady=5)

code_path_entry = tk.Entry(window, width=70)
code_path_entry.pack(pady=5)

# Botón para seleccionar archivo
open_button = tk.Button(window, text="Abrir Archivo", command=on_open_button_click)
open_button.pack(pady=5)

# Cuadro de texto para opciones adicionales de análisis
args_label = tk.Label(window, text="Opciones de análisis (separadas por espacios):")
args_label.pack(pady=5)

args_entry = tk.Entry(window, width=70)
args_entry.pack(pady=5)

# Botón para analizar el código
analyze_button = tk.Button(window, text="Analizar Código", command=on_analyze_button_click)
analyze_button.pack(pady=5)

# Cuadro de texto para mostrar resultados
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=20, state=tk.DISABLED)
result_text.pack(pady=10)

# Botón para guardar resultados en un archivo
save_button = tk.Button(window, text="Guardar Resultado", command=on_save_button_click)
save_button.pack(pady=5)

# Botón para limpiar el resultado
clear_button = tk.Button(window, text="Limpiar Resultado", command=on_clear_button_click)
clear_button.pack(pady=5)

# Verificación de herramientas instaladas
check_and_install_bandit()
check_and_install_eslint()
check_and_install_safety()
check_and_install_pyflakes()

# Ejecutar la interfaz gráfica
window.mainloop()
