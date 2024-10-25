import rsa
# function that creates new keys 
# (only do if you want new keys for encryption/decryption) 
# [NOT DEBUGGED]

pub_name = input("Enter a name for public key PEM: ")
priv_name = input("Enter a name for private key PEM: ") 

def createKeys(public, private): 
    pub_key, priv_key = rsa.newkeys(1024)
    with open(pub_name + ".pem", "wb") as f:
        f.write(pub_key.save_pkcs1("PEM"))
    with open(priv_name + ".pem", "wb") as f:
        f.write(priv_key.save_pkcs1("PEM"))

    print("The new public and private keys have been created!")

createKeys(pub_name, priv_name)

# uses already-generated public key pub_name and private key priv_name
# keys are stored as pem files, don't need to be regenerated
with open(pub_name + ".pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
with open(priv_name + ".pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# takes a user input, and prints out the encrypted message using key "public"
message  = input("Enter a message to be encrypted: ")
encrypted_message = rsa.encrypt(message.encode(), public_key)
print(encrypted_message)

# saves encrypted message as seperate file (if not desired as direct output)
with open("encrypted.message", "wb") as f:
    f.write(encrypted_message)

# takes the encrypted (using "public") message and decrypts it using key "private"
decrypted_message = rsa.decrypt(encrypted_message, private_key)
print("The decoded message is: " + decrypted_message.decode())


