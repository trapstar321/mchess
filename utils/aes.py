import pyaes

def encrypt(key, data):
    aes = pyaes.AESModeOfOperationCTR(key.encode('UTF-8'))
    return aes.encrypt(data)

def decrypt(key, data):
    counter = pyaes.Counter()
    aes = pyaes.AESModeOfOperationCTR(key.encode('UTF-8'), counter=counter)
    return aes.decrypt(data)

def to_hex(encrypted):
    return encrypted.hex()

def from_hex(hex):
    return bytes.fromhex(hex)

if __name__=="__main__":
    key = "12345678901234567890123456789012"
    ciphertext = encrypt(key, "Hello there")
    hex = to_hex(ciphertext)
    ciphertext = from_hex(hex)
    decrypted = decrypt(key, ciphertext)
    print(decrypted)

