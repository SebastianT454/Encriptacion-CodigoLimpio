#////////////////////////////// IMPORTS //////////////////////////////////////////////
import sys
sys.path.append("src")

import numpy as np
from Encryption.EncryptionLogic import *

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

class UI_GenerateKey:
    """
    Se define una clase general para todo lo relacionado en la generacion
    De claves manuales o automaticas --> hill_genkey(numero)
    """

    @staticmethod
    def Mostrar_error(err):
        print(" ")
        print("Error:", err)
        print(" ")

    @staticmethod
    def UI_GetMatrixSize():
        while True:
            try:
                # Obtaining the size of the matrix, it will be nxn.
                MatrixSize = input("Ingrese el tamano de la matrix: ")
                
                if not MatrixSize.isdigit():
                    raise Exception(f"El tamano de la clave no es un entero." )
                
                MatrixSize = int(MatrixSize)

                if MatrixSize > 5 or MatrixSize < 2:
                    raise Exception(f"El tamano de la clave no puede ser mayor a 5 y menor que 2." )
                
                break  # Exit the loop if successful conversion
            except Exception as err:
                UI_GenerateKey.Mostrar_error( err )

        print(f"La matrix tendra la misma cantidad de columnas y filas, {MatrixSize}")
        print(" ")
        return MatrixSize

    @staticmethod
    def UI_ManualKey(MatrixSize):
        """
        Funcion que verifica si la clave es valida para generarse.
        """
        TamanoClave = MatrixSize

        print("La clave debe estar en el formato 1,2,3,4.. n")
        print("La cantidad de elementos debe ser igual al tamaño de la matrix ^ 2")
        Clave = input("Ingrese la clave: ")

        try:
            # Verificar que la clave tenga algo.
            if len(Clave) == 0:
                raise Exception(f"La clave no tiene nada, esta vacia." )
            
            # Obteniendo el tamaño de la matrix
            Tamano_matrix = int(TamanoClave) ** 2
            # Obteniendo la cantidad de enteros en la clave
            Cnt_enteros = 0

            # Seperar todos los elementos en una lista, se separa cuando se encuentre una coma.
            Lista_string = Clave.split(",")
            Lista_string = [elemento.strip() for elemento in Lista_string] # Eliminando todos los espacios vacios que hayan.

            # Obtener la cantidad de elementos y verificar si es un entero.
            for Elemento in Lista_string:
                if Elemento.isdigit():
                    Cnt_enteros += 1
                else:
                    raise ValueError(f"Hay elementos que no son entero o están vacios.")

            # Verificar que la clave tenga la cantidad suficiente de elementos.
            if Cnt_enteros != Tamano_matrix:
                raise ValueError(f"Elementos incompletos (se necesitan {Tamano_matrix} enteros y {Tamano_matrix-1} comas) NO puede ser mayor o menor.")

            return Clave
        
        except Exception as err:
            UI_GenerateKey.Mostrar_error(err)
            return False

    @staticmethod
    def UI_GenerateManualKey(MatrixSize, Key):
        TamanoClave = MatrixSize
        Clave = Key

        # Transformar cada elemento a entero.
        Lista_string = Clave.split(",")
        Lista_enteros = [int(elemento) for elemento in Lista_string]

        Clave_Matrix = []

        for _ in range(TamanoClave):
            ListaFila = []
            for _ in range(TamanoClave):
                Entero = Lista_enteros.pop(0)
                ListaFila.append(Entero)
            # Append the row to the Key
            Clave_Matrix.append(ListaFila)

        return Clave_Matrix

    @staticmethod
    def UI_GetManualKeyMatrix(MatrixSize):
        """Creats a manual key with the format 1,2,3,4"""
        ClaveManual = UI_GenerateKey.UI_ManualKey(MatrixSize)

        try:
            if ClaveManual:
                ClaveMatrix = UI_GenerateKey.UI_GenerateManualKey(MatrixSize, ClaveManual)
                return ClaveMatrix
            else:
                raise Exception(f"No se pudo generar la clave manual.." )
        
        except Exception as err:
            UI_GenerateKey.Mostrar_error(err)
            return UI_GenerateKey.UI_GetManualKeyMatrix(MatrixSize)
    
    @staticmethod
    def UI_GetAutomaticKeyMatrix(MatrixSize):
        print("Creando de forma automatica clave...")
        Key = hill_genkey(MatrixSize)
        Key = np.matrix.tolist(Key)

        return Key
    
    @staticmethod
    def Create_key(size):
        """Prompts user to create a key matrix (manual or automatic)."""
        while True:
            choice = input("Ingresar 'm' para ingresar la clave manualmente o 'a' de forma automatica: ")
            if choice == 'm':
                return UI_GenerateKey.UI_GetManualKeyMatrix(size)
            elif choice == 'a':
                return UI_GenerateKey.UI_GetAutomaticKeyMatrix(size)
            else:
                print("Opcion invalida. Escribir 'm' o 'a'.")