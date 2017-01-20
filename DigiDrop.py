import os
from Crypto.Cipher import AES
import smtplib
import imaplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from Crypto.Hash import SHA512
import base64
import re
import time

def GetEncKey():
    print "Get Encryption Key"

def CheckEmail(username, password, server, port):
    m = imaplib.IMAP4_SSL(server)
    rv, data = m.login(username, password)
    rv, data = m.select('INBOX')
    numEmails = int(data[0])
    emailList =[]
    runsEmail = 0
    while numEmails >= 0:
        rv, data = m.fetch(numEmails, '(RFC822)')
        if len(re.findall('encCode', data[0][1])) >= 1:
            emailList.append(data[0][1])
        numEmails -=1
        runsEmail +=1
        if numEmails == 0:
            return emailList
        if runsEmail >= 100:
            return emailList
    print "Check Email"

def DecryptEmail(eList, encKey, salt, encValue):
    clear_val = []
    emailNum = len(eList)
    runs = 1
    for i in eList:
        print "Decrypt Email"
        masterDec = str(i).replace('\r', ' ')
        masterDec = masterDec.replace('\n', ' ')
        decoding = masterDec
        fPart = decoding.find('7bit')
        decoding = decoding[fPart+8:]
        lPart = decoding.find('  --==')
        decoding = decoding[:lPart]
        dec_secret = AES.new(encKey,AES.MODE_CFB, encValue)
        raw_decrypted = dec_secret.decrypt(base64.b64decode(decoding))
        sHash = masterDec
        fHash = sHash.find('Subject:')
        sHash = sHash[fHash+9:]
        lHash = sHash.find('    --==')
        sHash = sHash[:lHash]
        sText = ''
        sRun = len(salt)
        for i in range(0, len(raw_decrypted)-1):
            if sRun == 0:
                sRun = len(salt)
            sRun -=1
            sText = raw_decrypted[i] + salt[sRun]
        h = SHA512.new()
        h.update(sText)
        #h = SHA512.new()
        #h.update(raw_decrypted)
        dHash = h.hexdigest()
        if sHash == dHash:
            print "("+str(runs)+'/'+str(emailNum)+')'
            print "Encrypted Message is believed to be valid"
            print "Encrypted Message:"
            print decoding
            print "Decrypted Message:"
            print raw_decrypted
            print ""
            print "Subject Hash:"
            print sHash
            print "Decrypted Hash:"
            print dHash
            runs +=1
        else:
            print "("+str(runs)+'/'+str(emailNum)+')'
            print "Encrypted Message has been tampered with and cannot be trusted"
            print "Encrypted Message:"
            print decoding
            print "Decrypted Message:"
            print raw_decrypted
            print ""
            print "Subject Hash:"
            print sHash
            print "Decrypted Hash:"
            print dHash
            runs +=1
        raw_input('Press enter to continue.')
        os.system('cls')
        os.system('clear')
    return clear_val

def CreateEmail():
    print "Create Email"
    tEmail = raw_input("Enter the Email Address: ")
    eText = raw_input("Enter the message: ")
    return eText, tEmail

def EncryptEmail(eText, encKey, uName, salt, encValue):
    print "Encrypting Email"
    obj = AES.new(encKey, AES.MODE_CFB, encValue)
    #eEncrypted = obj.encrypt(eText)
    cipher_text = base64.b64encode(obj.encrypt(eText))
    sText = ''
    sRun = len(salt)
    for i in range(0, len(eText)-1):
        if sRun == 0:
            sRun = len(salt)
        sRun -=1
        sText = eText[i] + salt[sRun]
    h = SHA512.new()
    h.update(sText)
    eHash = h.hexdigest()
    eNum = uName.find('@')
    nName = uName[:eNum]
    fName = nName + str(eHash)[len(str(eHash))-2:]
    return eHash, cipher_text, fName

def SendEmail(eHash, eEncrypted, fName, uName, uPass, server, port, tEmail):
    print "Sending Email"
    send_from = fName
    send_to = tEmail
    message = eEncrypted
    subject = eHash
    msg = MIMEMultipart()
    msg.add_header('reply-to', fName)
    msg.add_header('encCode', 'testing')
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(server, port)
    server.starttls()
    server.login(uName, uPass)
    text = msg.as_string()
    server.sendmail(send_from, send_to, text)
    server.quit()
    print "Email Sent"
    raw_input("Press enter to continue.")
    os.system('cls')
    os.system('clear')
    

server = ''
port = ''

#Change these values VVVV
eSalt = "DeadDrop"
encKey = 'this is a temp encryption key000'
encValue = 'DigiDropAES12024'
#Change these values ^^^

uName = raw_input("Enter username: ")
uPass = raw_input("Enter Password: ")
os.system('cls')
os.system('clear')
print "(1) gmail"
print "(2) hotmail"
print "(3) yahoo"
print "(4) exchange"
print "(5) custom"
eEmail = raw_input("Select mail provider: ")
os.system('cls')
os.system('clear')
if eEmail == '1':
    server = 'smtp.gmail.com'
    port = 587
elif eEmail == '2':
    server = 'smtp.live.com'
    port = 587
elif eEmail == '3':
    server = 'smtp.mail.yahoo.com'
    port = 465
elif eEmail == '4':
    server = raw_input("Enter your SMTP server: ")
    port = int(raw_input("Enter the port number: "))
elif eEmail == '5':
    print 5


run = 0
while run == 0:
    print "Digital DeadDrop"
    print "(1) Retrieve Email"
    print "(2) Send Email"
    print "(3) Exit"
    eFunction = raw_input("Select Function: ")
    os.system('cls')
    os.system('clear')

    if eFunction == '1':
        eList = CheckEmail(uName, uPass, server, port)
        if eList == 0:
            print "No emails found"
        else:
            DecryptEmail(eList, encKey, eSalt, encValue)
    elif eFunction == '2':
        eText, tEmail = CreateEmail()
    
        eHash, eEncrypted, fName = EncryptEmail(eText, encKey, uName, eSalt, encValue)
        SendEmail(eHash, eEncrypted, fName, uName, uPass, server, port, tEmail)
    elif eFunction == '3':
        run = 1
                      
