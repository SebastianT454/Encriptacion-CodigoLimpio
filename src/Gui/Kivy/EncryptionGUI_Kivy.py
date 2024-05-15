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

# Logica de las funciones kivy
from Gui.GuiLogic.Kivy.EncryptionGUI_KivyLogic import *

# Modulos de base de datos para el Usuario.
from Database.Models.User import User
import Database.Controllers.UserController as UserController

# Modulos de base de datos para la Clave.
from Database.Models.EncryptionKey import EncryptionKey
import Database.Controllers.EncryptionKeyController as EncryptionKeyController

#////////////////////////////// GRAPHIC CONTENT //////////////////////////////////////////////

# Importando el apartado grafico del ingreso a la app.
from LoginGUI_Kivy import LoginScreen

# Importando el apartado grafico del menu de la app.
from MenuGUI_Kivy import OptionsMenuScreen

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
        MainContainer.add_widget( Label(text="Mensaje", font_size = 20) )
        self.Input_message = TextInput(font_size = 24, multiline = False)
        MainContainer.add_widget(self.Input_message)

        # Conectar con el callback con el evento on_text_validate para determinar si el mensaje es valido.
        self.Input_message.bind( on_text_validate = self.ValidateMessage)

        #---------------------------------- Boton - Label Generar Key -------------------------------------------

        Btn_Key = Button(text="Generar Clave",font_size = 30)
        MainContainer.add_widget(Btn_Key)

        # Conectar con el callback con el evento press del boton de generar clave.
        Btn_Key.bind( on_press = self.GenerateAutomaticKey )

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

        GridLayout_KeyLabels.add_widget( Label(text="Tamano Clave", font_size = 20, size_hint = (0.3, 1) ) )

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
        Btn_SavePassword = Button(text="Guardar Clave", font_size = 30)
        GridLayout_KeyButtons.add_widget(Btn_SavePassword)

        # Conectar con el callback con el evento press del boton guardar contraseña.
        Btn_SavePassword.bind( on_press= self.SaveKeyPopup )

        Btn_SelectKey = Button(text="Claves Guardadas", font_size = 30)
        GridLayout_KeyButtons.add_widget(Btn_SelectKey)

        # Conectar con el callback con el evento press del boton de generar clave.
        Btn_SelectKey.bind( on_press = self.SelectSavedKey )

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
        Btn_Decrypt.bind( on_press = self.DecryptMessage )

        MainContainer.add_widget( Label(text="Mensaje Desencriptado", font_size = 20) )
        self.Input_DecryptedMessage = TextInput(font_size=24)
        MainContainer.add_widget(self.Input_DecryptedMessage)

        #---------------------------------- Boton (Volver al menu) ------------------------------------------

        Btn_Return_To_Menu = Button(text="Volver al menu", font_size = 30)
        MainContainer.add_widget(Btn_Return_To_Menu)

        # Conectar con el callback con el evento press del boton encriptar.
        Btn_Return_To_Menu.bind( on_press = self.Switch_To_Menu )

        # Size Hint (widht, Alto) = representa el espacio que se quiere utilizar en su totalidad 1 = 100% de la Window screen.
        # Size = tamaño que va tomar, en este caso el tamaño de la Window screen de ancho y alto.

        Scroll_MainContainer = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        Scroll_MainContainer.add_widget(MainContainer)

        self.add_widget(Scroll_MainContainer)

    def Switch_To_Menu(self, value):
        """
        Funcion para cambiar entre ventanas
        """
        self.manager.current = 'menu_screen'
      
    def ShowError( self, err ):
        """
        Funcion para desplegar el error de alguno de las operaciones.
        """
        GridLayout_ErrorContent = GridLayout(cols = 1)
        GridLayout_ErrorContent.add_widget( Label(text= str(err) ) )
        Btn_Close = Button(text="Cerrar" )
        GridLayout_ErrorContent.add_widget( Btn_Close )
        Popup_widget = Popup(title="Error", content = GridLayout_ErrorContent)
        Btn_Close.bind( on_press= Popup_widget.dismiss)
        Popup_widget.open()
        return False
    
    def SaveKeyPopup(self, value):
        """
        Funcion grafica para guardar una clave en el usuario actual.
        """

        # Verificar si la clave y el mensaje son validos.
        ValidKey = self.ValidateKey(value)

        if ValidKey:
            try:
                GridLayout_SaveKey = BoxLayout(orientation='vertical')

                GridLayout_SaveKey.size_hint = (0.6, 0.5)  # Ancho: 60%, Alto: 50%
                GridLayout_SaveKey.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 

                # Input para el nombre de la clave.
                GridLayout_SaveKey.add_widget( Label(text= "Nombre para la clave:" , size_hint_y=0.1, font_size = 25) )
                self.Input_KeyName = TextInput(size_hint_y=0.1, font_size = 25)
                GridLayout_SaveKey.add_widget( self.Input_KeyName )

                # Input para la clave de autenticacion.
                GridLayout_SaveKey.add_widget( Label(text= "Escribe la clave de autenticacion:" , size_hint_y=0.1, font_size = 25) )
                self.Input_NewAuthenticationKey = TextInput(size_hint_y=0.1, font_size = 25)
                GridLayout_SaveKey.add_widget( self.Input_NewAuthenticationKey )

                # Añadiendo un espacio respecto al boton de guardar contraseña.
                Spacer = Widget(size_hint_y = 0.1)
                GridLayout_SaveKey.add_widget(Spacer)

                # Boton para guardar la contraseña
                Btn_SaveKey = Button(text="Guardar" , size_hint_y=0.1, font_size = 25)
                GridLayout_SaveKey.add_widget( Btn_SaveKey )
                Btn_SaveKey.bind( on_press= self.AddKeyToUserHandler )

                # Añadiendo un espacio respecto al boton de cerrar.
                Spacer = Widget(size_hint_y = 0.1)
                GridLayout_SaveKey.add_widget(Spacer)

                # Boton para cerrar el popup
                Btn_Close = Button(text="Cerrar" , size_hint_y=0.1, font_size = 25)
                GridLayout_SaveKey.add_widget( Btn_Close )

                Popup_widget = Popup(title="Guardar Clave", content = GridLayout_SaveKey)
                Btn_Close.bind( on_press= Popup_widget.dismiss)
                Popup_widget.open()

            except Exception as err:
                self.ShowError( err )

    def AddKeyToUserHandler(self, value):
        """
        Funcion que gestiona el ingreso de una nueva clave a un usuario.
        """
        try:
            # Obteniendo la información necesaria para el objeto de tipo clave.
            KeyName = self.Input_KeyName.text
            Key = self.Input_Key.text
            AuthenticationKey = self.Input_NewAuthenticationKey.text

            # Obteniendo el Usuario.
            User = self.manager.User

            if KeyName == "" or AuthenticationKey == "":
                raise Exception(f"El nombre o la clave de autenticacion están vacias." )
            
            KeyObject = EncryptionKey(KeyName, Key, AuthenticationKey)

            AddKeyToUser(User, KeyObject)
            
        except Exception as err:
            self.ShowError( err ) 

    def SelectSavedKey(self, value):
        """
        Funcion que desplega los componentes graficos para visualizar las claves que el usuario tiene.
        """
        
        # Verificar que el usuario minimo tenga 1 clave.
        User = self.manager.User
        AmountOfSavedKeys = GetAmountOfKeys(User)

        if AmountOfSavedKeys == 0:
            raise Exception(f"Usted no tiene claves guardadas!" )

        # Definiendo una lista para guardar los botones
        KeyButtons = []

        # Definiendo una lista para guardar las ids de cada clave existente y el nombre de las claves.
        KeysNames = EncryptionKeyController.GetKeysNames( User )

        GridLayout_Keys = GridLayout(cols = 1)
        GridLayout_Keys.add_widget( Label(text= "Claves" , font_size = 25) )

        for KeyName in KeysNames:
            Btn = Button(text = f"{KeyName}", font_size = 25, on_press = self.ValidateAuthenticationKeyGUI)

            # Agregar el boton en el grid.
            GridLayout_Keys.add_widget(Btn)

            # Agregar el boton en la lista de botones
            KeyButtons.append(Btn)

        # Añadiendo un espacio respecto al boton de Cerrar
        Spacer = Widget(size_hint_y = 0.1)
        GridLayout_Keys.add_widget(Spacer)

        # Boton para cerrar el popup
        Btn_Close = Button(text="Cerrar" , font_size = 25)
        GridLayout_Keys.add_widget( Btn_Close )

        self.Popup_widget_SelectKey = Popup(title="Claves Guardadas", content = GridLayout_Keys)
        Btn_Close.bind( on_press = self.Popup_widget_SelectKey.dismiss)
        self.Popup_widget_SelectKey.open()
    
    def ValidateAuthenticationKeyGUI(self, Btn):
        """
        Funcion grafica que desplega el contenido para verificar si la clave es correcta.
        """
         
        try:
            # Obtener el nombre de la clave através del boton.
            self.BtnNameToAuthenticate = Btn.text

            # Crear el grid para validar la clave.
            GridLayout_Authenticationkey = BoxLayout(orientation='vertical')

            GridLayout_Authenticationkey.size_hint = (0.6, 0.5)  # Ancho: 60%, Alto: 50%
            GridLayout_Authenticationkey.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 

            # Input para la clave de autenticacion.
            GridLayout_Authenticationkey.add_widget( Label(text= "Escribe la clave de autenticacion:" , size_hint_y=0.1, font_size = 25) )
            self.Input_AuthenticationKey = TextInput(size_hint_y=0.1, font_size = 25)
            GridLayout_Authenticationkey.add_widget( self.Input_AuthenticationKey )

            # Añadiendo un espacio respecto al boton de guardar contraseña.
            Spacer = Widget(size_hint_y = 0.1)
            GridLayout_Authenticationkey.add_widget(Spacer)

            # Boton para enviar y verificar la contraseña
            Btn_SaveKey = Button(text="Enviar" , size_hint_y=0.1, font_size = 25)
            GridLayout_Authenticationkey.add_widget( Btn_SaveKey )
            Btn_SaveKey.bind( on_press= self.ValidateAuthenticationKey )

            # Añadiendo un espacio respecto al boton de cerrar.
            Spacer = Widget(size_hint_y = 0.1)
            GridLayout_Authenticationkey.add_widget(Spacer)

            # Boton para cerrar el popup
            Btn_Close = Button(text="Cerrar" , size_hint_y=0.1, font_size = 25)
            GridLayout_Authenticationkey.add_widget( Btn_Close )

            self.Popup_widget_ValidateAuthenticationKey = Popup(title="Validar Clave", content = GridLayout_Authenticationkey)
            Btn_Close.bind( on_press= self.Popup_widget_ValidateAuthenticationKey.dismiss)
            self.Popup_widget_ValidateAuthenticationKey.open()

        except Exception as err:
            self.ShowError( err )

    def ValidateAuthenticationKey(self, value):
        """
        Funcionalidad que verifica si la clave de verificacion es correcto o no, si lo es, es colacada como clave para encriptar.
        """

        # Obtenemos el nombre del boton que llamo la funcion que sera el nombre de la key.
        BtnName = self.BtnNameToAuthenticate

        # Obtenemos la clave de verificacion ingresada por el usuario y comprobamos.
        AuthenticationKeyEntered = self.Input_AuthenticationKey.text

        try:
            if AuthenticationKeyEntered == "":
                raise Exception(f"La clave de autenticación esta vacia!" )

            KeyObject = EncryptionKeyController.GetKeyByName( BtnName, AuthenticationKeyEntered )
            KeyValue = KeyObject.value

            # Minimizar los dos popups que se tenian.
            self.Popup_widget_ValidateAuthenticationKey.dismiss()
            self.Popup_widget_SelectKey.dismiss()

            # Agregar la clave para la encriptacion.
            self.Input_Key.text = KeyValue
            self.Spinner_KeySize.text = SetSizeVerifiedKey(KeyValue)

        except Exception as err:
            self.ShowError( err )
            return False

    def GenerateAutomaticKey(self, value):
        """
        Si se presiona el boton generar clave, este
        Automaticamente generara una clave y la pondra en Input_Key
        """

        KeySize = int(self.Spinner_KeySize.text)

        self.Input_Key.text = GenerateAutomaticKeyLogic(KeySize)

    def GenerateKey(self, value):
        """
        Retorna el formato de la string de forma ordenada
        """
        
        KeySize = int(self.Spinner_KeySize.text)
        Key = self.Input_Key.text

        return GenerateKeyLogic(KeySize, Key)

    def ValidateMessage(self, value):
        """
        Verificar si el mensaje tiene caracteres validos para la encriptacion,
        es decir si sus caracteres estan en el diccionario de letras en Encryption Logic
        """

        Message = self.Input_message.text  # El texto del TextInput

        return ValidateMessageLogic(Message)

    def ValidateKey(self, value):
        """
        Funcion que verifica si la clave es valida para generarse.
        """
        KeySize = self.Spinner_KeySize.text
        Key = self.Input_Key.text

        return ValidateKeyLogic(KeySize, Key)

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

class EncryptionApp(App):
    def build(self):
        # Crear el Screen Mananger para multiples ventanas.
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(OptionsMenuScreen(name='menu_screen'))
        sm.add_widget(EncryptionMenu(name='encryption_menu'))

        return sm

if __name__ == "__main__":
    EncryptionApp().run()