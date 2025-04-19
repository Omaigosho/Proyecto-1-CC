from modules.tools import vig_matrix

def main():
    print("Bienvenido al Codificador/Decodificador")
    print("-----------------------------------------------")
    
    # Cargar la matriz Vigenère al iniciar
    matriz_vigenere = vig_matrix()
    llave_actual = ""
    
    while True:
        print("codificador >> ", end="")
        comando = input()
        
         # Comando para salir del programa
        if comando == "quit":
            print("Saliendo ...")
            print("Gracias por usar nuestro codificador.")
            break
        
        # Comando setkey: Fija una llave de encriptación la cual se utilizará a la hora de recorrer la matriz
        if len(comando) > 7 and comando[:6] == "setkey" and comando[6] == ' ':
            llave = comando[7:]
            es_valida = True
            for letra in llave:
                if not (('A' <= letra <= 'Z') or ('a' <= letra <= 'z')):
                    es_valida = False
                    break
            
            if es_valida and llave != "":
                llave_actual = ""
                for letra in llave:
                    if 'A' <= letra <= 'Z':
                        llave_actual += chr(ord(letra) + 32)
                    else:
                        llave_actual += letra
                print("resultado >> nueva llave aceptada")
            else:
                print("ERROR! Expresion no valida")
        
        elif len(comando) > 12 and comando[:11] == "encode-text" and comando[11] == ' ':
            if llave_actual == "":
                print("ERROR! No hay llave establecida")
            else:
                texto = comando[12:]
                if texto == "":
                    print("ERROR! Texto vacio")
                else:
                    codificado = codificar(texto, llave_actual, matriz_vigenere)
                    print("resultado >> " + codificado)
        
        elif len(comando) > 12 and comando[:11] == "decode-text" and comando[11] == ' ':
            if llave_actual == "":
                print("ERROR! No hay llave establecida")
            else:
                texto = comando[12:]
                if texto == "":
                    print("ERROR! Texto vacio")
                else:
                    decodificado = decodificar(texto, llave_actual, matriz_vigenere)
                    print("resultado >> " + decodificado)

#Función encargada de la codificación de los textos (te toca ver que onda con las tildes jajajaj)
def codificar(texto, llave, matriz):
    resultado = ""
    indice_llave = 0
    
    for caracter in texto:
        if caracter.isalpha():
            es_minuscula = caracter.islower()
            letra = caracter.upper()
            clave = llave[indice_llave % len(llave)].upper()
            
            fila = ord(letra) - ord('A')
            columna = ord(clave) - ord('A')
            nuevo_caracter = matriz[fila][columna]
            
            if es_minuscula:
                nuevo_caracter = nuevo_caracter.lower()
            
            resultado += nuevo_caracter
            indice_llave += 1
        else:
            resultado += caracter
    
    return resultado

#Función encargada de la decodificación de los textos
def decodificar(texto, llave, matriz):
    resultado = ""
    indice_llave = 0
    
    for caracter in texto:
        if caracter.isalpha():
            es_minuscula = caracter.islower()
            letra = caracter.upper()
            clave = llave[indice_llave % len(llave)].upper()
            
            columna = ord(clave) - ord('A')
            # Recorremos la matriz en busca de la letra
            for fila in range(len(matriz)):
                if matriz[fila][columna] == letra:
                    nuevo_caracter = chr(fila + ord('A'))
                    break
            
            if es_minuscula:
                nuevo_caracter = nuevo_caracter.lower()
            
            resultado += nuevo_caracter
            indice_llave += 1
        else:
            resultado += caracter
    
    return resultado

main()