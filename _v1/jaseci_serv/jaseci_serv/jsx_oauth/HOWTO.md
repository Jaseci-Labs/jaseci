# **SAMPLE SOCIAL APP CREATION**

- Add `Social App` for GitHub in Admin Panel
![Add GitHub on SocialApp](https://user-images.githubusercontent.com/74129725/234258273-05fbaa39-f113-464e-8100-5004c2192692.png)
- Sample `Social App` listing in Admin Panel
![Add GitHub on SocialApp](https://user-images.githubusercontent.com/74129725/234258565-4324a4a0-6fbc-43a3-96cc-7365c512976a.png)
- Add GlobalVars for `GITHUB_REDIRECT_URI`
![GITHUB_REDIRECT_URI](https://user-images.githubusercontent.com/74129725/209336232-67c6918c-da37-4632-96cb-551b76f267ca.png)

---

# **GETTING TOKEN**

## **via `AUTHORIZATION CODE`**
> **`METHOD`**: \
> POST
>
> **`URL`**: \
> /auth/`{{provider}}` => **ex**: /auth/`google`


##### **`REQUEST BODY`**:
```js
{
    code: "{{authorization code}}",

    // optional: used if FE wants to redirect it to different url
    callback_url: redirect_uri
}
```
---
## **via `ID TOKEN`**
> **`METHOD`**: \
> POST
>
> **`URL`**: \
> /auth/`{{provider}}` => **ex**: /auth/`google`


##### **`REQUEST BODY`**:
```js
{
    id_token: "{{id_token}}",

    // optional:
    access_token: "{{access token if present}}"
}
```
---
## **via `ACCESS TOKEN`**
> **`METHOD`**: \
> POST
>
> **`URL`**: \
> /auth/`{{provider}}` => **ex**: /auth/`google`


##### **`REQUEST BODY`**:
```js
{
    access_token: "{{access token if present}}"
}
```
# **SUPPORTED PROVIDER**
---

## **`GOOGLE`**
![google-sign-in](https://user-images.githubusercontent.com/74129725/234259948-db3d3fab-bc0b-497b-a7f4-e8264b28baa0.png)
- [Google Documentation](https://developers.google.com/identity/protocols/oauth2/web-server#python) for Authorizing OAuth Apps
- [Add SocialApp](./HOWTO.md) for Google
- Use the sample code from Google docs for getting Authorization code
```js
<button onclick="client.requestCode();">Login with Google</button>

<script src="all required scripts from docs"></script>
<script>
    const client = google.accounts.oauth2.initCodeClient({
        client_id: "{{client_id}}",
        scope: "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
        ux_mode: 'redirect',
        redirect_uri: "http://localhost:8001/auth/examples/" + provider + "/",
        state: "offline"
    });
</script>
```
- Upon successful login authorization code should now be present on URL and can be used on [getting Access Token](./HOWTO.md)
- Try it on your local using `/auth/examples/google/`

---
## **`GITHUB`**
![github-sign-in](https://user-images.githubusercontent.com/74129725/234259914-10b845a7-e148-4371-b6ec-b8b16da4e8ed.png)
- [GitHub Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps) for Authorizing OAuth Apps
- [Add SocialApp](./HOWTO.md) for GitHub
- you need to redirect to this URL format
> https://github.com/login/oauth/authorize?client_id=`{{your GitHub OAuth App's client ID}}`&redirect_uri=`{{your GitHub OAuth App's allowed callback URI set in GitHub OAuth App}}`&scope=read:user,user:email&state=`{{your any random str}}`
- Upon successful login authorization code should now be present on URL and can be used on [getting Access Token](./HOWTO.md)
- Try it on your local using `/auth/examples/github/`

---
## **`FACEBOOK`**
![facebook-sign-in](https://user-images.githubusercontent.com/74129725/234259980-b931d8db-2c93-4446-9fc4-a49b5d6448ba.png)
- [Facebook Documentation](https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow#checklogin) for Authorizing OAuth Apps
- [Add SocialApp](./HOWTO.md) for Facebook
- you need to redirect to this URL format
> https://www.facebook.com/dialog/oauth/?client_id=`{{your Facebook OAuth App's client ID}}`&redirect_uri=`{{your Facebook OAuth App's allowed callback URI set in Facebook OAuth App}}`&scope=email&state=`{{your any random str}}`
- Upon successful login authorization code should now be present on URL and can be used on [getting Access Token](./HOWTO.md)
- Try it on your local using `/auth/examples/facebook/`

---
## **`APPLE`**
![apple-sign-in](https://user-images.githubusercontent.com/74129725/234259881-bf98be3e-4c26-4103-97c0-c7f113e9c454.png)
- [Documentation](https://developer.apple.com/documentation/sign_in_with_apple/sign_in_with_apple_js) for Apple Sign-in Integration
- [Add SocialApp](./HOWTO.md) for Apple
    - apple have different required [fields](https://django-allauth.readthedocs.io/en/latest/providers.html#apple)
- setup your web based on apple [docs](https://developer.apple.com/documentation/sign_in_with_apple/sign_in_with_apple_js/configuring_your_webpage_for_sign_in_with_apple)
- Try it on your local using `/auth/examples/apple/`

---
# **MULTIPLE SAME PROVIDER INTEGRATION**
- if admin want's to integrate multiple google provider with different client id, admin is required to use `Social App's ID`.
![App Listing](https://user-images.githubusercontent.com/74129725/234258565-4324a4a0-6fbc-43a3-96cc-7365c512976a.png)
- `Social App's ID` should be included on request as **`app_id`**.
- if app_id is not specified and you have multiple google provider, error will return
> ```js
>{
>   "non_field_errors": [
>       "You have multiple google Social App. app_id is required to associated it on one of those apps!"
>   ]
>}
>```
## **`HOW TO USE`**
#### **via `AUTHORIZATION CODE`**
```js
{
    app_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
    code: "{{authorization code}}",

    // optional: used if FE wants to redirect it to different url
    callback_url: redirect_uri
}
```
---
#### **via `ID TOKEN`**
```js
{
    app_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
    id_token: "{{id_token}}",

    // optional:
    access_token: "{{access token if present}}"
}
```
---
#### **via `ACCESS TOKEN`**:
```js
{
    app_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
    access_token: "{{access token if present}}"
}
```


---
# **FEATURE**
- Allowed to bind multiple provider to a single account
    - response will have "type" and "details" field for FE handling
        - `REGISTRATION`: New account
        - `EXISTING`: Existing account
        - `ACTIVATION`: Existing account but just got activated
        - `BINDING`: Existing account but just got binded with different login type

---