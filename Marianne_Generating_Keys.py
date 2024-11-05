import rsa

with open("public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


message = "I have a new account on Twitter which is @watermelon"


with open ("signature", "rb") as f:
    signature = f.read()

print(rsa.verify(message.encode(), signature, public_key))