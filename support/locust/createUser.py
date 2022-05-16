import requests
import utils

targetServer = input("Target Server: ")
UserNum = int(input("Number of Users: "))

# Create all the users
for i in range(UserNum):
    username = utils.gen_username(i)
    password = utils.gen_password(i)
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

