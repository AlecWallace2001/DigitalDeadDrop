    #PassGen - Complex password generation script
    #Copyright (C) 2017 Lee Bratina

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
