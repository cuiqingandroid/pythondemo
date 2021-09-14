import rsa
import rsa.transform
import rsa.common
import rsa.core

class Encrypt(object):
    def __init__(self,e,m):
        self.e = e
        self.m = m

    def encrypt(self,message):
        mm = int(self.m, 16)
        ee = int(self.e, 16)
        rsa_pubkey = rsa.PublicKey(mm, ee)
        crypto = self._encrypt(message.encode(), rsa_pubkey)
        return crypto.hex()

    def _pad_for_encryption(self, message, target_length):
        message = message[::-1]
        max_msglength = target_length - 11
        msglength = len(message)

        padding = b''
        padding_length = target_length - msglength - 3

        for i in range(padding_length):
            padding += b'\x00'

        # newMassage = b''
        # for i in message:
        #     newMassage += bytes(i)
        return b''.join([b'\x00\x00',padding,b'\x00',message])

    def _encrypt(self, message, pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, keylength)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, keylength)

        return block


def encrypt(e,m,message):
	en = Encrypt(e,m)
	return en.encrypt(message)

e = '010001'
m = 'E329CFCCF2DC28B6944F30EFC627B647B74A7E5B875369B71EC5E660789CB689795592B499AB526CA6114A2FC479FAB0054FBA494A38D653A321F6630C99AD51C6825CFF11EF7C4DAC55E44BC1786E9BA6D0B10A2BA7ADF8512921D6D18AFFCAF4A1901A54FF1FBF309CFF7A4BDC6269E93DB947FC17617478A4418ED7FD7FB8407A790A371D7B9CD822FC488A8A7AEC160C61EF45C586CD1826F49A90719735FF7045C0411568B990F88B3EBCBDD9BA4AB6FCAD07FEDC73AFA9D92AE0311483F7C1C71141B654F576EB7FD46DD80CCE799A50D99D2BE362CE3F78D1471C017418B5A59E51EDFA82E2B0CFE01B18222F4C64A24E9A1FAEB68BAAB3EA66CCEEF9'
print(encrypt(e, m, "1234"))