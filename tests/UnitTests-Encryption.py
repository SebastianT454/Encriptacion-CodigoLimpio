#////////////////////////////// IMPORTS //////////////////////////////////////////////

import unittest
import sys
sys.path.append("src")

from Encryption.EncryptionLogic import *

#////////////////////////////// TESTS //////////////////////////////////////////////

class Test_CasosNormales(unittest.TestCase):
    """
    Se visualiza el comportamiento de la encriptacion, cuando
    Se intenta crifar un mensaje que no contiene muchos caracteres
    Especiales y es habitual que aparezcan estos mensajes.

    """

    def test_1(self):
        key = [[11, 42, 19], [21, 5, 15], [37, 8, 25]]
        plaintext = "THE BROWN CAT"
        ciphertext = "cZoB2,lwOofWEoo"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_2(self):
        key = [[23, 14], [7, 1]]
        plaintext = "NIGHT SKY"
        ciphertext = "J69is?SCDq"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_3(self):
        key = [[4, 18, 40], [12, 29, 33], [23, 40, 9]]
        plaintext = "Secret"
        ciphertext = "psoZ2p"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_4(self):
        key = [[15, 35, 2, 41], [32, 10, 27, 24], [40, 21, 8, 16], [18, 38, 0, 3]]
        plaintext = "Meet Me"
        ciphertext = "RFy3cS8?"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_5(self):
        key = [[3, 20, 24, 12, 8], [27, 8, 38, 12, 40], [33, 38, 35, 5, 34], [10, 38, 36, 41, 33], [34, 37, 40, 23, 4]]
        plaintext = "New House??"
        ciphertext = "?fZQO9RdR hYdb7"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_6(self):
        key = [[19, 25], [14, 8]]
        plaintext = "BonJour"
        ciphertext = "nleYYlCr"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

class Test_CasosExcepcionales(unittest.TestCase):
    """
    Se visualiza el comportamiento de la encriptacion, cuando
    Se intenta crifar un mensaje muy largo, pequeño, con muchos
    Caracteres especial y por consiguiente casos excepcionales.

    """

    def test_1(self):
        key = [[27, 28, 9],[28, 32, 34],[32, 33, 34]]
        plaintext = "1?, HO?,. ARE Y.OU?"
        ciphertext = "KfsvLdBQI1Xi,xmDsQ2xb"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_2(self):
        key = [[13, 17], [10, 16]]
        plaintext = "aaabbb"
        ciphertext = "YuaKnU"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_3(self):
        key = [[7, 3, 37], [14, 32, 36], [29, 37, 18]]
        plaintext = "AAABBB"
        ciphertext = "AAAgPR"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_4(self):
        key = [[7, 20, 25, 38],[27, 22, 36, 32],[37, 29, 19, 8],[20, 0, 4, 28]]
        plaintext = "La gravedad es un fenomeno natural por el cual los objetos y campos de materia dotados de masa."
        ciphertext = "yplVxciowwU6pJBVSH,eYmCGaH2FqgpI7pMC8NNaBW8?PvgY6UomJMkUKFByZ?d.y3QxBV4esHULQh11uuPRQD8NeWGis:TZ"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_5(self):
        key = [[5, 15, 18, 15, 10], [22, 10, 35, 10, 37], [28, 33, 31, 7, 30], [14, 35, 33, 38, 28], [30, 0, 37, 26, 6]]
        plaintext = "MANY WRITERS SEEM TO THINK THAT CAPITALIZATION COMMUNICATES AUTHORITY AND IMPORTANCE."
        ciphertext = "i14Q44zDrAeEK.DF:X38qAygDZP1VfK.TIx893M:qEXyD0At,3xBaipWgAolQfcb58ZR2Art,Utd9Lo1h5rGs"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)

    def test_6(self):
        key = [[13, 17], [10, 16]]
        plaintext = "123456789"
        ciphertext = "XhQ7JSCDbh"
        ciphertext_new = hill_cipher(plaintext, key)
        self.assertEqual(ciphertext_new, ciphertext)
        plaintext_new = hill_decipher(ciphertext, key)
        self.assertEqual(plaintext_new, plaintext)


class Test_CasosError(unittest.TestCase):
    """
    Se visualiza todos los posibles casos de error (para el programa),
    Cuando algunos de los inputs no son validos para el algoritmo
    (Encriptacion por Hills) o afectan el rendimiento del programa.

    """

    # Casos Error 1: Solamente hay una fila por lo tanto, la clave no es cuadrada (nxn).
    def test_1(self):
        key = [[23, 14]]
        plaintext = "Hello.."
        self.assertRaises( MultiplicacionInvalidaDeMatriz,  hill_cipher, plaintext, key)

    # Casos Error 2: La clave (matriz) no es invertible.
    def test_2(self):
        key = [[23, 14],[23, 14]]
        plaintext = "Hello.."
        self.assertRaises( MatrizNoEsInvertible,  hill_decipher, plaintext, key)

    # Casos Error 3: El mensaje esta vacio.
    def test_3(self):
        key = [[23, 14], [8, 41]]
        plaintext = ""
        self.assertRaises( MensajeVacio,  hill_decipher, plaintext, key)
    
    # Casos Error 4: El mensaje tiene caracteres invalidos en el alfabeto.
    def test_4(self):
        key = [[23, 14], [8, 41]]
        plaintext = "-"
        self.assertRaises( CaracteresInvalidosMensaje,  hill_cipher, plaintext, key)

    # Casos Error 5: El mensaje es diferente a una string.
    def test_5(self):
        key = [[23, 14], [8, 41]]
        plaintext = 1
        self.assertRaises( MensajeNoEsString,  hill_cipher, plaintext, key)

    # Casos Error 6: La Key contiene strings o otro tipo de dato.
    def test_6(self):
        key = [[23, "14"], [11, 41]]
        plaintext = "Ouch..."
        self.assertRaises( MultiplicacionInvalidaDeMatriz,  hill_cipher, plaintext, key)

    # Casos Error 7: Se ingresa un valor de tamaño para la matriz clave incorrecto.
    def test_7(self):
        Size = "3"
        self.assertRaises( SizeInvalida,  hill_genkey, Size)

    # Casos Error 8: Se verifica cuando se ingresa un valor muy grande para la matriz.
    def test_8(self):
        Size = 101
        self.assertRaises( ClaveDemasiadoGrande,  hill_genkey, Size)


if __name__ == '__main__':

    # crear una suite con todas las pruebas
    test_classes_to_run = [Test_CasosNormales, Test_CasosExcepcionales, Test_CasosError]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    all_tests_suite = unittest.TestSuite(suites_list)

    # ejecutar el conjunto de pruebas con gran velocidad
    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(all_tests_suite)


