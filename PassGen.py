import os
import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def gKey(reqs, length):
    length = int(length)
    reqs = int(reqs)
    if reqs == 5:
        return ''.join(random.choice("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""") for a in range(length))
    elif reqs == 4:
        return ''.join(random.choice("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890""") for a in range(length))
    elif reqs == 3:
        return ''.join(random.choice("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""") for a in range(length))
    elif reqs == 2:
        return ''.join(random.choice("""ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890""") for a in range(length))
    elif reqs == 1:
        return ''.join(random.choice("""abcdefghijklmnopqrstuvwxyz1234567890""") for a in range(length))

print "Please select required strength of the key/password:"
print "(1) Alphanumeric lowecase only"
print "(2) Alphanumeric upercase only"
print "(3) Alpha only, Case sensitive"
print "(4) Alphanumeric Case sensitive"
print "(5) Alphanumeric, Case sensitive, Special Characters"
kReq = raw_input("Selection: ")
length = raw_input("Key/pass length: ")

kVal = gKey(kReq, length)
print kVal, len(kVal)
