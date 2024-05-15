import unittest

import sys
sys.path.append("src")

from Database.Models.EncryptionKey import EncryptionKey
import Database.Controllers.EncryptionKeyController as EncryptionKeyController

class ControllerTest(unittest.TestCase):
    """
        Pruebas a la Clase Controlador de la aplicación
    """

    # TEST FIXTURES
    # Codigo que se ejecuta antes de cada prueba

    def setUp(self):
        """ Se ejecuta siempre antes de cada metodo de prueba """
        print("Invocando setUp")
        EncryptionKeyController.DeleteRows() # Asegura que antes de cada metodo de prueba, se borren todos los datos de la tabla

    def setUpClass():
        """ Se ejecuta al inicio de todas las pruebas """
        print("Invocando setUpClass")
        EncryptionKeyController.CreateTable()  # Asegura que al inicio de las pruebas, la tabla este creada

    def tearDown(self):
        """ Se ejecuta al final de cada test """
        print("-- Test Finalizado --")

    def tearDownClass():
        """ Se ejecuta al final de todos los tests """
        print("-- Tests Finalizados --")
        EncryptionKeyController.DeleteRows()

    def testInsert(self):
        """ Verifica que funcione bien la creacion y la busqueda de una clave """
        # Pedimos crear una clave
        print("Ejecutando testInsert")
        test_key = EncryptionKey("Contrasena 1", "1,2,3,4", "Sol321") 

        EncryptionKeyController.InsertIntoTable( test_key )

        # Buscamos la clave
        key_found = EncryptionKeyController.GetKeyByName( test_key.name , test_key.authentication_key)

        # Verificamos que los datos de la clave sean correcto
        self.assertEqual( test_key.name, key_found.name )
        self.assertEqual( test_key.value, key_found.value )
        self.assertEqual( test_key.authentication_key, key_found.authentication_key )

    def testDelete(self):
        """ Verifica que funcione bien la eliminacion de claves """

        print("Ejecutando testDelete")

        # Ingresamos la clave
        key_to_delete = EncryptionKey("Contrasena 1", "1,2,3,4", "Sol321")
        EncryptionKeyController.InsertIntoTable( key_to_delete )

        # Eliminamos la clave
        EncryptionKeyController.DeleteKey( key_to_delete.name )

        # Buscamos la clave y debe de retornar False.

        KeyExists = EncryptionKeyController.VerifyKeyExistance( key_to_delete.name )

        self.assertEqual(KeyExists, False)


# Este fragmento de codigo permite ejecutar las pruebas individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    unittest.main()