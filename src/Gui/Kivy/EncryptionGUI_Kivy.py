#////////////////////////////// IMPORTS //////////////////////////////////////////////
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.spinner import Spinner

import sys
sys.path.append("src")

# Logica de Encriptacion.
from Encryption.EncryptionLogic import *

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

class EncryptionApp(App):
    def build(self):
        # GridLayout = Matrix de filas de columnas con widgets (botones, labels, etc.)
        # Cols o Rows, el orden de la matrix en el GridLayout
        # Padding = El espacio entre el Contenido_Error del widget y su borde (entre más grande, más pequeño sera el borde del widget)
        # Spacing = El tamaño entre cada widget (entre más grande, más separado estara cada widget)

        ContenedorPrincipal = GridLayout(cols = 1,padding=20,spacing=10)

        # Label y text input con el mensaje.
        ContenedorPrincipal.add_widget( Label(text="Mensaje", font_size = 20) )
        self.Input_Mensaje = TextInput(font_size = 24, multiline = False)
        ContenedorPrincipal.add_widget(self.Input_Mensaje)

        # Conectar con el callback con el evento on_text_validate para determinar si el mensaje es valido.
        self.Input_Mensaje.bind( on_text_validate = self.Validar_Mensaje)

        #---------------------------------- Boton - Label Generar Clave -------------------------------------------

        Btn_clave = Button(text="Generar Clave",font_size = 40)
        ContenedorPrincipal.add_widget(Btn_clave)

        # Conectar con el callback con el evento press del boton de generar clave.
        Btn_clave.bind( on_press= self.GenerarClaveAutomatica )

        """
        ContenedorPrincipal.add_widget( Label(text="Clave generada", font_size = 20) )
        self.Input_Clave = TextInput(font_size=17)
        ContenedorPrincipal.add_widget(self.Input_Clave)
        """

        # Crear el grid para la clave
        ContenedorClave = GridLayout(cols=2)

        # Para la clave: size_hint = (0.7, 1)  Ancho = 70%, Altura = 100%
        # Para el tamaño: size_hint = (0.3, 1)  Ancho = 30%, Altura = 100%

        # Crear y agregar los labels para la clave
        ContenedorClave.add_widget( Label(text="Clave", font_size = 20, size_hint = (0.7, 1) ))

        ContenedorClave.add_widget( Label(text="Tamano Clave", font_size = 20, size_hint = (0.3, 1) ) )

        # Crea y agrega el TextInput
        self.Input_Clave = TextInput(multiline = False, size_hint = (0.7, 1), font_size = 12, text = "La clave esta en el formato 1,2,3,4")
        ContenedorClave.add_widget(self.Input_Clave)

        # Crea y configura el Spinner
        self.ListaTamanoClave = Spinner(text="2", values=("2", "3", "4", "5"), size_hint = (0.3, 1))
        ContenedorClave.add_widget(self.ListaTamanoClave)

        ContenedorPrincipal.add_widget(ContenedorClave)
        #---------------------------------- Boton - Label Encriptar --------------------------------------------

        Btn_encriptar = Button(text="Encriptar",font_size=40)
        ContenedorPrincipal.add_widget(Btn_encriptar)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_encriptar.bind( on_press= self.EncriptarMensaje )

        ContenedorPrincipal.add_widget( Label(text="Mensaje Encriptado", font_size = 20) )
        self.Input_MensajeEncriptado = TextInput(font_size=24)
        ContenedorPrincipal.add_widget(self.Input_MensajeEncriptado)

        #---------------------------------- Boton - Label Desencriptar ------------------------------------------

        Btn_desencriptar = Button(text="Desencriptar",font_size=40)
        ContenedorPrincipal.add_widget(Btn_desencriptar)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_desencriptar.bind( on_press= self.DesencriptarMensaje )

        ContenedorPrincipal.add_widget( Label(text="Mensaje Desencriptado", font_size = 20) )
        self.Input_MensajeDesencriptado = TextInput(font_size=24)
        ContenedorPrincipal.add_widget(self.Input_MensajeDesencriptado)

        # Size Hint (widht, height) = representa el espacio que se quiere utilizar en su totalidad 1 = 100% de la Window screen.
        # Size = tamaño que va tomar, en este caso el tamaño de la Window screen de ancho y alto.
        Scroll_ContenedorPrincipal = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        Scroll_ContenedorPrincipal.add_widget(ContenedorPrincipal)

        # Se retorna el widget o "raiz" que contiene a todos los demás
        return Scroll_ContenedorPrincipal

    # instance es el widget que generó el evento
    # Value es el valor actual que tiene el widget

    def GenerarClaveAutomatica(self, value):
        Tamano_Clave = int(self.ListaTamanoClave.text)
        Clave = hill_genkey(Tamano_Clave)
        #Transformando np.matrix a una lista.
        Clave = np.matrix.tolist(Clave)

        Cadena = str(Clave)
        # Eliminar los corchetes
        ClaveString = Cadena.replace('[', '').replace(']', '')
        self.Input_Clave.text = ClaveString

    def EncriptarMensaje(self, value):

        # Verificar si la clave y el mensaje son validos.
        MensajeValido = self.Validar_Mensaje(value)
        ClaveValida = self.Validar_Clave(value)

        if MensajeValido and ClaveValida:
            try:
                # Realizar la encriptacion.
                Clave = self.Generar_Clave(value)
                Mensaje = self.Input_Mensaje.text

                MensajeEncriptado = hill_cipher(Mensaje, Clave)
                self.Input_MensajeEncriptado.text = MensajeEncriptado

            except Exception as err:
                return self.Mostrar_error( err )

    def DesencriptarMensaje(self, value):
        try:
            MensajeEncriptado = self.Input_MensajeEncriptado.text
            Clave = self.Generar_Clave(value)
            MensajeDesencriptado = ""

            # Verificar si hay algo en como mensaje encriptado de lo contrario, se toma
            # El mensaje como la clave.
            if MensajeEncriptado != "":
                # Realizar la desencriptacion.
                MensajeDesencriptado = hill_decipher(MensajeEncriptado, Clave)
            else:
                MensajeValido = self.Validar_Mensaje(value)

                if MensajeValido:
                    Mensaje = self.Input_Mensaje.text
                    MensajeDesencriptado = hill_decipher(Mensaje, Clave)

            self.Input_MensajeDesencriptado.text = MensajeDesencriptado

        except Exception as err:
            return self.Mostrar_error( err )
        
    def Mostrar_error( self, err ):
        Contenido_Error = GridLayout(cols = 1)
        Contenido_Error.add_widget( Label(text= str(err) ) )
        Btn_cerrar = Button(text="Cerrar" )
        Contenido_Error.add_widget( Btn_cerrar )
        Popup_widget = Popup(title="Error", content = Contenido_Error)
        Btn_cerrar.bind( on_press= Popup_widget.dismiss)
        Popup_widget.open()
        return False

    def Validar_Mensaje(self, value):
        """
        Verificar si el mensaje tiene caracteres validos para la encriptacion,
        es decir si sus caracteres estan en el diccionario de letras en Encryption Logic

        """
        try:
            Mensaje = self.Input_Mensaje.text  # El texto del TextInput
            Diccionario_encrypt_ref = Diccionario_encrypt  # Diccionario de encriptación

            # Recorrer cada caracter del mensaje y verificar si se encuentra en el diccionario.
            for caracter in Mensaje:
                if caracter not in Diccionario_encrypt_ref.keys():
                    raise Exception(f"Caracter no válido: {caracter}")
                
            # Verificar si el mensaje esta vacio.
            if len(Mensaje) == 0:
                raise Exception(f"El mensaje no tiene nada, esta vacio." )
            
            # Verificar que el mensaje tenga minimo 1 elemento.
            if len(Mensaje) == 1:
                raise Exception(f"El mensaje apenas tiene 1 elemento, tiene que ser más que una letra o numero." )
            
            return True
        
        except Exception as err:
            return self.Mostrar_error(err)

    def Validar_Clave(self, value):
        """
        Funcion que verifica si la clave es valida para generarse.
        """
        TamanoClave = self.ListaTamanoClave.text
        Clave = self.Input_Clave.text

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

            return True
        
        except Exception as err:
            return self.Mostrar_error(err)

    def Generar_Clave(self, value):
        TamanoClave = int(self.ListaTamanoClave.text)
        Clave = self.Input_Clave.text

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


if __name__ == "__main__":
    EncryptionApp().run()