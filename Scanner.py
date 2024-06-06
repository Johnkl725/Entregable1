import tkinter as tk
from tkinter import scrolledtext, messagebox

def scanner():
    global CadFuente, PosActual, token
    token = ""
    palabras_reservadas = ['entero', 'real', 'si', 'sino', 'fun', 'finsi', 'mientras', 'finmientras']
    while PosActual < len(CadFuente) and CadFuente[PosActual] in [' ', '\n', '\t']:  # Ignorar espacios en blanco y saltos de línea
        PosActual += 1
    if PosActual >= len(CadFuente):  # Si hemos llegado al final de la cadena, terminamos
        return
    elif CadFuente[PosActual].isalpha():  # Si es una letra ==> ID
        while PosActual < len(CadFuente) and CadFuente[PosActual].isalnum():  # Si es letra o dígito
            token += CadFuente[PosActual]
            PosActual += 1
        if token in palabras_reservadas:
            mostrar_resultado(f"Palabra reservada: {token}")
        elif PosActual < len(CadFuente) and CadFuente[PosActual] == '(':
            mostrar_resultado(f"Función: {token}")
        else:
            mostrar_resultado(f"Variable: {token}")
    elif CadFuente[PosActual].isdigit():  # Si es un dígito ==> NUM
        while PosActual < len(CadFuente) and (CadFuente[PosActual].isdigit() or CadFuente[PosActual] == '.'):  # Si es dígito o punto
            token += CadFuente[PosActual]
            PosActual += 1
        mostrar_resultado(f"Número: {token}")
    elif CadFuente[PosActual] in ['+', '-', '*', '/', '(', ')', ':', ',', '>', '<', '=']:  # Operador de 1 carácter
        mostrar_resultado(f"Operador: {CadFuente[PosActual]}")
        PosActual += 1
    elif CadFuente[PosActual] in ["'", '"']:  # Si es una cadena de texto
        end_char = CadFuente[PosActual]
        PosActual += 1
        while PosActual < len(CadFuente) and CadFuente[PosActual] != end_char:
            token += CadFuente[PosActual]
            PosActual += 1
        if PosActual < len(CadFuente):  # Verificar si aún estamos dentro del rango
            PosActual += 1  # Saltar el carácter final de la cadena
        mostrar_resultado(f"Cadena: {token}")
    else:
        messagebox.showerror("Error Lexicografico", f"Carácter No Valido '{CadFuente[PosActual]}'")  # Carácter No Valido
    token = ""

def procesar_codigo():
    global CadFuente, PosActual, token
    CadFuente = textoEntrada.get("1.0", tk.END).strip()
    PosActual = 0
    token = ""
    textoSalida.config(state=tk.NORMAL)
    textoSalida.delete("1.0", tk.END)
    while PosActual < len(CadFuente):
        try:
            scanner()
            token = ""
        except Exception as e:
            mostrar_resultado(str(e))
            break
    textoSalida.config(state=tk.DISABLED)

def mostrar_resultado(mensaje):
    textoSalida.config(state=tk.NORMAL)
    textoSalida.insert(tk.END, mensaje + "\n")
    textoSalida.config(state=tk.DISABLED)

# Interfaz gráfica
root = tk.Tk()
root.title("Escaner de Código")
root.geometry("800x600")

frameEntrada = tk.Frame(root)
frameEntrada.pack(padx=10, pady=10)

labelEntrada = tk.Label(frameEntrada, text="Ingrese el código fuente:")
labelEntrada.pack(pady=5)

textoEntrada = scrolledtext.ScrolledText(frameEntrada, width=80, height=10)
textoEntrada.pack(pady=5)

botonProcesar = tk.Button(frameEntrada, text="Procesar Código", command=procesar_codigo)
botonProcesar.pack(pady=5)

frameSalida = tk.Frame(root)
frameSalida.pack(padx=10, pady=10)

labelSalida = tk.Label(frameSalida, text="Salida:")
labelSalida.pack(pady=5)

textoSalida = scrolledtext.ScrolledText(frameSalida, width=80, height=20, state=tk.DISABLED)
textoSalida.pack(pady=5)

root.mainloop()
