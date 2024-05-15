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

# Modulos de base de datos para el Usuario.
from Database.Models.User import User
import Database.Controllers.UserController as UserController

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        LoginLayout = BoxLayout(orientation='vertical')

        LoginLayout.size_hint = (0.6, 0.5)  # Ancho: 60%, Alto: 50%
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
        Btn_Login = Button(text='Ingresar', size_hint_y=0.1, font_size = 25, on_press = self.LoginHandler)
        LoginLayout.add_widget(Btn_Login)

        # Añadiendo un espacio respecto al boton de registrarse
        Spacer = Widget(size_hint_y = 0.1)
        LoginLayout.add_widget(Spacer)

        # Boton Registrarse
        Btn_SignIn = Button(text='Registrarse', size_hint_y=0.1, font_size = 25, on_press = self.SignInHandler)
        LoginLayout.add_widget(Btn_SignIn)

        self.add_widget(LoginLayout)

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
    
    def Switch_To_Menu(self, User):
        """
        Funcion para cambiar al menu, si el login es correcto.
        """

        self.manager.current = 'menu_screen'
        self.manager.User = User

    def VerifyUsernameAndPasswordLen(self):
        """
        Verifica si la contraseña o el usuario no están vacios.
        """

        if self.Input_Username.text == "" or self.Input_Password.text == "":
            raise Exception("El usuario o la contraseña están vacias!")
        
    def SignInHandler(self, value):
        """
        Funcion que verifica y registra el usuario.
        """

        try:
            self.VerifyUsernameAndPasswordLen()

            Username = self.Input_Username.text
            Password = self.Input_Password.text

            # Por defecto será una string que esta en el formato 1,9,4,10 donde cada numero representa el Id dentro la base de datos.
            EncryptionKeyList = "" # Siempre vacia.

            # Verificamos que usuario no exista.

            UserExists = UserController.VerifyUserExistance( Username )

            if UserExists:
                raise Exception(f"El usuario {Username} ya existe!")
            
            UserToAdd = User(Username, Password, EncryptionKeyList)
            UserController.InsertIntoTable(UserToAdd)

            self.Switch_To_Menu(UserToAdd)

        except Exception as err:
            return self.ShowError( err )

    def LoginHandler(self, value):
        """
        Funcion que verifica y valida el ingreso del usuario a la App.
        """

        try:
            self.VerifyUsernameAndPasswordLen()

            Username = self.Input_Username.text
            Password = self.Input_Password.text

            # Verificamos que usuario no exista.
            UserExists = UserController.VerifyUserExistance( Username )

            if not UserExists:
                raise Exception(f"El usuario {Username} no existe!")
            
            DesiredUser = UserController.GetUserByUsername( Username )
            
            if Username == DesiredUser.name and Password == DesiredUser.password: 
                #print(f"Ingreso Exitoso.... {self.Input_Username.text}")
                self.Switch_To_Menu(DesiredUser)
            else:
                raise Exception("La contraseña o el usuario están incorrectos!")
        
        except Exception as err:
            return self.ShowError( err )