# Encriptación por metodo de Hills

## ¿Quién hizo esto?

Sebastián Tamayo Avendaño - Estudiante Ing Sistemas.

## ¿Qué es y para qué es?

Este es un método de encriptación a través de matrices que esta relacionado con él código cesar, este tiene alfabeto donde cada palabra tiene un número o peso asociado Este se utilizará a través de operaciones entre matrices para obtener la encriptación De un mensaje limitado por la cantidad de letras en el alfabeto.

## ¿Cómo lo hago funcionar?

- Prerrequisitos: 
    - Descargar libreria numpy
    - Descargar libreria sympy
    - Descargar libreria src
    - Descargar libreria kivy


## ¿Cómo está hecho?

El cifrado Hill es un criptosistema que se basa en emplear una matriz como clave para cifrar un texto en claro y 
Su inversa para descifrar el criptograma correspondiente.

Se ha usado un alfabeto de 67 caracteres que incluyen letras  dígitos numéricos, del 0 al 9, 
así como los 4 caracteres siguientes: ".", ",", ":", "?" y el espacio en blanco, en ese orden.

Cada letra está representada por un número (diccionario).

## Estructura

- Carpeta src: Codigo fuente de la logica de la aplicación. Tiene subcarpetas por cada capa de la aplicacion
- Carpeta tests: Pruebas Unitarias (UnitTests-Encryption.py)

Recuerde que cada carpeta de código fuente debe contener un archivo __init.py que permite que python
reconozca la carpeta como un Módulo y pueda hacer import

- Modulos: Existen los siguientes modulos en el conjunto de subcarpetas **src**, que estan diseñados para la logica y la interfaz del Usuario
  1. Encryption --> EncryptionLogic.py ( Logica y metodos para encriptar el mensaje )

  2. Gui -->  Console -->  EncryptionGUI_Console.py ( Gui en Consola )
  3. Gui -->  Kivy -->  EncryptionGUI_Kivy.py ( Gui Principal )
  4. Gui -->  Kivy -->  LoginGUI_Kivy.py ( Gui de la pestaña Login )
  5. Gui -->  Kivy -->  MenuGUI_Kivy.py ( Gui de la pestaña Menu )
  6. Gui -->  GuiLogic -->  Kivy --> EncryptionGUI_KivyLogic.py ( Logica del Gui Principal )

  7. Database -->  Controllers -->  UserController.py ( Controlador para el usuario )
  8. Database -->  Controllers -->  EncryptionKeyController.py ( Controlador para la clave asociada a un usuario )

  9. Database -->  Models -->  User.py ( Clase de tipo usuario )
  10. Database -->  Models -->  EncryptionKey.py ( Clase de tipo clave )

## Uso

Para ejecutar las pruebas unitarias de la encriptacion, desde la carpeta src, use el comando

`
  python tests\UnitTests-Encryption.py
`

Para ejecutar las pruebas unitarias de la base de datos para el usuario, use el comando

`
  python src\Database\tests\ControllerUserTest.py
`

Para ejecutar las pruebas unitarias de la base de datos para las claves del usuario, use el comando

`
  python src\Database\tests\ControllerEncryptionKey.py
`

Para poder ejecutarlas desde la carpeta raiz, debe indicar la ruta de busqueda donde se encuentran los
módulos, incluyendo las siguientes lineas al inicio del módulo de pruebas

- Este programa cuenta con dos interfaces de usuario, una que es por consola y otra que esta hecha con la libreria kivy.

Para ejecutar la interfaz por consola, se debe utilizar el siguiente comando:

`
  python src\Console\EncryptionUi_Console.py
`

El orden de ejecucion del programa en consola consiste en:

1. Se ingresa un mensaje
2. Seleccionar el tamaño de la clave, que sera una matrix, nxn elementos adentro **Solo se permiten numeros**
3. Seleccionar si esta clave quiere ser creada de forma automatica (valores aleatorios) o de forma manual con datos especificos.
4. Seleccionar si se quiere encriptar o desincriptar, si no se ha encriptado anteriormente, saldra un error si se selecciona desencriptar.
   Una vez que se encripte, se puede continuar el programa para utilizar la funcionalidad de desencriptacion, si selecciona "n", el programa
   Volvera ejecutarse desde el inicio.

Para ejecutar la interfaz por Kivy, se debe utilizar el siguiente comando:

`
  python src\Gui\Kivy\EncryptionGUI_Kivy.py
`

El orden de ejecucion del programa en Kivy consiste en:

1. Se ingresa un mensaje y se verifica si es valido para la encriptacion si se presiona Enter.
2. Seleccionar el tamaño de la clave en el menu y ingresar los datos de la matriz:
	- Escribir la clave en el formato "1,2,3,7,8,9" donde tiene que haber una cantidad de elementos igual a
	  Tamaño de la matriz ^ 2
	- Si no se escribe correctamente, se dispara una excepcion dependiendo del error.
3. Seleccionar si se quiere encriptar o desincriptar, si no se ha encriptado anteriormente, saldra una excepcion si se selecciona desencriptar.

- En caso que no funcione alguno de los modulos, ingrese el siguiente comando: 

`
  import sys
  sys.path.append("src")
`
