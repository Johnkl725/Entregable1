import tkinter as tk
from tkinter import scrolledtext, messagebox

# Tu código original aquí
def scanner():
    global CadFuente, PosActual, token
    token = ""
    palabras_reservadas = ['Entero', 'Real', 'Si', 'Sino','Fun','FinSi','Mientras','FinMientras']
    while PosActual < len(CadFuente) and CadFuente[PosActual] in [' ', '\n', '\t']:  # ignorar espacios en blanco y saltos de línea
        PosActual += 1
    if PosActual >= len(CadFuente):  # Si hemos llegado al final de la cadena, terminamos
        return
    elif CadFuente[PosActual].isalpha():  # Si es una letra ==> ID
        while PosActual < len(CadFuente) and CadFuente[PosActual].isalnum():  # Si es letra o digito
            token += CadFuente[PosActual]
            PosActual += 1
        if token in palabras_reservadas:
            mostrar_resultado(f"Palabra reservada: {token}")
        elif CadFuente[PosActual] == '(':
            mostrar_resultado(f"Función: {token}")
        else:
            mostrar_resultado(f"Variable: {token}")
    elif CadFuente[PosActual].isdigit():  # Si es un dígito ==> NUM
        while PosActual < len(CadFuente) and (CadFuente[PosActual].isdigit() or CadFuente[PosActual] == '.'):  # Si es dígito o punto
            token += CadFuente[PosActual]
            PosActual += 1
    elif CadFuente[PosActual] in ['+', '-', '*', '/', '(', ')', ':',',','>','<','=']:  # operador de 1 caracter
        PosActual += 1
    elif CadFuente[PosActual] in ["'", '"']:  # Si es una cadena de texto
        end_char = CadFuente[PosActual]
        PosActual += 1
        while PosActual < len(CadFuente) and CadFuente[PosActual] != end_char:
            PosActual += 1
        if PosActual < len(CadFuente):  # Verificar si aún estamos dentro del rango
            PosActual += 1  # Saltar el carácter final de la cadena
    else:
        messagebox.showerror("Error Lexicografico", f"Carácter No Valido '{CadFuente[PosActual]}'")  # Carácter No Valido
    token = ""

def procesar_codigo():
    global CadFuente, PosActual, token
    CadFuente = textoEntrada.get("1.0", tk.END).strip()
    PosActual = 0
    token = ""
    while PosActual < len(CadFuente):
        try:
            scanner()
            token = ""
        except Exception as e:
            mostrar_resultado(str(e))
            break

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
