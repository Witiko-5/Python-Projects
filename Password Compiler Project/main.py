def view():
    with open("passwords.txt","r") as f:
        for line in f.readlines():
            data = line.rstrip()
            website, user, password = data.split("|")
            print("Website:", website, "| User:", user, "| Password:", password)

def add():
    web_name = input("Website: ")
    name = input("Account Name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(web_name + "|" + name + "|" + pwd + "\n")

while True:
    mode = input("Would you like to add a new password or view existing one or press Q to quit? (view, add, Q) ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue