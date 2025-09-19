import hashlib
import self


class User:
    def __init__(self, first_name, last_name, email, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.gender = gender

    def signup(self):
        email = input("Enter email address: ")
        password = input("Enter password: ")
        conf_password = input("Confirm password: ")

        if conf_password == password:
            encode = conf_password.encode()
            hash1 = hashlib.md5(encode).hexdigest()
            with open("credentials.txt", "w") as f:
                f.write(email + "\n")
                f.write(hash1)
                f.close()
                print("You have registered successfully!")
        else:
            print("Password is not same as above! \n")

    def login(self):
        email = input("Enter email address: ")
        password = input("Enter password: ")

        auth = password.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        with open("credentials.txt", "r") as f:
            stored_email, stored_pwd = f.read().split("\n")
        f.close()

        if email == stored_email and auth_hash == stored_pwd:
            print("Logged in Successfully!")
        else:
            print("Login failed! \n")

    while 1:
        print("********** Login System **********")
        print("1.Signup")
        print("2.Login")
        print("3.Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            signup(self)
        elif ch == 2:
            login(self)
        elif ch == 3:
            break
        else:
            print("Wrong Choice!")