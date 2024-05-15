#////////////////////////////// IMPORTS //////////////////////////////////////////////
import sys
sys.path.append("src")

from Encryption.EncryptionLogic import *
from Gui.Console.EncryptionGUI_Console import *

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

# Funcion que muestra una excepcion por consola.
def ShowError(err):
    print(" ")
    print("Error:", err)
    print(" ")

# Funcion principal de la interfaz grafica.
def main():
    # Menu para consola

    while True:
        print("\n --- Encryptation Program --- \n")

        # Input del usuario
        while True:
            message = input("Ingresar el mensaje: ")
            if message and len(message) >= 2:
                break
            else:
                try:
                    if len(message) == 0:
                        raise Exception(f"El mensaje esta vacio." )
                    if len(message) == 1:
                        raise Exception(f"El mensaje debe tener más de un valor." )

                except Exception as err:
                    ShowError( err )

        # Mensaje formateado.
        print("Tu mensaje:", message)
        print(" ")

        # Obteniendo la clave en la consola.
        key = UI_GenerateKey.Create_key(UI_GenerateKey.UI_GetMatrixSize())
        print("\n Clave:")
        print(key)
        print(" ")

        # Teniendo un menu para escoger entre encriptar y desencriptar
        while True:
            choice = input(" Ingrese 'e' para encriptar o 'd' to desencriptar: ")

            try:
                if choice == 'e':
                    encryptedMessage = hill_cipher(message, key)
                    print("\n Mensaje Encriptado:", encryptedMessage)
                elif choice == 'd':
                    if encryptedMessage:
                        decryptedMessage = hill_decipher(encryptedMessage, key)
                    else:
                        decryptedMessage = hill_decipher(message, key)
                        
                    print("\n Mensaje Desencriptado:", decryptedMessage)
                else:
                    print("Opcion invalida, solamente es valido 'e' o 'd'.")

            except Exception as err:
                ShowError( err )

            # Acabar el programa.
            print("\n Si ingresa 'y' podra encriptar o desencriptar nuevamente.")
            choice = input("\n Quiere continuar (y/n)? ")
            print(" ")
            if choice != "y":
                print("-- EXECUTION FINISHED --")
                break

main()