# Tu código original aquí
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
        print(f"Error Lexicografico: Carácter No Valido '{CadFuente[PosActual]}'")  # Carácter No Valido
    token = ""

def procesar_codigo(codigo_fuente):
    global CadFuente, PosActual, token
    CadFuente = codigo_fuente.strip()
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
    print(mensaje)

# Ejemplo de uso
codigo_fuente = """
entero a
entero b,c=3
real x,suma,y = 4.8
si a>b
    b = c+1
    mientras x<8
        a = b+y
        x = x+1
    finmientras
finsi
"""
procesar_codigo(codigo_fuente)
