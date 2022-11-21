
---
### Setting up Google OAuth credentials
---
For setting up Google Credentials You need to follow few steps:

## Step 1 : signup or signin
Create or login your google consol by visiting the[ Google API Console ](http://localhost:8000/admin/) to obtain OAuth 2.0 credentials such as a client ID and client secret that are known to both Google and your application.


## Step 2 : create credentials
1. First select the project on top right section in nav bar
2. Now click on credentials link available in left sidebar.
3.  After clicking on `Create credentials` a pop up will appear
4. In this pop up  select `OAuth client ID` option
- see the following image for reference
    ![alt text](https://drive.google.com/uc?export=view&id=1wACwTUtD_MbkA_dymi3F0xcjVNDJPM1T)


## Step 3 : configure
In this section you need to provide some inputs for creating `OAuth client ID`
1. select `web application` option form Application type drop down menu
2. on next input provide the application name.
3. now provide you url for `Authorized JavaScript origins`. keep separate url for productions and development environment. for example `http://localhost:8000`
4. after this you need to provide a `Authorized redirect URI` google will redirect user to this url after navigating user to auth page
5. Now click on create button and create your `OAuth client ID` would be created.
- see the following image for reference

    ![alt text](https://drive.google.com/uc?export=view&id=10XZIWrRRD8RyLOcVKYbQcHOqngIgJvMA)

## Step 4 : save details
After creating the OAuth ID another pop up will appear immediately.
copy and paste the client id and secret to a secure place. you can also download a json file which contains both id ans secret by clicking `DOWNLOAD JSON`link appear bottom left corner of pop up window

- see the following image for reference

    ![alt text](https://drive.google.com/uc?export=view&id=1oh-XAUEkPcwKwwXxMnHGHgzOpChZd7Wp)

## Step 5: manage credentials API settings
Now you have your `client ID` and `Secret`. its time to map these details into jaseci Configuration for this
- First login into your jaseci admin by visiting `http://localhost:8000/admin`
- Now in left sidebar click on `OAuth Credentials` link under `JASECI_SSO` section
- then click on `Add oauth credentials` button available on top right.

- see the following image for reference

    ![alt text](https://drive.google.com/uc?export=view&id=1eNsIrAXPkyfZHDItbeSdYVLQbeYqkFn8)


## Step 6: manage credentials API settings
After clicking `Add Oauth credentials` button you will land the page where you can add the credentials
1. first select the authentication provider type
2. paste your `client ID ` received from authenticate service provider.
3. paste your `client Secret` received from authenticate service provider.
4. select is active flag to yes, in case if you want to disable this configuration simply set this flag to false or No.
5. Now click on `save` button to save the configuration.
- see the following image for reference


    ![alt text](https://drive.google.com/uc?export=view&id=1kaw6H8bPi6jXBMrKLbnllJklXUHciv7u)

now you need to restart you jaseci server by running
`jsserv runserver`

for test the configuration navigate
[http://localhost:8000/auth/examples/google/](http://localhost:8000/auth/examples/google/)
