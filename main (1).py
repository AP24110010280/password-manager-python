import string
import random
from cryptography.fernet import Fernet



MASTER_PASSWORD = "admin123"

def login():
    print("---- PASSWORD MANAGER LOGIN ----")

    password = input("Enter master password: ")

    if password == MASTER_PASSWORD:
        print("Login Successful!\n")
        return True
    else:
        print("Wrong password!")
        return False


def check_strength(password):

    strength = 0

    if len(password) >= 8:
        strength += 1

    if any(char.isdigit() for char in password):
        strength += 1

    if any(char.isupper() for char in password):
        strength += 1

    if any(char in string.punctuation for char in password):
        strength += 1

    if strength <= 1:
        return "Weak Password"

    elif strength <= 3:
        return "Medium Password"

    else:
        return "Strong Password"



def generate_password(length=12):

    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))

    return password



def load_key():

    try:
        with open("key.key", "rb") as file:
            key = file.read()

    except FileNotFoundError:

        key = Fernet.generate_key()

        with open("key.key", "wb") as file:
            file.write(key)

    return key


key = load_key()
cipher = Fernet(key)


def encrypt_password(password):

    encrypted = cipher.encrypt(password.encode())

    return encrypted.decode()


def decrypt_password(encrypted_password):

    decrypted = cipher.decrypt(encrypted_password.encode())

    return decrypted.decode()



def save_password(site, username, password):

    encrypted = encrypt_password(password)

    with open("passwords.txt", "a") as file:

        file.write(f"{site},{username},{encrypted}\n")

    print("Password saved successfully!")



def view_passwords():

    try:

        with open("passwords.txt", "r") as file:

            for line in file:

                try:
                    site, username, encrypted = line.strip().split(",")

                    password = decrypt_password(encrypted)

                    print("\nSite:", site)
                    print("Username:", username)
                    print("Password:", password)
                    print("-----------------------")

                except:
                    print("Skipped invalid entry")

    except FileNotFoundError:

        print("No passwords saved yet.")



if login():

    print("Welcome to Password Manager")

    while True:

        print("\n1. Save Password")
        print("2. View Passwords")
        print("3. Generate Password")
        print("4. Check Password Strength")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":

            site = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")

            print("Password Strength:", check_strength(password))

            save_password(site, username, password)

        elif choice == "2":

            view_passwords()

        elif choice == "3":

            print("Generated Password:", generate_password())

        elif choice == "4":

            pwd = input("Enter password to check strength: ")

            print("Password Strength:", check_strength(pwd))

        elif choice == "5":

            print("Exiting program...")

            break

        else:

            print("Invalid option")