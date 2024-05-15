class EncryptionKey:
    # Representa la clave en la aplicación

    def __init__( self, name, value, authentication_key )  :
        self.name = name
        self.value = value
        self.authentication_key = authentication_key

    def __repr__(self) -> str:
        return f"Name: {self.name}, Key: {self.key}, Authentication Key: {self.authentication_key}"