import requests
import credentials

targetServer = input("Target Server: ")
UserNum = int(input("Number of Users: "))

for i in range(UserNum):
    username = credentials.gen_username(i)
    password = credentials.gen_password(i)
    data = {
        "email": username,
        "password": password,
        "is_activated": True,
        "is_superuser": True,
    }
    URL = targetServer + "/user/create/"
    print(data)
    response = requests.post(URL, data=data)
    print(response.text)
