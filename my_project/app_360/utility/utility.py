from django.http import HttpResponse
import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import os
from django.conf import settings
from app_360.ServiceHelper.ApiBase import ApiBase
from django.shortcuts import render
apibaseobj = ApiBase()

class UtilityClass: 
    def __init__(self):
        self.bs = AES.block_size
        self.key = b'Sixteen byte key'

    def GetAccessToken(self, request):
        cookie_value = request.COOKIES.get('access_token', 'Cookie not found')
        return HttpResponse(f'The cookie value is: {cookie_value}')
    
    def SaveAccessToken(self,request,   access_token):
        response = HttpResponse("Cookie has been set")
        response.set_cookie('access_token', access_token)
        return response
        

    def FetchCompanyid(self,request, companyurl):
        company_id_json = request.COOKIES.get('company_id')
    
        if not company_id_json:
            # Cookie not present, fetch company ID
            url = request.build_absolute_uri()
            data = {'companyurl': str(companyurl)}
            response_data = self.apibaseobj.PostRequest(data = data, url='/masterdata/fetchcompanyid', token='')  # Assuming this returns a dict or similar structure
            company_id = response_data.get('companyid')
            
            # Create an HttpResponse object
            response = HttpResponse("Saved Successfully!")
                
            # Set the cookie in the response
            response.set_cookie('company_id', str(company_id))
            
            # Debugging information
            print('Cookie set:', response.cookies)
            print('Company ID:', company_id)
            
            return company_id  


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

   