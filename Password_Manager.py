import rsa
from fernet import Fernet
import os

# personalized Password Manager that encrypts passwords using Fernet symmetric encryption, but uses RSA assymetric encryption to encrypt the file housing
# the symmetric encryption key (double encryption!)
# also adds a "waiting" period between each user choice, clear the console screen afterwards for better flow

class PasswordManager:
    def __init__(self):
        self.pubKey = None
        self.privKey = None
        self.symKey = None
        self.passwordFile = None
        self.passwordComp = {}

    def createRSAKeys(self, pubName, privName): # creates a pair of keys, public and private, for symmteric key encryption (1)
        pub_key, priv_key = rsa.newkeys(1024)
        with open(pubName + ".pem", "wb") as f:
            f.write(pub_key.save_pkcs1("PEM"))
        with open(privName + ".pem", "wb") as f:
            f.write(priv_key.save_pkcs1("PEM"))

        # loads the newly-created keys as current keys
        self.loadRSAKeys(pubName, privName)
        print("\nThe new public and private keys have been created!")

    def loadRSAKeys(self, pubName, privName): # loads RSA keys from (1) and (6)
        with open(pubName + ".pem", "rb") as f:
            self.pubKey = rsa.PublicKey.load_pkcs1(f.read())
        with open(privName + ".pem", "rb") as f:
            self.privKey = rsa.PrivateKey.load_pkcs1(f.read())

    def createSymKey(self, name): # creates a symmetric key for password encryption (2)
        self.symKey = Fernet.generate_key()
        encryptedSym = rsa.encrypt(self.symKey, self.pubKey)
        with open(name + ".key", "wb") as f:
            f.write(encryptedSym)
        
        print("\nThe new symmetric password encryption key has been created!")

    def loadSymKey(self, name): # loads symmetric key for (2) and (6)
        with open(name + ".key", "rb") as f:
            encryptedSym = f.read()
            self.symKey = rsa.decrypt(encryptedSym, self.privKey)

    def createPasswordFile(self, fileName): # creates an empty password file (3)
        self.passwordFile = fileName + ".message"
        with open(self.passwordFile, "w") as f:
            f.write("")

        print("\nThe new password list file has been created!")

    def loadPasswordFile(self, pubName, privName, keyName, fileName): # loads an existing password file (assumes it comes from a .message file) (6)
        self.passwordFile = fileName + ".message"
        self.loadRSAKeys(pubName, privName)
        self.loadSymKey(keyName)
        with open(self.passwordFile, 'r') as f:
            for line in f:
                websiteName, encrypted = line.split(":")
                self.passwordComp[websiteName] = Fernet(self.symKey).decrypt(encrypted.encode()).decode()
        
    def addPassword(self, websiteName, password): # adds a password in the currently selected password file (3)
        self.passwordComp[websiteName] = password
        if self.passwordFile is not None:
            with open(self.passwordFile, "a+") as f:
                encrypted = Fernet(self.symKey).encrypt(password.encode())
                f.write(websiteName + ":" + encrypted.decode() + "\n")
            print("\nThe password has been added to the file!")
        else:
            print("Sorry, you do not have a selected file to add a password in!")

    def getPassword(self, websiteName): # returns a password from the currently selected password file (4)
        if self.passwordFile is not None:
            with open(self.passwordFile, 'r'):
                password = self.passwordComp[websiteName]
                print("The password to " + websiteName + " is: " + password)
        else:
            print("Sorry, you do not have a selected file to return a password from!")



# in-console interactive for Password Manager
def main():
    pm = PasswordManager()
    
    done = False
    while not done:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("------PASSWORD MANAGER------")
        if(pm.passwordFile == None):
            print("Currently selected password file: None")
        else:
            print("Currently selected password file: " + pm.passwordFile)

        print("""Please select an option:
          (1) Create new RSA keys 
          (2) Create symmetric key
          (3) Create new password file
          (4) Add a password to an existing password file
          (5) Get a password from an existing password file
          (6) Load an existing password file
          (q) Quit Password Manager
            """)
        option = input("Your choice: ")

        if(option == "1"):
            pubKey = input("Enter a name for public RSA key: ")
            privKey = input("Enter a name for private RSA key: ")
            pm.createRSAKeys(pubKey, privKey)
            input("\nPress enter to continue...")

        elif(option == "2"):
            symKey = input("Enter a name for password encryption key: ")
            pm.createSymKey(symKey)
            input("\nPress enter to continue...")

        elif(option == "3"):
            passFile = input("Enter a name for the new password list: ")
            pm.createPasswordFile(passFile)
            input("\nPress enter to continue...")

        elif(option == "4"):
            website = input("Enter the name of the application you want to record the password for: ")
            password = input("Enter the password for the application: ")
            pm.addPassword(website, password)
            input("\nPress enter to continue...")

        elif(option == "5"):
            website = input("Enter the name of the application you need the password for: ")
            pm.getPassword(website)
            input("\nPress enter to continue...")

        # assumes that user knows what file(s) correspond w/ public, private, and symmertic keys
        elif(option == "6"):
            passFile = input("Enter the name of the file you wish to load: ")
            pubKey = input("Enter the name of the file containing the associatied public key: ")
            privKey = input("Enter the name of the file containing the associatied private key: ")
            symKey = input("Enter the name of the file containing the associatied password encryption key: ")
            pm.loadPasswordFile(pubKey, privKey, symKey, passFile)
            input("\nPress enter to continue...")

        elif(option == 'q'):
            done = True
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Thank you for using Password Manager!")

        else:
            print("Sorry! That was an invalid choice, please make another selection.")
            input("\nPress enter to continue...")


if __name__ == "__main__":
    main()