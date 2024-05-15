import unittest

import sys
sys.path.append("src")

from Database.Models.User import User
import Database.Controllers.UserController as UserController

class ControllerTest(unittest.TestCase):
    """
        Pruebas a la Clase Controlador de la aplicación
    """

    # TEST FIXTURES
    # Codigo que se ejecuta antes de cada prueba

    def setUp(self):
        """ Se ejecuta siempre antes de cada metodo de prueba """
        print("Invocando setUp")
        UserController.DeleteRows() # Asegura que antes de cada metodo de prueba, se borren todos los datos de la tabla

    def setUpClass():
        """ Se ejecuta al inicio de todas las pruebas """
        print("Invocando setUpClass")
        UserController.CreateTable()  # Asegura que al inicio de las pruebas, la tabla este creada

    def tearDown(self):
        """ Se ejecuta al final de cada test """
        print("-- Test Finalizado --")

    def tearDownClass():
        """ Se ejecuta al final de todos los tests """
        print("-- Tests Finalizados --")
        UserController.DeleteRows()

    def testInsert(self):
        """ Verifica que funcione bien la creacion y la busqueda de un usuario """
        # Pedimos crear un usuario
        print("Ejecutando testInsert")
        test_user = User("Juan", "asdasd123", "9,10,14,7") 

        UserController.InsertIntoTable( test_user )

        # Buscamos el usuario
        user_found = UserController.GetUserByUsername( test_user.name )

        # Verificamos que los datos del usuario sean correcto
        self.assertEqual( test_user.name, user_found.name )
        self.assertEqual( test_user.password, user_found.password )
        self.assertEqual( test_user.encryption_keysIds, user_found.encryption_keysIds )

    def testDelete(self):
        """ Verifica que funcione bien la eliminacion de usuarios """

        print("Ejecutando testDelete")

        # Ingresamos el usuario
        user_to_delete = User("Juan", "asdasd123", "9,10,14,7")
        UserController.InsertIntoTable( user_to_delete )

        # Eliminamos el usuario
        UserController.DeleteUser( user_to_delete.name )

        # Buscamos el usuario para verificar que ya no existe (debe lanzar una excepcion)
        self.assertRaises(UserController.ErrorNotFound, UserController.GetUserByUsername, user_to_delete.name)

    def testUpdateUserEncryptionKeys(self):
        """ Verifica que se actualice los Ids de las claves para la encriptacion """

        print("Ejecutando testUpdateUserEncryptionKeys")

        # Ingresamos el usuario
        test_user = User("Juan", "asdasd123", "9,10,14,7") 
        UserController.InsertIntoTable( test_user )

        NewEncryptionKeyList = "1,2,4,10"

        # Actualizamos el usuario
        UserController.UpdateUserEncryptionKeys( test_user.name, NewEncryptionKeyList )

        # Buscamos el usuario
        user_found = UserController.GetUserByUsername( test_user.name )

        self.assertEqual( NewEncryptionKeyList, user_found.encryption_keysIds )

# Este fragmento de codigo permite ejecutar las pruebas individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    unittest.main()