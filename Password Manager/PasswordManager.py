from cryptography.fernet import Fernet

class PasswordManager:
    
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(self.key)

# creates file mykey.key
    # pm = PasswordManager()
    #pm.create_key("mykey.key")

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                # TODO: add password function
                self.add_password(key, value)
        
    def load_password_file(self,path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
        else:
            print("No password file loaded! Did you forget to load one?")

    def get_password(self, site):
        return self.password_dict[site]
    
    def get_sites(self):
        if self.password_file is not None:
            with open(self.password_file, 'r') as f:
                for line in f:
                    site, _ = line.split(":")
                    print(f"{site}")
        else:
            print("No password file loaded! Did you forget to load one?")


def main():
    password = {
        "email":"12345",
        "sheCodes":"2024",
        "broncoID":"0000",
        "youtube":"text"
    }

    pm = PasswordManager()
    print("""
            -----------------------------------
                What do you want to do?:
            (1) I don't have passwords saved...
            (2) I have passwords saved...
            ------------------------------------\n
        """)
    done = False
    choice = input("Enter your choice: ")

    if choice == "1":
        while (done is not True):
            print("""\n
                    ------------------------------------
                        What do you want to do?:
                    (1) Create a new key
                    (2) Create new password file
                    (q) Quit
                    ------------------------------------
                """)
            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                path = input("Enter name of file: ")
                pm.create_key(path)
                    
            elif choice2 == "2":
                path = input("Enter name of file: ")
                pm.create_password_file(path, password)
            
            elif choice2 == "q":
                done = True
                print("Exiting...")

            else:
                print("Not valid input.")

    elif choice == "2":
        while (done is not True):
            print("""\n
                    ------------------------------------
                        What do you want to do?
                    (1) Load an existing key 
                    (2) Load existing password file
                    (3) List sites with passwords
                    (4) Add a new password
                    (5) Retrieve a password
                    (q) Quit
                    ------------------------------------
                """)

            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                path = input("Enter name of file: ")
                pm.load_key(path)

            elif choice2 == "2":
                path = input("Enter name of file: ")
                pm.load_password_file(path)
            
            elif choice2 == "3":
                print("You have passwords for:")
                pm.get_sites()

            elif choice2 == "4":
                site = input("Enter the site: ")
                password = input("Enter the password: ")
                pm.add_password(site, password)
                    
            elif choice2 == "5":
                site = input("What site do you want?: ")
                print(f"Password for {site} is {pm.get_password(site)}")

            elif choice2 == "q":
                done = True
                print("Exiting...")
            
            else:
                print("Not valid input.")
    else:
        print("Invalid choice!")
        return

if __name__ == "__main__":
    main()