import win32com.client
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
import os
import re
import base64
import random
import time

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
        return ''.join(random.choice("""abcdefghijklmnopqrstuvwxyz1234567890"""))

raw_input("Please verify that your physical drive has been named before pressing enter to continue.")
strComputer = "." 
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
DriveInfo = []
for objItem in colItems:
    DriveInfo.append([objItem.DeviceID, objItem.Size, objItem.VolumeSerialNumber, objItem.VolumeName])
runs = 0
vYes = raw_input("Will you be using a mounted encrypted disc(y/n)? ")
vYes = vYes.lower()
if vYes == 'y':
    raw_input("Please make sure you have mounted the drive. Press enter to continue.")

print "The following drives are found on your system."
for i in DriveInfo:
    print str(runs) + ') '+str(i[0])
    runs +=1
pDrive = raw_input("Please select the physical drive you will be using: ")
if vYes == 'y':
    vDrive = raw_input("Please select the mounted drive you will be using: ")
    os.chdir(DriveInfo[int(vDrive)][0])
else:
    os.chdir(DriveInfo[int(pDrive)][0])

sBranch = raw_input("Do you want to to have the encryption keys generated for you(y/n)?")
sBranch = sBranch.lower()

if sBranch == 'y':
    ekOne = gKey('5', '32')
    print "Your first key is: " + ekOne
    ekTwo = gKey('5', '16')
    print "Your second key is: " + ekTwo
    Salt = gKey('5', '32')
    print "Your salt is: " + Salt
else:
    print "The first key needs to be 32 characters long. If the key you enter is longer, it will be truncated. If it is shorter, additional characters will be appended."
    ekOne = raw_input("Enter the first key: ")
    if len(ekOne) > 32:
        ekOne = ekOne[:31]
    elif len(ekOne) < 32:
        ekOne = ekOne + gKey('5', 32-len(ekOne))
    print "Your first key is: " + ekOne
    print "The second key needs to be 16 characters long. If the key you enter is longer, it will be truncated. If it is shorter, additional characters will be appended."
    ekTwo = raw_input("Enter the first key: ")
    if len(ekTwo) > 16:
        ekTwo = ekTwo[:16]
    elif len(ekTwo) < 32:
        ekTwo = ekTwo + gKey('5', 16-len(ekTwo))
    print "Your second key is: " + ekTwo
    print "The salt needs to be at least 32 characters long. If it is shorter, additional characters will be appended."
    Salt = raw_input("Enter the first key: ")
    if len(Salt) < 32:
        Salt = Salt + gKey('5', 32-len(Salt))
    print "Your first key is: " + Salt
    
print "32 character string will be constructed now using (Serial A) + (Serial B) seeded with (Name A)"
print DriveInfo[int(pDrive)]
if vYes == 'y':
    print DriveInfo[int(vDrive)]
print "Serial A " + DriveInfo[int(pDrive)][2]
if vYes == 'y':
    print "Serial B " + DriveInfo[int(vDrive)][2]
print "Name A " + DriveInfo[int(pDrive)][3]
if vYes == 'y':
    preSeeded = DriveInfo[int(pDrive)][2] + DriveInfo[int(vDrive)][2]
else:
    preSeeded = DriveInfo[int(pDrive)][2] + DriveInfo[int(pDrive)][2]
salt = DriveInfo[int(pDrive)][3]
sRun = len(salt)
print len(preSeeded)
print preSeeded
sText = ''
for i in range(0, len(preSeeded)-1):
    if sRun == 0:
        sRun = len(salt)
    sRun -=1
    sText = sText + preSeeded[i] + salt[sRun]
    print sText
h = SHA512.new()
h.update(sText)
        #h = SHA512.new()
        #h.update(raw_decrypted)
dHash = h.hexdigest()

print "Seeded Value " + sText
print "Hashed Value " + dHash
print "Secret Key 1: " + dHash[:32] + "   " + str(len(dHash[:32]))
print "Secret Key 2: " + dHash[32:48] + "   " + str(len(dHash[32:48]))

tbEnc = dHash + '||' + ekOne + '||' + ekTwo + '||' + Salt + '||'
print tbEnc
obj = AES.new(dHash[:32], AES.MODE_CFB, dHash[32:48])
encEnc = base64.b64encode(obj.encrypt(tbEnc))
print encEnc
encFile = open('nEncFile', 'w')
encFile.write(encEnc)
encFile.close()
