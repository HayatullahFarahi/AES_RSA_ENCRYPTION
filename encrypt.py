import json
from base64 import b64encode

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


class Encrypt:

    def encrypt_data(self):
        f = open('credentials.json',)
        credentials = json.load(f)
        key, iv = Random.new().read(32), Random.new().read(16)
        credentials = self.aes_encrypt(AES.MODE_GCM, credentials, key, iv)
        secret = {"key": key, "iv": iv}
        secret = str(secret).encode('utf-8')
        secrets = self.public_encrypt(secret)
        final_data = {'data': credentials.decode('utf-8'), 'secret': secrets.decode('utf-8')}
        print(final_data)
        f = open('final_data.txt', 'w')
        f.write(str(final_data))
        f.close()

    def public_encrypt(self, data):
        public_key = RSA.import_key(open('public.pem', 'r').read())
        if type(data) == str:
            data = data.encode('utf-8')
        elif type(data) == dict:
            data = str(json.dumps(data)).encode('utf-8')
        if type(data) == bytes:
            cipher = PKCS1_OAEP.new(key=public_key)
            return b64encode(cipher.encrypt(data))
        raise TypeError('can only encrypt the following types str, dict, bytes')

    def aes_encrypt(self, mode, message, key, iv):
        if type(message) == str:
            message = message.encode('utf-8')
        elif type(message) == dict:
            message = str(json.dumps(message)).encode('utf-8')
        if type(message) == bytes:
            cipher = AES.new(key, mode, iv)
            return b64encode(cipher.encrypt(message))
        raise TypeError('can only encrypt the following types str, dict, bytes')

api = Encrypt()
api.encrypt_data()