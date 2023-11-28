from asyncio.windows_events import NULL
from PIL import Image
import hashlib
import numpy
from Crypto.Cipher import AES
class CryptImage:
    def __init__(self, image, key_hash = None):
        self.image = image
        self.key_hash = key_hash
        self.tag = NULL
    def encrypt(self, key):
        m = hashlib.sha256()
        m.update(bytes(key))
        key = m.digest()
        m.update(m.digest())
        self.key_hash = m.digest()
        shape = self.image.size
        im = list(self.image.getdata())
        im = [bytes(x) for x in im]
        x = im[0]
        for i in range(1,len(im)):
            x = x + im[i]
        im = x
        cipher = AES.new(key, AES.MODE_EAX)
        cipher.nonce = "arazim"
        ciphertext = cipher.encrypt_and_digest(im)
        self.tag = ciphertext[1]
        ciphertext = numpy.frombuffer(ciphertext[0], dtype = numpy.uint8)
        curr = [(ciphertext[3*i],ciphertext[3*i + 1], ciphertext[3*i + 2]) for i in range(int(len(ciphertext)/3))]
        im = Image.new('RGB', shape, 255)
        data = im.load()
        im.putdata(curr)
    def decrypt(self, key):
        m = hashlib.sha256()
        m.update(bytes(key))
        if (m.digest() == self.key_hash):
            self.key_hash = None
            im = numpy.asarray(self.image)
            cipher_aes = AES.new(m.digest(), AES.MODE_EAX, "arazim")
            data = cipher_aes.decrypt_and_verify(im)
            self.image = Image.fromarray(data)
        self.image.show()
    @classmethod
    def create_from_path(cls, path):
        obj = CryptImage(Image.open(path),None)
        return obj
