from modules.tools import vig_matrix
import os
def main():
    print("Bienvenido al Codificador/Decodificador")
    print("-----------------------------------------------")
    print("----------------- Autores ---------------------")
    print("-----------------------------------------------")
    print("- Edson Joao Andrés Pereira Alvarado - 25000144")
    print("- Edgar Andrés Ozaeta Alvarado - 25000137")
    print("")
    print("")

    
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
            

            
        #Comando encode-text: toma la llave de encriptacion para manipular el texto que se envie junto con el comando
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
        
        
        #Comando decode-text: toma la llave actual y el texto codificado para devolver el texto original  
        # (devuelve un sinsentido si la llave no es la misma que la del momento de encriptacion)
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

        elif len(comando) > 12 and comando[:11] == "encode-file" and comando[11] == ' ':
            llave_or_arc = comando[11:].strip().split()
            if len(llave_or_arc) == 2:
                if '.' in llave_or_arc[1]:
                    llave_comm = llave_or_arc[0].lower()
                    archivo = llave_or_arc[1]
            elif len(llave_or_arc) == 1:
                llave_comm = llave_actual
                archivo = llave_or_arc[0]
            else:
                    print('No hay parametros!')
                    continue
                
            if llave_comm == ' ':
                    print('ERROR! Falta establecer una llave')
            else:
                    sent, prompt = encodeFiles(archivo, llave_comm, matriz_vigenere)
                    if sent == True:
                        print(f'resultado >> {prompt}')
                    else:
                        print(f'ERROR! {prompt}')


        elif len(comando) > 12 and comando[:11] == "decode-file" and comando[11] == ' ':
            llave_or_arc = comando[11:].strip().split()
            if len(llave_or_arc) == 2:
                if '.' in llave_or_arc[1]:
                    llave_comm = llave_or_arc[0].lower()
                    archivo = llave_or_arc[1]
            elif len(llave_or_arc) == 1:
                llave_comm = llave_actual
                archivo = llave_or_arc[0]
            else:
                    print('No hay parametros!')
                    continue
                
            if llave_comm == ' ':
                    print('ERROR! Falta establecer una llave')
            else:
                    sent, prompt = decodeFiles(archivo, llave_comm, matriz_vigenere)
                    if sent == True:
                        print(f'resultado >> {prompt}')
                    else:
                        print(f'ERROR! {prompt}')
        else:
                print("ERROR! Expresion no valida")       

                   
#Función encargada de la codificación de los textos
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

#Fuuncion para codificar texto de archivos y los mismos archivos (tenes que tener el archivo ya hecho con texto ya puesto)
def encodeFiles(archivo, llave, matriz):
    if not os.path.exists(archivo):
        return False, f"Tu archivo {archivo} parece no existir. Revisa su localización o si lo escribiste de manera correcta."
    if archivo.lower().endswith('.txt') == False:
        return False, f"Tu archivo {archivo} no es un archivo de texto con la extensión .txt, por lo que no podemos procesarlo."
    
    open_arc = open(archivo, 'r')

    contents = open_arc.read()

    encr_contents = codificar(contents, llave, matriz)
    nom_base = os.path.splitext(archivo)[0]
    arc_output = f"{nom_base}.gcf"
    
    cont = 1
    while os.path.exists(arc_output):
        arc_output = f"{nom_base}({cont}).gcf"
        cont += 1

    open_arc = open(arc_output, 'w')
    open_arc.write(encr_contents)

    return True, arc_output

def decodeFiles(archivo, llave, matriz):
    if not os.path.exists(archivo):
        return False, f"Tu archivo {archivo} parece no existir. Revisa su localización o si lo escribiste de manera correcta."
    if not archivo.lower().endswith('.gcf'):
        return False, f"Tu archivo {archivo} no es un archivo de texto con la extensión .gcf, por lo que no podemos procesarlo."
    
    open_arc = open(archivo, 'r')
    contents = open_arc.read()
    open_arc.close()

    decr_contents = decodificar(contents, llave, matriz)
    nom_base = os.path.splitext(archivo)[0]
    arc_output = f"{nom_base}-decoded.txt"
    
    cont = 1
    while os.path.exists(arc_output):
        arc_output = f"{nom_base}-decoded({cont}).txt"
        cont += 1
    
    open_arc = open(arc_output, 'w')
    open_arc.write(decr_contents)
    open_arc.close()


    
    return True, arc_output



main()