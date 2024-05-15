#////////////////////////////// IMPORTS //////////////////////////////////////////////
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

import sys
sys.path.append("src")

# Logica de Encriptacion.
from Encryption.EncryptionLogic import *

# Modulos de base de datos para el Usuario.
from Database.Models.User import User
import Database.Controllers.UserController as UserController

# Modulos de base de datos para la Clave.
from Database.Models.EncryptionKey import EncryptionKey
import Database.Controllers.EncryptionKeyController as EncryptionKeyController

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

# Funcion para mostrar el error en Kivy.
def ShowError( err ):
    GridLayout_ErrorContent = GridLayout(cols = 1)
    GridLayout_ErrorContent.add_widget( Label(text= str(err) ) )
    Btn_Close = Button(text="Cerrar" )
    GridLayout_ErrorContent.add_widget( Btn_Close )
    Popup_widget = Popup(title="Error", content = GridLayout_ErrorContent)
    Btn_Close.bind( on_press= Popup_widget.dismiss)
    Popup_widget.open()
    return False

# Funcion para generar de forma aleatoria una contraseña (matrix) de orden n.
def GenerateAutomaticKeyLogic(KeySize):
    Key = hill_genkey(KeySize)
    #Transformando np.matrix a una lista.
    Key = np.matrix.tolist(Key)

    KeyToString = str(Key)
    # Eliminar los corchetes
    StringKey = KeyToString.replace('[', '').replace(']', '')
    return StringKey
        
# Funcion que transforma una string en formato 1,2,3,4 a una matrix [1,2,3,4]
def GenerateKeyLogic(KeySize, Key):
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

# Funcion para verificar si el mensaje cumple todo lo necesario para ser encriptado.
def ValidateMessageLogic(Message):
    try:
        Diccionario_encrypt_ref = Dictionary_encrypt  # Diccionario de encriptación

        # Recorrer cada Character del mensaje y verificar si se encuentra en el diccionario.
        for Character in Message:
            if Character not in Diccionario_encrypt_ref.keys():
                raise Exception(f"Caracter no válido: {Character}")
            
        # Verificar si el mensaje esta vacio.
        if len(Message) == 0:
            raise Exception(f"El mensaje no tiene nada, esta vacio." )
        
        # Verificar que el mensaje tenga minimo 1 Element.
        if len(Message) == 1:
            raise Exception(f"El mensaje apenas tiene 1 elemento, tiene que ser más que una letra o numero." )
        
        return True
    
    except Exception as err:
        return ShowError(err)

# Funcion que valida que si la clave esta en el formato que debe, es decir 1,2,3,4
def ValidateKeyLogic(KeySize, Key):
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

        return True
    
    except Exception as err:
        return ShowError(err)
    
# Funcion pora crear una clave y ingresarla al respectivo usuario.
def AddKeyToUser( User, Key ):
    try:
        KeyExists = EncryptionKeyController.VerifyKeyExistance( Key.name )

        if KeyExists:
            raise Exception(f"La clave ya existe en este usuario." )
            
        # Ingresar la clave en la base de datos.
        EncryptionKeyController.InsertIntoTable(Key)

        # Obtener el id de la clave.
        KeyId = EncryptionKeyController.GetKeyId( Key.name )
        #print(KeyId)

        # Obtener la lista de claves actuales del usuario y modificarla.
        ActualEncryptionKeys = User.encryption_keysIds

        if len(ActualEncryptionKeys) == 0:
            ActualEncryptionKeys = ActualEncryptionKeys + f"{KeyId}"
        else:
            ActualEncryptionKeys = ActualEncryptionKeys + f",{KeyId}"

        User.encryption_keysIds = ActualEncryptionKeys
        #print(User.encryption_keysIds, ActualEncryptionKeys)

        # Actualizar las Keys del usuario en la base de datos.
        UserController.UpdateUserEncryptionKeys( User.name, User.encryption_keysIds)

    except Exception as err:
        return ShowError(err)
    
# Funcion para obtener cuantas claves tiene un usuario agregadas.
def GetAmountOfKeys( User ):
    KeyString = User.encryption_keysIds

    TotalOfIds = KeyString.split(",")
    return len(TotalOfIds)

# Funcion para obtener la lista de claves agregadas al usuario.
def GetUserKeysId( User ):
    KeyString = User.encryption_keysIds

    KeysId = KeyString.split(",")
    return KeysId

# Funcion para determinar de forma automatica el size de una de las claves guardadas.
def SetSizeVerifiedKey(KeyValue):
    KeySizes = [2,3,4,5]

    for KeySize in KeySizes:
        if (len(KeyValue) % KeySize) == 0:
            return str(KeySize)