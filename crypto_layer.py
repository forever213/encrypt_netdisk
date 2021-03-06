from kem import *
import SM4 as AES 

class cipher(object):
    def __init__(self, policy, password):
        self.policy = policy
        self.pw = password
        self.sym_key = {}
    
    def encrypt(self, message, key = False):
        kemObj = kem(self.policy, key = key)
        self.sym_key['sym_key'], self.sym_key['sym_key_cipher'], self.sym_key['key'] = kemObj.gen_key(self.pw)

        symObj = AES.AESCipher(self.sym_key['sym_key'])
        cipher_text = symObj.encrypt(message)

        return self.sym_key, cipher_text

    def decrypt(self, sym_key_cipher, cipher_text, attr, pk):
        kemObj = kem(self.policy, key = pk)

        skx = kemObj.cpabe_key(attr, pk)
        dec_key = kemObj.get_key(sym_key_cipher, pk, skx)

        symObj = AES.AESCipher(dec_key)
        plain = symObj.decrypt(cipher_text)

        return plain

def main():
    pol = '(ONE or THREE) and (TWO or FOUR)'
    pw = input('password:>>')
    cipherObj = cipher(pol, pw)
    plain = input('plain:>>')
    key, cipher_text = cipherObj.encrypt(plain)

    print(key)
    print(cipher_text)

    attr = ['THREE', 'ONE', 'TWO']
    plain = cipherObj.decrypt(key['sym_key_cipher'], cipher_text, attr, key['key'])

    print(plain)

if __name__ == '__main__':
    main()        