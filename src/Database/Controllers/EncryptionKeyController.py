# Controla las operaciones de almacenamiento de las claves

import sys
sys.path.append("src")

from Database.Models.EncryptionKey import EncryptionKey

import psycopg2
import Database.SecretConfig as SecretConfig

class ErrorNotFound( Exception ):
    """ Excepcion que indica que una row buscada no fue encontrada"""
    pass

def GetCursor() :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = SecretConfig.PGDATABASE
    USER = SecretConfig.PGUSER
    PASSWORD = SecretConfig.PGPASSWORD
    HOST = SecretConfig.PGHOST
    PORT = SecretConfig.PGPORT

    connection = psycopg2.connect( database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT )
    return connection.cursor()

def CreateTable():
    """
    Crea la tabla de claves, en caso de que no exista
    """    
    sql = ""
    with open("sql/CreateEncryptionKey.sql","r") as f:
        sql = f.read()

    cursor = GetCursor()
    try:
        cursor.execute( sql )
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def DeleteTable():
    """
    Borra (DROP) la tabla en su totalidad
    """    
    sql = "drop table encryptionkey;"
    cursor = GetCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def DeleteRows():
    """
    Borra todas las filas de la tabla (DELETE)
    """
    sql = "delete from encryptionkey;"
    cursor = GetCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def InsertIntoTable( Key ):
    """ Guarda una clave en la base de datos """

    cursor = GetCursor()

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor.execute(f"""
        insert into encryptionkey (
            key_name, key_value, authentication_key
        )
        values 
        (
            '{Key.name}',  '{Key.value}', '{Key.authentication_key}'
        );
                       """)

        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes

        cursor.connection.commit()
    except:
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar la clave: " + Key.name )
    

def GetKeyByName( KeyName , AuthenticationKey ):    
    """ Busca la Key con el respectivo nombre y su contraseña, retornamos el objeto """

    cursor = GetCursor()
    cursor.execute(f"SELECT key_name, key_value, authentication_key from encryptionkey where key_name = '{KeyName}' ")
    row = cursor.fetchone()

    if row is None:
        raise ErrorNotFound("El registro buscado, no fue encontrado. Nombre: " + KeyName)
    
    GetedAuthenticationKey = row[2]

    if GetedAuthenticationKey == AuthenticationKey:
        result = EncryptionKey( row[0], row[1], row[2] )
        return result
    else:
        raise ErrorNotFound("Contraseña invalida. Clave de autenticación: " + AuthenticationKey)

def VerifyKeyExistance( KeyName ):
    """ Busca una clave por el nombre y validamos si existe """

    cursor = GetCursor()
    cursor.execute(f"SELECT key_name, key_value, authentication_key from encryptionkey where key_name = '{KeyName}' ")
    row = cursor.fetchone()

    if row is None:
        return False
    return True

def DeleteKey( KeyName ):
    """ Elimina la fila que contiene a una clave en la BD """

    cursor = GetCursor()

    try:
        #Verificamos si la clave existe
        keyExists = VerifyKeyExistance( KeyName )

        if not keyExists:
            raise

        # Si existe hacer la eliminacion en la tabla.
        sql = f"delete from encryptionkey where key_name = '{KeyName}'"
        cursor.execute( sql )
        cursor.connection.commit()

    except:
        cursor.connection.rollback()
        raise Exception("No fue posible eliminar la clave: " + KeyName )
    
def GetKeyId( KeyName ):
    """ Obtiene la Key Id del respectivo objeto en la base de datos"""

    cursor = GetCursor()
    cursor.execute(f"SELECT id from encryptionkey where key_name = '{KeyName}' ")
    row = cursor.fetchone()

    if row is None:
        raise ErrorNotFound("El Id de la clave no fue generada correctamente")
    
    return row[0]

def GetKeysNames( User ):
    """ Obtiene una lista con los nombres de los ids del usuario y los retorna como lista"""

    cursor = GetCursor()

    # Seperando el formato de la string 1,2,3,4 en una lista de formato ['1', '2', '3', '4']
    KeyString = User.encryption_keysIds
    KeysId = KeyString.split(",")

    # Guardando la lista de los nombres.
    KeyNames = []

    for KeyId in KeysId:
        cursor.execute(f"SELECT key_name FROM encryptionkey WHERE id = '{int(KeyId)}' ")
        row = cursor.fetchone()
        KeyNames.append(row[0])

    return KeyNames