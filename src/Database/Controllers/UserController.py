# Controla las operaciones de almacenamiento de la clase Usuario

import sys
sys.path.append("src")

from Database.Models.User import User

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
    Crea la tabla de usuarios, en caso de que no exista
    """    
    sql = ""
    with open("sql/CreateUser.sql","r") as f:
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
    sql = "drop table users;"
    cursor = GetCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def DeleteRows():
    """
    Borra todas las filas de la tabla (DELETE)
    """
    sql = "delete from users;"
    cursor = GetCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def InsertIntoTable( User ):
    """ Guarda un Usuario en la base de datos """

    cursor = GetCursor()

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor.execute(f"""
        insert into users (
            _name, _password, encryption_keys_ids
        )
        values 
        (
            '{User.name}',  '{User.password}', '{User.encryption_keysIds}'
        );
                       """)

        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes

        cursor.connection.commit()
    except:
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el usuario: " + User.name )
    

def GetUserByUsername( Username ):    
    """ Busca un usuario por el nombre y lo retornamos como objeto """

    cursor = GetCursor()
    cursor.execute(f"SELECT _name, _password, encryption_keys_ids from users where _name = '{Username}' ")
    row = cursor.fetchone()

    if row is None:
        raise ErrorNotFound("El registro buscado, no fue encontrado. Nombre: " + Username)

    result = User( row[0], row[1], row[2] )
    return result

def VerifyUserExistance( Username ):
    """ Busca un usuario por el nombre y validamos si existe """

    cursor = GetCursor()
    cursor.execute(f"SELECT _name, _password, encryption_keys_ids from users where _name = '{Username}' ")
    row = cursor.fetchone()

    if row is None:
        return False
    return True

def DeleteUser( Username ):
    """ Elimina la fila que contiene a un usuario en la BD """

    cursor = GetCursor()

    try:
        #Verificamos si el usuario existe
        GetUserByUsername(Username)

        # Si existe hacer la eliminacion en la tabla.
        sql = f"delete from users where _name = '{Username}'"
        cursor.execute( sql )
        cursor.connection.commit()

    except:
        cursor.connection.rollback()
        raise Exception("No fue posible eliminar el usuario: " + Username )
    
def UpdateUserEncryptionKeys( Username , EncryptionKeys):
    """ Actualiza las encryptions keys de un usuario """
    
    cursor = GetCursor()

    try:
        #Verificamos si el usuario existe
        GetUserByUsername(Username)
        
        cursor.execute(f"""
            update users
            set 
                encryption_keys_ids ='{EncryptionKeys}'
            where _name ='{Username}'
        """)

        cursor.connection.commit()

    except:
        cursor.connection.rollback()
        raise Exception("No fue posible actualizar el usuario: " + Username )