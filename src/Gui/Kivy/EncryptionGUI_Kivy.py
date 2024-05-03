#////////////////////////////// IMPORTS //////////////////////////////////////////////
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

import sys
sys.path.append("src")

# Logica de Encriptacion.
from Encryption.EncryptionLogic import *

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

# Declare both screens
class EncryptionMenu(Screen):
    def __init__(self, **kwargs):
        super(EncryptionMenu, self).__init__(**kwargs)
        
        # GridLayout = Matrix de filas de columnas con widgets (botones, labels, etc.)
        # Cols o Rows, el orden de la matrix en el GridLayout
        # Padding = El espacio entre el GridLayout_ErrorContent del widget y su borde (entre más grande, más pequeño sera el borde del widget)
        # Spacing = El tamaño entre cada widget (entre más grande, más separado estara cada widget)

        MainContainer = GridLayout(cols = 1 , padding = 20 , spacing = 10)

        # Label y text input con el mensaje.
        MainContainer.add_widget( Label(text="Message", font_size = 20) )
        self.Input_message = TextInput(font_size = 24, multiline = False)
        MainContainer.add_widget(self.Input_message)

        # Conectar con el callback con el evento on_text_validate para determinar si el mensaje es valido.
        self.Input_message.bind( on_text_validate = self.ValidateMessage)

        #---------------------------------- Boton - Label Generar Key -------------------------------------------

        Btn_Key = Button(text="Generar Clave",font_size = 30)
        MainContainer.add_widget(Btn_Key)

        # Conectar con el callback con el evento press del boton de generar clave.
        Btn_Key.bind( on_press= self.GenerateAutomaticKey )

        """
        MainContainer.add_widget( Label(text="Key generada", font_size = 20) )
        self.Input_Key = TextInput(font_size=17)
        MainContainer.add_widget(self.Input_Key)
        """

        # Crear el grid para el label
        GridLayout_KeyLabels = GridLayout( cols = 2 )

        # Para la clave: size_hint = (0.7, 1)  Ancho = 70%, Altura = 100%
        # Para el tamaño: size_hint = (0.3, 1)  Ancho = 30%, Altura = 100%

        # Crear y agregar los labels para la clave
        GridLayout_KeyLabels.add_widget( Label(text="Key", font_size = 20, size_hint = (0.7, 1) ))

        GridLayout_KeyLabels.add_widget( Label(text="Tamano Key", font_size = 20, size_hint = (0.3, 1) ) )

        MainContainer.add_widget(GridLayout_KeyLabels)

        # Crear el grid para los inputs de la clave
        GridLayout_KeyInputs = GridLayout( cols = 2 )

        # Crea y agrega el TextInput
        self.Input_Key = TextInput(multiline = False, size_hint = (0.7, 1), font_size = 18, text = "La clave esta en el formato 1,2,3,4")
        GridLayout_KeyInputs.add_widget(self.Input_Key)

        # Crea y configura el Spinner
        self.Spinner_KeySize = Spinner(text="2", values=("2", "3", "4", "5"), size_hint = (0.3, 1))
        GridLayout_KeyInputs.add_widget(self.Spinner_KeySize)

        MainContainer.add_widget(GridLayout_KeyInputs)

        # Crear el grid para los botones de la contraseña
        GridLayout_KeyButtons = GridLayout( cols = 2 )

        # Boton para guardar contraseñas
        Btn_SavePassword = Button(text="Guardar Contraseña", font_size = 30)
        GridLayout_KeyButtons.add_widget(Btn_SavePassword)

        # Boton para escribir la contraseña asociada en la base de datos
        Btn_AuthenticationPassword = Button(text="Clave de seguridad", font_size = 30)
        GridLayout_KeyButtons.add_widget(Btn_AuthenticationPassword)

        MainContainer.add_widget(GridLayout_KeyButtons)

        #---------------------------------- Boton - Label Encriptar --------------------------------------------

        Btn_Encrypt = Button(text="Encriptar",font_size = 30)
        MainContainer.add_widget(Btn_Encrypt)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_Encrypt.bind( on_press= self.EncryptMessage )

        MainContainer.add_widget( Label(text="Mensaje Encriptado", font_size = 20) )
        self.Input_EncryptedMessage = TextInput(font_size=24)
        MainContainer.add_widget(self.Input_EncryptedMessage)

        #---------------------------------- Boton - Label Desencriptar ------------------------------------------

        Btn_Decrypt = Button(text="Desencriptar",font_size = 30)
        MainContainer.add_widget(Btn_Decrypt)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_Decrypt.bind( on_press= self.DecryptMessage )

        MainContainer.add_widget( Label(text="Mensaje Desencriptado", font_size = 20) )
        self.Input_DecryptedMessage = TextInput(font_size=24)
        MainContainer.add_widget(self.Input_DecryptedMessage)

        #---------------------------------- Boton (Volver al menu) ------------------------------------------

        Btn_Return_To_Menu = Button(text="Volver al menu", font_size = 30)
        MainContainer.add_widget(Btn_Return_To_Menu)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_Return_To_Menu.bind( on_press= self.Switch_To_Menu )

        # Size Hint (widht, height) = representa el espacio que se quiere utilizar en su totalidad 1 = 100% de la Window screen.
        # Size = tamaño que va tomar, en este caso el tamaño de la Window screen de ancho y alto.

        Scroll_MainContainer = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        Scroll_MainContainer.add_widget(MainContainer)

        self.add_widget(Scroll_MainContainer)

    def Switch_To_Menu(self, value):
        self.manager.current = 'menu_screen'

    def GenerateAutomaticKey(self, value):
        KeySize = int(self.Spinner_KeySize.text)
        Key = hill_genkey(KeySize)
        #Transformando np.matrix a una lista.
        Key = np.matrix.tolist(Key)

        KeyToString = str(Key)
        # Eliminar los corchetes
        StringKey = KeyToString.replace('[', '').replace(']', '')
        self.Input_Key.text = StringKey

    def EncryptMessage(self, value):

        # Verificar si la clave y el mensaje son validos.
        ValidMessage = self.ValidateMessage(value)
        ValidKey = self.ValidateKey(value)

        if ValidMessage and ValidKey:
            try:
                # Realizar la encriptacion.
                Key = self.GenerateKey(value)
                Message = self.Input_message.text

                EncryptedMessage = hill_cipher(Message, Key)
                self.Input_EncryptedMessage.text = EncryptedMessage

            except Exception as err:
                return self.ShowError( err )

    def DecryptMessage(self, value):
        try:
            EncryptedMessage = self.Input_EncryptedMessage.text
            Key = self.GenerateKey(value)
            DecryptedMessage = ""

            # Verificar si hay algo en como mensaje encriptado de lo contrario, se toma
            # El mensaje como la clave.
            if EncryptedMessage != "":
                # Realizar la desencriptacion.
                DecryptedMessage = hill_decipher(EncryptedMessage, Key)
            else:
                ValidMessage = self.ValidateMessage(value)

                if ValidMessage:
                    Message = self.Input_message.text
                    DecryptedMessage = hill_decipher(Message, Key)

            self.Input_DecryptedMessage.text = DecryptedMessage

        except Exception as err:
            return self.ShowError( err )
        
    def ShowError( self, err ):
        GridLayout_ErrorContent = GridLayout(cols = 1)
        GridLayout_ErrorContent.add_widget( Label(text= str(err) ) )
        Btn_Close = Button(text="Cerrar" )
        GridLayout_ErrorContent.add_widget( Btn_Close )
        Popup_widget = Popup(title="Error", content = GridLayout_ErrorContent)
        Btn_Close.bind( on_press= Popup_widget.dismiss)
        Popup_widget.open()
        return False

    def ValidateMessage(self, value):
        """
        Verificar si el mensaje tiene caracteres validos para la encriptacion,
        es decir si sus caracteres estan en el diccionario de letras en Encryption Logic

        """
        try:
            Message = self.Input_message.text  # El texto del TextInput
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
                raise Exception(f"El mensaje apenas tiene 1 Element, tiene que ser más que una letra o numero." )
            
            return True
        
        except Exception as err:
            return self.ShowError(err)

    def ValidateKey(self, value):
        """
        Funcion que verifica si la clave es valida para generarse.
        """
        KeySize = self.Spinner_KeySize.text
        Key = self.Input_Key.text

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
            return self.ShowError(err)

    def GenerateKey(self, value):
        KeySize = int(self.Spinner_KeySize.text)
        Key = self.Input_Key.text

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
    
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        LoginLayout = BoxLayout(orientation='vertical')

        LoginLayout.size_hint = (0.6, 0.5)  # Width: 60%, Height: 50%
        LoginLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 

        # El label y el input del usuario.
        Label_Username = Label(text='Usuario:', size_hint_y=0.1, font_size = 25)
        LoginLayout.add_widget(Label_Username)
        self.Input_Username = TextInput(size_hint_y = 0.1, font_size = 24, multiline=False)
        LoginLayout.add_widget(self.Input_Username)

        # El label y el input de la contraseña.
        Label_Password = Label(text='Contrasena:', size_hint_y=0.1, font_size = 25)
        LoginLayout.add_widget(Label_Password)
        self.Input_Password = TextInput(size_hint_y = 0.1, font_size = 24, password = True, multiline=False)
        LoginLayout.add_widget(self.Input_Password)

        # Añadiendo un espacio respecto al boton de login
        Spacer = Widget(size_hint_y = 0.1)
        LoginLayout.add_widget(Spacer)

        # Boton Login
        Btn_Login = Button(text='Login', size_hint_y=0.1, font_size = 25, on_press = self.LoginHandler)
        LoginLayout.add_widget(Btn_Login)

        self.add_widget(LoginLayout)

    def Switch_To_Menu(self):
        self.manager.current = 'menu_screen'

    def LoginHandler(self, value):
        print(f"Login.... {self.Input_Username.text} with password: {self.Input_Password.text}")
        self.Switch_To_Menu()

class OptionsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsMenuScreen, self).__init__(**kwargs)

        MenuLayout = BoxLayout(orientation='vertical')
        MenuLayout.size_hint = (0.6, 0.5)  # Width: 60%, Height: 50%
        MenuLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 

        # Boton para el menu de encriptacion
        Btn_EncryptionScreen = Button(text='Motor de Encriptacion', size_hint_y = 0.1, font_size = 25, on_press = self.Switch_To_EncryptionMenu)
        MenuLayout.add_widget(Btn_EncryptionScreen)

        # Añadiendo un espacio respecto al boton de contrasenas
        Spacer = Widget(size_hint_y = 0.1)
        MenuLayout.add_widget(Spacer)

        # Boton para el menu de gestion de contrasenas
        Btn_PasswordsScreen = Button(text='Gestionar Contraseñas', size_hint_y = 0.1, font_size = 25)
        MenuLayout.add_widget(Btn_PasswordsScreen)

        self.add_widget(MenuLayout)

    def Switch_To_EncryptionMenu(self, value):
        self.manager.current = 'encryption_menu'

class EncryptionApp(App):
    def build(self):
        # Crear el Screen Mananger
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(OptionsMenuScreen(name='menu_screen'))
        sm.add_widget(EncryptionMenu(name='encryption_menu'))

        return sm

    # instance es el widget que generó el evento
    # Value es el valor actual que tiene el widget


if __name__ == "__main__":
    EncryptionApp().run()