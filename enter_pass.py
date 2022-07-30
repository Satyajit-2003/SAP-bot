import pickle

username = input("Enter username: ")
password = input("Enter password: ")

dc = [username, password]
pickle.dump(dc, open("pass.pkl", "wb"))