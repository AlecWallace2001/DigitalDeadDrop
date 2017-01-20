# DigitalDeadDrop
This will allow anyone to create secured e-mails with burner accounts. More updates coming


Best implementation reccomended:

  Place script on an encrypted USB file. (I will work on creating a device agnostic executable)
  
  Change the following variables to your desired values:
  
    eSalt (The longer and more random, the better)
    
    encKey (Value must be 16, 24, or 32 characters long)
    
    encValue (Value needs to be 16 characters long)
    
  Image the USB and create a duplicate.
  
  Provide the duplicate to the person you are going to be communicating with.
  
  
  
To use the Dead Drop:

  1.) Launch DigiDrop.py
  
  2.) Enter the login name/Email address for the account you will be using
  
  3.) Enter the password 
  
  4.) Select your mail client.
  
    If it is not shown and you have the SMTP server and port, select 'exchange'
    
  5.) Select Retrieve or Send Email
  
  
  
Sending Email

  1.) Select #2 Send Email
  
  2.) Enter the e-mail address you will be sending your communication to, then press enter
  
  3.) Enter your message, then press enter.
  
    You can only write in one paragraph block. As soon as you press enter, it will send your email.
    
    You will not be entering a subject in the email as that is reserved for the hash to verify that the message recieved has not been tampered in transit.
    
    
    
Retrieving Email

  DigitalDeadDrop will pull the 100 most recent emails you recieved. It will look for a specific value that has been added to the header of the email. Once the email(s) has been found, it will read the hash value and the email text. It will attempt to decrypt the text and compare the hash from the decrypted text to the hash in the subject line. If the hashes match, the program will let you know that it considers the message to be trustworthy. Trustworthy in this case means that the message was sent from a corresponding drive with the appropriate keys.
  
  If more than one email was found, they will be stored in a list in memory. It will not be written to disc or saved on the USB. When I create an initialization script, I will include options to save to a .txt file as well as delete(or mark for deletion) the email on the server.
  
  
  Retrieved Email Format:
  
  Validity indication
  
  Message Encrypted
  
  Message Decrypted
  
  
  
  Subject Hash
  
  Decrypted Message Hash
  
  
  Pressing enter after reading the message will scroll you through the emails.

Close the program (not minimize) when finished and remove the drive. Only mount the encrypted drive when you are going to use the DigitalDeadDrop.
