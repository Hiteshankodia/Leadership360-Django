import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BS = 16  # Block size for AES

def pad(s):
    padding_length = BS - len(s) % BS
    return s + bytes([padding_length]) * padding_length

def unpad(s):
    padding_length = s[-1]
    return s[:-padding_length]

class AESCipher:
    def __init__(self, key):
        # Key should be exactly 16, 24, or 32 bytes long
        self.key = key.ljust(BS)[:BS].encode()  # Ensure key length is correct

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        iv = get_random_bytes(BS)  # Generate a random IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enc = cipher.encrypt(raw)
        return base64.b64encode(iv + enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:BS]  # Extract IV from the beginning
        enc = enc[BS:]  # Extract the actual encrypted message
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

# Example usage
if __name__ == "__main__":
    key = 'abcdefghijklmnopqrstuvwxyz123456'  # 32-byte key

    aes = AESCipher(key)

    # Example texts
    
    text = str('1:12:31')
    
    encrypted = aes.encrypt(text)
    decrypted = aes.decrypt(encrypted)
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {text == decrypted}\n")
