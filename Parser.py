import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Definiciones de palabras clave y listas de resultados
PalabrasReservadas = ["entero", "real", "si", "mientras", "finmientras", "finsi"]
tokenSimbolos = []
tokenNumeros = []
tokenIdentificadores = []
declaracionesEncontradas = []
palabrasReservadasEncontradas = []
codigo = []
stack = []

# Funciones de verificación
def verificarNumero(palabra):
    estado = 0
    for p in palabra:
        if estado == 0:
            if p.isdigit():
                estado = 0
            elif p == '.':
                estado = 1
            else:
                return False
        elif estado == 1:
            if p.isdigit():
                estado = 1
            else:
                return False
    return True

def verificarIdentificador(palabra):
    if palabra[0].isalpha() or palabra[0] == '_':
        for p in palabra[1:]:
            if not (p.isalpha() or p.isdigit() or p == '_'):
                return False
        return True
    return False

def verificarReservada(palabra):
    return palabra in PalabrasReservadas

def verificarDeclaracion(linea):
    tipos_datos = ["entero", "real"]
    for tipo in tipos_datos:
        if linea.startswith(tipo):
            return True
    return False

# Procesamiento de líneas
def procesarLinea(linea):
    tokens = linea.split()
    if not tokens:
        return
    primer_token = tokens[0]

    if verificarDeclaracion(linea):
        declaracionesEncontradas.append(linea.strip())
    elif verificarReservada(primer_token):
        palabrasReservadasEncontradas.append(primer_token)
        manejarEstructuraControl(primer_token)
    else:
        codigo.append(linea.strip())

def manejarEstructuraControl(palabra):
    if palabra in ["si", "mientras"]:
        stack.append(palabra)
    elif palabra == "finsi":
        if stack and stack[-1] == "si":
            stack.pop()
        else:
            messagebox.showerror("Error", "'finsi' sin 'si' correspondiente")
    elif palabra == "finmientras":
        if stack and stack[-1] == "mientras":
            stack.pop()
        else:
            messagebox.showerror("Error", "'finmientras' sin 'mientras' correspondiente")

def procesarCodigo():
    entrada = textoEntrada.get("1.0", tk.END).strip().split('\n')
    
    # Resetear listas
    declaracionesEncontradas.clear()
    palabrasReservadasEncontradas.clear()
    codigo.clear()
    stack.clear()
    
    for linea in entrada:
        procesarLinea(linea)
    
    # Actualizar resultados
    textoDeclaraciones.config(state=tk.NORMAL)
    textoDeclaraciones.delete("1.0", tk.END)
    imprimirTokens("DECLARACIONES ENCONTRADAS", declaracionesEncontradas, textoDeclaraciones)
    textoDeclaraciones.config(state=tk.DISABLED)
    
    textoReservadas.config(state=tk.NORMAL)
    textoReservadas.delete("1.0", tk.END)
    imprimirTokens("PALABRAS RESERVADAS ENCONTRADAS", palabrasReservadasEncontradas, textoReservadas)
    textoReservadas.config(state=tk.DISABLED)
    
    textoCodigo.config(state=tk.NORMAL)
    textoCodigo.delete("1.0", tk.END)
    imprimirTokens("CODIGO", codigo, textoCodigo)
    textoCodigo.config(state=tk.DISABLED)
    
    # Verificar si la pila está vacía al final
    if stack:
        messagebox.showerror("Error", f"Estructuras de control sin cerrar correctamente: {stack}")
    else:
        messagebox.showinfo("Éxito", "Estructuras de control cerradas correctamente")

def imprimirTokens(titulo, tokens, textoWidget):
    textoWidget.insert(tk.END, f"\n-----------------------\n|{titulo}|\n-----------------------\n")
    for i, token in enumerate(tokens):
        textoWidget.insert(tk.END, f"{i + 1} {token}\n")

# Interfaz gráfica con ttk
root = tk.Tk()
root.title("Analizador de Código")

# Centrarse y establecer tamaño de la ventana
ancho_ventana = 1000  # Ancho
alto_ventana = 600  # Alto
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
x_pos = (ancho_pantalla // 2) - (ancho_ventana // 2)
y_pos = (alto_pantalla // 2) - (alto_ventana // 2)
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Estilo
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TFrame", padding=10)

# Frame de entrada
frameEntrada = ttk.Frame(root)
frameEntrada.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

labelEntrada = ttk.Label(frameEntrada, text="Ingrese el código fuente:")
labelEntrada.pack(pady=5)

textoEntrada = scrolledtext.ScrolledText(frameEntrada, width=120, height=10, font=("Consolas", 11))
textoEntrada.pack(pady=5)

botonProcesar = ttk.Button(frameEntrada, text="Procesar Código", command=procesarCodigo)
botonProcesar.pack(pady=10, side=tk.RIGHT)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=10, pady=10)

# Frame de resultados
frameResultados = ttk.Frame(root)
frameResultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame de declaraciones encontradas
frameDeclaraciones = ttk.Labelframe(frameResultados, text="Declaraciones Encontradas", padding=10)
frameDeclaraciones.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

textoDeclaraciones = scrolledtext.ScrolledText(frameDeclaraciones, width=40, height=20, state=tk.DISABLED, font=("Consolas", 11))
textoDeclaraciones.pack(padx=5, pady=5)

# Frame de palabras reservadas encontradas
frameReservadas = ttk.Labelframe(frameResultados, text="Palabras Reservadas Encontradas", padding=10)
frameReservadas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

textoReservadas = scrolledtext.ScrolledText(frameReservadas, width=40, height=20, state=tk.DISABLED, font=("Consolas", 11))
textoReservadas.pack(padx=5, pady=5)

# Frame de código encontrado
frameCodigo = ttk.Labelframe(frameResultados, text="Código", padding=10)
frameCodigo.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

textoCodigo = scrolledtext.ScrolledText(frameCodigo, width=40, height=20, state=tk.DISABLED, font=("Consolas", 11))
textoCodigo.pack(padx=5, pady=5)

# Menú de la aplicación
menuBar = tk.Menu(root)
root.config(menu=menuBar)

# Menú "Archivo"
fileMenu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Archivo", menu=fileMenu)
fileMenu.add_command(label="Salir", command=root.quit)

root.mainloop()

