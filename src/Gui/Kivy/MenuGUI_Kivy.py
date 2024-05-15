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
import Database.Controllers.UserController as UserController

#////////////////////////////// FUNCTIONS //////////////////////////////////////////////

class OptionsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsMenuScreen, self).__init__(**kwargs)

        MenuLayout = BoxLayout(orientation='vertical')
        MenuLayout.size_hint = (0.6, 0.5)  # Ancho: 60%, Alto: 50%
        MenuLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 

        # Boton para el menu de encriptacion
        Btn_EncryptionScreen = Button(text='Motor de Encriptacion', size_hint_y = 0.1, font_size = 25, on_press = self.Switch_To_EncryptionMenu)
        MenuLayout.add_widget(Btn_EncryptionScreen)

        # Añadiendo un espacio respecto al boton de contrasenas
        Spacer = Widget(size_hint_y = 0.1)
        MenuLayout.add_widget(Spacer)

        """
        Funcionalidad incompleta - Opcional para descartar para la entrega final, de lo contrario.
        Este apartado se tenia pensado para visualizar todas las claves guardadas del usuario, poder
        Eliminarlas o actualizarlas.

        # Boton para el menu de gestion de contrasenas
        Btn_PasswordsScreen = Button(text='Gestionar Contraseñas', size_hint_y = 0.1, font_size = 25)
        MenuLayout.add_widget(Btn_PasswordsScreen)
        
        # Añadiendo un espacio respecto al boton de eliminar cuenta
        Spacer = Widget(size_hint_y = 0.1)
        MenuLayout.add_widget(Spacer)
        """

        # Boton para eliminar la cuenta de usuario
        Btn_DeleteUser = Button(text='Borrar Cuenta', size_hint_y = 0.1, font_size = 25, on_press = self.DeleteUserHandler)
        MenuLayout.add_widget(Btn_DeleteUser)

        self.add_widget(MenuLayout)

    def Switch_To_EncryptionMenu(self, value):
        self.manager.current = 'encryption_menu'

    def Switch_To_LoginMenu(self):
        self.manager.current = 'login_screen'
        self.manager.User = None

    def DeleteUserHandler(self, value):
        UserController.DeleteUser(self.manager.User.name)
        self.Switch_To_LoginMenu()