import rsa

public_key, private_key = rsa.newkeys(1024)
print(private_key)

# make a file public.pem and private.pem that saves the public/private key respectively
    #with open("public.pem", "wb") as f:
    #    f.write(public_key.save_pkcs1("PEM"))

    #with open("private.pem", "wb") as f:
    #    f.write(private_key.save_pkcs1("PEM")) """
# ^^ already made private.pem and public.pem files, we go down to reading them now vv:

with open("public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("private.pem", "rb") as f:
     private_key = rsa.PrivateKey.load_pkcs1(f.read())

# encrypt message "Hello sheCodes" 
message = "Hello sheCodes"
encrypted_message = rsa.encrypt(message.encode(), public_key)
print(encrypted_message)

# make file encrypted.message that writes out the encrypted message
with open("encrypted.message", "wb") as f:
     f.write(encrypted_message)

# make file read from encrypted.message write out decrypted message
encrypted_message = open("encrypted.message", "rb").read()
clear_message = rsa.decrypt(encrypted_message, private_key)
print(clear_message)

# print message without b (bytes) at start
print(clear_message.decode())

# sign the message to verify that the correct private key is the sender
message2 = "This is for private encryption practice"
signature = rsa.sign(message2.encode(), private_key, "SHA-256")

# make a file named signature with our encoded message2
with open("signature", "wb") as f:
     f.write(signature)
    
# verify signature
with open("signature", "rb") as f:
     isSignature = f.read()
    
# should print SHA-56 to verify that the message is authentic
print(rsa.verify(message2.encode(), isSignature, public_key))

