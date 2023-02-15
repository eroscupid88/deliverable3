#!urs/bin/python3
from cryptography.fernet import Fernet
import os
class EncryptionObject(object):
    """
        Constructor of EncrytpionObject 
    """
    def __init__(self,path):
        super().__init__()
        self.path = path
        self.cipher_key = self.generateKey()
    """
        getKey function return a cipher_key
        prams: None
        return a String type
    """
    def getKey(self):
        return self.cipher_key

    """
        generateKey function generate a cipher_key and return it as a string
        prams: None
        return : a String type
    """
    def generateKey(self):
        cipher_key= ''
        if not os.path.isfile(self.path):
            cipher_key = Fernet.generate_key()
            with open(self.path,'wb') as filekey:
                filekey.write(cipher_key)
        else:
            with open(self.path,'rb') as filekey:
                cipher_key = filekey.read().strip()
        return cipher_key


    """
        generateCipher function generate cipher for encryption purposes
        prams: None
        return: None
    """
    def generateCipher(self):
        return Fernet(self.cipher_key)

    """
        encryptMessage function taking a encode message as parameter and encryp        ted and return a string
        pram : 
            decodeMessage : type UTF-8
        return: a String
    """

    def encryptMessage(self,encodeMessage):
        cipher = self.generateCipher()
        return cipher.encrypt(encodeMessage)

    """
        decryptMessage function taking encrypted message as parameter and decrip        t and return a string
        pram : 
            encryptedMessage : type String
        return: a String
    """
    def decryptMessage(self,encryptedMessage):
        cipher = self.generateCipher()
        return cipher.decrypt(encryptedMessage).decode()


