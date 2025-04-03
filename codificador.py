import time
cod_Input = ""
while cod_Input != "quit":
    cod_Input = input("codificador >> ")
    if cod_Input == "quit":
        print("Saliendo...")
        time.sleep(2)
        print("Gracias por usar el codificador")