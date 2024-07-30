from django.http import HttpResponse
import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import os
from django.conf import settings

class UtilityClass: 
    def __init__(self):
        self.bs = AES.block_size
        self.key = b'Sixteen byte key'


    def SaveAccessToken(self, access_token):
        response = HttpResponse('Login successful')
        response.set_cookie('access_token', access_token, max_age=3600, httponly=True, samesite='Strict')

    def _pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

    def decrypt(self, enc):
        print("HII")
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        a =  self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        print(a)
        return a
    
    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
    
if __name__ == "__main__":
    key = b'Sixteen byte key'
    aes = UtilityClass()

    encrypted = aes.encrypt('109')
    print(encrypted)
    # Decrypting the encrypted message
    decrypted = aes.decrypt('t9muUKolsa7H2qROZE2ujQORhNRGkU5gTapOuAsyn8Y=')
    
    print("Decrypted:", decrypted) 

   