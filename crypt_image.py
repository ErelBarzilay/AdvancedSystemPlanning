from PIL import Image
import hashlib
import numpy
from PyCryptodome import AES
class CryptImage:
    def __init__(self, image, key_hash):
        self.image = image
        self.key_hash = key_hash
    
    def encrypt(self, key):
        m = hashlib.sha256()
        m.update(bytes(key))
        key = m.digest()
        m.update(m.digest())
        self.key_hash = m.digest()
        im = numpy.asarray(self.image)
        cipher = AES.new(key, AES.MODE_EAX)
        cipher.nonce = "arazim"
        ciphertext = cipher.encrypt_and_digest(im)
        self.image = Image.fromarray(ciphertext)
    
    def decrypt(self, key):
        m = hashlib.sha256()
        m.update(bytes(key))
        if (m.digest() == self.key_hash):
            self.key_hash = None
            im = numpy.asarray(self.image)
            cipher_aes = AES.new(m.digest(), AES.MODE_EAX, "arazim")
            data = cipher_aes.decrypt_and_verify(im)
            self.image = Image.fromarray(data)
    @classmethod
    def create_from_path(cls, path):
        obj = CryptImage(Image.open(path),None)
        return obj
