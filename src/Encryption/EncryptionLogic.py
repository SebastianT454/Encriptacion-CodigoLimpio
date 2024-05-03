#////////////////////////////// IMPORTS //////////////////////////////////////////////
import sys
sys.path.append("src")

import numpy as np
import random
from sympy import Matrix

#////////////////////////////// CONSTANTS //////////////////////////////////////////////

Dictionary_encrypt = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 
                      'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, '0': 26, '1': 27, '2': 28, '3': 29, '4': 30,
                      '5': 31, '6': 32, '7': 33, '8': 34, '9': 35, '.': 36, ',': 37, ':': 38, '?': 39, ' ': 40, 'a': 41, 'b': 42, 'c': 43, 'd': 44, 'e': 45,
                      'f': 46, 'g': 47, 'h': 48, 'i': 49, 'j': 50, 'k': 51, 'l': 52, 'm': 53, 'n': 54, 'o': 55, 'p': 56, 'q': 57, 'r': 58, 's': 59, 't': 60,
                      'u': 61, 'v': 62, 'w': 63, 'x': 64, 'y': 65, 'z': 66}

Dictionary_decrypt = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J', '10': 'K', '11': 'L', '12': 'M',
                       '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y',
                       '25': 'Z', '26': '0', '27': '1', '28': '2', '29': '3', '30': '4', '31': '5', '32': '6', '33': '7', '34': '8', '35': '9', '36': '.',
                       '37': ',', '38': ':', '39': '?', '40': ' ', '41': 'a', '42': 'b', '43': 'c', '44': 'd', '45': 'e', '46': 'f', '47': 'g', '48': 'h',
                       '49': 'i', '50': 'j', '51': 'k', '52': 'l', '53': 'm', '54': 'n', '55': 'o', '56': 'p', '57': 'q', '58': 'r', '59': 's', '60': 't',
                       '61': 'u', '62': 'v', '63': 'w', '64': 'x', '65': 'y', '66': 'z'}

Mod_To_InvertMatrix = 67

#////////////////////////////// EXCEPTIONS //////////////////////////////////////////////

class MultiplicacionInvalidaDeMatriz(Exception):
  def __init__(self):
    super().__init__( f"Se esta multiplicando una matriz de un tamaño 1 x n columnas." )

class MatrizNoEsInvertible(Exception):
  def __init__(self):
    super().__init__( f"La invertible es 0, por lo tanto no existe (No es cuadrada o son productos iguales)" )

class MensajeVacio(Exception):
  def __init__(self):
    super().__init__( f"El mensaje no tiene nada, esta vacio." )

class CaracteresInvalidosMensaje(Exception):
  def __init__(self):
    super().__init__( f"El mensaje tiene caracteres que no están definidos en el alfabeto." )

class MensajeNoEsString(Exception):
  def __init__(self):
    super().__init__( f"El mensaje es un tipo de dato diferente de str." )

class SizeInvalida(Exception):
  def __init__(self):
    super().__init__( f"El valor dado para Size es diferente de int." )

class ClaveDemasiadoGrande(Exception):
  def __init__(self):
    super().__init__( f"El size ingresado para la clave es demasiado grande." )

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////
    
def hill_genkey(size):
    """
    Hill Key Generation
    :size: matrix size
    :return: size x size matrix containing the key
    """

    if type(size) != int:
       raise SizeInvalida

    if size > 100:
       raise ClaveDemasiadoGrande

    matrix = []

    L = []

    # Relleno una lista con tantos valores aleatorios como elementos a rellenar en la matriz determinada por size (size * size)

    for x in range(size * size):
        L.append(random.randrange(40))


    # Se crea la matrix clave con los valores generados, de tamaño size * size

    matrix = np.array(L).reshape(size, size)

    return matrix


def hill_cipher(message, key):
    """
    Hill cipher
    :message: message to cipher (plaintext)
    :key: key to use when ciphering the message (as it is returned by
          uoc_hill_genkey() )
    :return: ciphered text
    """
    #print(key)

    ciphertext = ''

    # Variables

    matrix_mensaje = []
    list_temp = []
    cifrado_final = ''
    ciphertext_temp = ''
    cont = 0

    if type(message) != str:
       raise MensajeNoEsString

    # Si el tamaño del mensaje es menor o igual al tamaño de la clave

    if len(message) <= len(key):

        # Convertir el tamaño del mensaje al tamaño de la clave, si no es igual, se añaden 'X' hasta que sean iguales los tamaños.

        while len(message) < len(key):
            message = message + 'X'

        # Crear la matriz para el mensaje

        for i in range(0, len(message)):
            try:
                matrix_mensaje.append(Dictionary_encrypt[message[i]])
            except KeyError:
                raise CaracteresInvalidosMensaje

        # Se crea la matriz

        matrix_mensaje = np.array(matrix_mensaje)

        # Se multiplica la matriz clave por la de mensaje

        cifrado = np.matmul(key, matrix_mensaje)

        # Se obtiene el Mod_To_InvertMatrix sobre el diccionario de cada celda

        cifrado = cifrado % Mod_To_InvertMatrix

        # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado

        for i in range(0, len(cifrado)):
            ciphertext += Dictionary_decrypt[str(cifrado[i])]
    else:

    # Si el tamaño del mensaje es menor o igual al tamaño de la clave

        # Si al dividir en trozos del tamaño de la clave, existe algun trozo que tiene menos caracteres que la long. de la clave se añaden tantas 'X' como falten

        while len(message) % len(key) != 0:
            message = message + 'X'

        # Se troce el mensaje en subsstrings de tamaño len(key) y se alamcenan como valores de un array

        matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                          len(message), len(key))]

        # Para cada valor del array (grupo de caracteres de la longitud de la clave)

        for bloque in matrix_mensaje:

            # Crear la matriz para el bloque

            for i in range(0, len(bloque)):
                list_temp.append(Dictionary_encrypt[bloque[i]])

            # Se crea la matriz de ese bloque

            matrix_encrypt = np.array(list_temp)

            # Se multiplica la matriz clave por la del bloque
            try:
                cifrado = np.matmul(key, matrix_encrypt)
            except Exception:
                raise MultiplicacionInvalidaDeMatriz

            # Se obtiene el Mod_To_InvertMatrix sobre el diccionario de cada celda

            cifrado = cifrado % Mod_To_InvertMatrix

            # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado

            for i in range(0, len(cifrado)):
                ciphertext_temp += Dictionary_decrypt[str(cifrado[i])]

            # Se inicializan las variables para el nuevo bloque

            matrix_encrypt = []
            list_temp = []

        # Se añade el mensaje encriptado a la variable que contiene el mensaje encriptado completo

        ciphertext = ciphertext_temp

    # --------------------------------

    return ciphertext


def hill_decipher(message, key):
    """
    Hill decipher
    :message: message to decipher (ciphertext)
    :key: key to use when deciphering the message (as it is returned by
          uoc_hill_genkey() )
    :return: plaintext corresponding to the ciphertext
    """

    plaintext = ''

    matrix_mensaje = []
    plaintext_temp = ''
    list_temp = []
    matrix_inversa = []
    matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                      len(message), len(key))]

    # Se calcula la matriz inversa aplicando el Mod_To_InvertMatrix
    try:
        matrix_inversa = Matrix(key).inv_mod(Mod_To_InvertMatrix)
    except ValueError:
        raise MatrizNoEsInvertible

    # Se transforma en una matriz

    matrix_inversa = np.array(matrix_inversa)

    # Se pasan los elementos a float

    matrix_inversa = matrix_inversa.astype(float)

    # Para cada bloque

    for bloque in matrix_mensaje:

        # Se encripta el mensaje encriptado

        for i in range(0, len(bloque)):
            list_temp.append(Dictionary_encrypt[bloque[i]])

        # Se convierte a matriz

        matrix_encrypt = np.array(list_temp)

        # Se multiplica la matriz inversa por el bloque

        cifrado = np.matmul(matrix_inversa, matrix_encrypt)

        # Se le aplica a cada elemento el Mod_To_InvertMatrix

        cifrado = np.remainder(cifrado, Mod_To_InvertMatrix).flatten()

        # Se desencripta el mensaje

        for i in range(0, len(cifrado)):
            plaintext_temp += Dictionary_decrypt[str(int(cifrado[i]))]

        matrix_encrypt = []
        list_temp = []
    plaintext = plaintext_temp

    # Se eleminan las X procedentes de su addicion en la encriptacion para tener bloques del tamaño de la clave

    try:
        while plaintext[-1] == 'X':
            plaintext = plaintext.rstrip(plaintext[-1])
    except IndexError:
        raise MensajeVacio

    return plaintext