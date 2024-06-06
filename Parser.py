PalabrasReservadas = ["entero", "real", "si", "mientras", "finmientras", "finsi"]

tokenSimbolos = []
tokenNumeros = []
tokenIdentificadores = []
declaracionesEncontradas = []
palabrasReservadasEncontradas = []
codigo = []
stack = []

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
            print("Error: 'finsi' sin 'si' correspondiente")
    elif palabra == "finmientras":
        if stack and stack[-1] == "mientras":
            stack.pop()
        else:
            print("Error: 'finmientras' sin 'mientras' correspondiente")

def imprimirTokens(titulo, tokens):
    print(f"\n-----------------------\n|{titulo}|\n-----------------------")
    for i, token in enumerate(tokens):
        print(f"{i + 1} {token}")

# Simulación de la lectura del archivo
entrada = """entero a
entero b,c=3
real x,suma,y = 4.8

si a>b
    b = c+1
    mientras x<8
        a = b+y
        x = x+1
    finmientras
finsi"""

lineas = entrada.split('\n')

for linea in lineas:
    procesarLinea(linea)

# Imprimir resultados
imprimirTokens("DECLARACIONES ENCONTRADAS", declaracionesEncontradas)
imprimirTokens("PALABRAS RESERVADAS ENCONTRADAS", palabrasReservadasEncontradas)
imprimirTokens("CODIGO", codigo)



# Verificar si la pila está vacía al final
if stack:
    print("Error: Estructuras de control sin cerrar correctamente:", stack)
else:
    print("Estructuras de control cerradas correctamente")