from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        print(f"New key created and saved to {path}.")

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
        print(f"Key loaded from {path}.")

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for key, value in initial_values.items(): 
                self.add_password(key, value)
        print(f"Password file created at {path}.")

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.strip().split(" : ")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        print(f"Password file loaded from {path}.")

    def add_password(self, site, password): 
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + " : " + encrypted.decode() + "\n")
        print(f"Password for {site} added successfully.")

    def get_password(self, site):
        return self.password_dict.get(site, "[X] No password found for this site.")
    
    def display_all_passwords(self):
        if not self.password_dict:
            print("[X] No stored passwords found.")
        else:
            print("\nStored Passwords:")
            for site, password in self.password_dict.items():
                print(f"{site}: {password}")

def main():
    initial_passwords = {
        "Email": "1234567",
        "Facebook": "myfbpassword",
        "Youtube": "helloworld123",
        "Instagram": "myfavoritepassword_123"
    }

    pm = PasswordManager()

    print("Welcome to the Password Manager!")

    print("""What would you like to do?
    (1) Create a new encryption key
    (2) Load an existing encryption key
    (3) Create a new password file
    (4) Load an existing password file
    (5) Add a new password
    (6) Retrieve a password
    (7) Display all stored passwords
    (q) Quit
    """)

    done = False

    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter the path to save your new key file: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter the path to your key file: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter the location to save your new password file: ")
            pm.create_password_file(path, initial_passwords)
        elif choice == "4":
            path = input("Specify the path to your existing password file: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site name: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("Enter the site name to retrieve its password: ")
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == "7":
            pm.display_all_passwords()
        elif choice == "q":
            done = True
            print("Thank you for using the Password Manager! Goodbye!")
        else:
            print("Invalid choice! Please select a valid option from the menu.") 

if __name__ == "__main__":
    main()