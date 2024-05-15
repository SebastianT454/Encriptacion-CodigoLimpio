#////////////////////////////// IMPORTS //////////////////////////////////////////////
import sys
sys.path.append("src")

import numpy as np
from Encryption.EncryptionLogic import *

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

class UI_GenerateKey:
    """
    Se define una clase general para todo lo relacionado en la generacion
    De claves manuales o automaticas
    """

    # Funcion que muestra por consola el error.
    @staticmethod
    def ShowError(err):
        print(" ")
        print("Error:", err)
        print(" ")

    # Funcion que obtiene por consola el tamaño de la matriz.
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
                UI_GenerateKey.ShowError( err )

        print(f"La matrix tendra la misma cantidad de columnas y filas, {MatrixSize}")
        print(" ")
        return MatrixSize

    # Funcion que obtiene de forma manual la clave para la encriptacion.
    @staticmethod
    def UI_ManualKey(MatrixSize):
        """
        Funcion que verifica si la clave es valida para generarse.
        """
        KeySize = MatrixSize

        print("La clave debe estar en el formato 1,2,3,4.. n")
        print("La cantidad de elementos debe ser igual al tamaño de la matrix ^ 2")
        Key = input("Ingrese la clave: ")

        try:
            # Verificar que la clave tenga algo.
            if len(Key) == 0:
                raise Exception(f"La clave no tiene nada, esta vacia." )
            
            # Obteniendo el tamaño de la matrix
            Matrix_Size = int(KeySize) ** 2
            # Obteniendo la cantidad de enteros en la clave
            Cnt_Integers = 0

            # Seperar todos los elementos en una lista, se separa cuando se encuentre una coma.
            StringArray = Key.split(",")
            StringArray = [Element.strip() for Element in StringArray] # Eliminando todos los espacios vacios que hayan.

            # Obtener la cantidad de elementos y verificar si es un entero.
            for Element in StringArray:
                if Element.isdigit():
                    Cnt_Integers += 1
                else:
                    raise ValueError(f"Hay elementos que no son entero o están vacios.")

            # Verificar que la clave tenga la cantidad suficiente de elementos.
            if Cnt_Integers != Matrix_Size:
                raise ValueError(f"Elementos incompletos (se necesitan {Matrix_Size} enteros y {Matrix_Size-1} comas) NO puede ser mayor o menor.")

            return Key
        
        except Exception as err:
            UI_GenerateKey.ShowError(err)
            return False

    # Funcion que transforma la clave de formato 1,2,3,4 a matriz.
    @staticmethod
    def UI_GenerateManualKey(MatrixSize, Key):
        KeySize = MatrixSize

        # Transformar cada Element a entero.
        StringArray = Key.split(",")
        IntegersArray = [int(Element) for Element in StringArray]

        MatrixKey = []

        for _ in range(KeySize):
            RowArray = []
            for _ in range(KeySize):
                Integer = IntegersArray.pop(0)
                RowArray.append(Integer)
            # Append the row to the Key
            MatrixKey.append(RowArray)

        return MatrixKey

    # Funcion que gestiona que se cree apropiadamente la clave manual.
    @staticmethod
    def UI_GetManualKeyMatrix(MatrixSize):
        """Creats a manual key with the format 1,2,3,4"""
        ManualKey = UI_GenerateKey.UI_ManualKey(MatrixSize)

        try:
            if ManualKey:
                MatrixKey = UI_GenerateKey.UI_GenerateManualKey(MatrixSize, ManualKey)
                return MatrixKey
            else:
                raise Exception(f"No se pudo generar la clave manual.." )
        
        except Exception as err:
            UI_GenerateKey.ShowError(err)
            return UI_GenerateKey.UI_GetManualKeyMatrix(MatrixSize)
    
    # Funcion que crea una matriz con valores aleatorios.
    @staticmethod
    def UI_GetAutomaticKeyMatrix(MatrixSize):
        print("Creando de forma automatica clave...")
        Key = hill_genkey(MatrixSize)
        Key = np.matrix.tolist(Key)

        return Key
    
    # Funcion que despliega las respectivas interfaces graficas para la generacion de la clave (matriz).
    @staticmethod
    def Create_key(size):
        """Avisa el usuario si quiere generar su clave de forma automatica o manual."""
        while True:
            choice = input("Ingresar 'm' para ingresar la clave manualmente o 'a' de forma automatica: ")
            if choice == 'm':
                return UI_GenerateKey.UI_GetManualKeyMatrix(size)
            elif choice == 'a':
                return UI_GenerateKey.UI_GetAutomaticKeyMatrix(size)
            else:
                print("Opcion invalida. Escribir 'm' o 'a'.")