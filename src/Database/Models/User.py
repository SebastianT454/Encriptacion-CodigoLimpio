class User:
    # Representa el Usuario en la aplicación que tiene una claves asociadas

    def __init__( self, name, password, encryption_keysIds )  :
        self.name = name
        self.password = password
        self.encryption_keysIds = encryption_keysIds

    def __repr__(self) -> str:
        return f"Name: {self.name}, Password: {self.password}, Encryption Keys Ids: {self.encryption_keysIds}"

    """
    def isEqual( self, compare_to ) :
        #Compara el objeto actual, con otra instancia de la clase Usuario
        
        assert( self.name == compare_to.name )
        assert( self.password == compare_to.password )
        assert( self.encryption_keysIds == compare_to.encryption_keysIds )
        
        return True
    """
        
    def addEncryptionKey(self, key):
        self.encryption_keysIds.append(key)