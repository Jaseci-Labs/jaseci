# **SAMPLE SOCIAL APP CREATION**

- Add `Social App` for GitHub in Admin Panel
![Add GitHub on SocialApp](https://user-images.githubusercontent.com/74129725/229818863-61fc7ec9-3f95-44a6-86fc-086aef37e92c.png)
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

- [GitHub Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps) for Authorizing OAuth Apps
- [Add SocialApp](./HOWTO.md) for GitHub
- you need to redirect to this URL format
> https://github.com/login/oauth/authorize?client_id=`{{your GitHub OAuth App's client ID}}`&redirect_uri=`{{your GitHub OAuth App's allowed callback URI set in GitHub OAuth App}}`&scope=read:user,user:email&state=`{{your any random str}}`
- Upon successful login authorization code should now be present on URL and can be used on [getting Access Token](./HOWTO.md)
- Try it on your local using `/auth/examples/github/`

---
## **`FACEBOOK`**

- [Facebook Documentation](https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow#checklogin) for Authorizing OAuth Apps
- [Add SocialApp](./HOWTO.md) for Facebook
- you need to redirect to this URL format
> https://www.facebook.com/dialog/oauth/?client_id=`{{your Facebook OAuth App's client ID}}`&redirect_uri=`{{your Facebook OAuth App's allowed callback URI set in Facebook OAuth App}}`&scope=email&state=`{{your any random str}}`
- Upon successful login authorization code should now be present on URL and can be used on [getting Access Token](./HOWTO.md)
- Try it on your local using `/auth/examples/facebook/`
---
# **MULTIPLE SAME PROVIDER INTEGRATION** (`Internal Clients`)
- if admin want's to integrate multiple google provider with different client id, admin is required to add `Internal Clients`.
- Internal client will be associated to specific `Social App`
![Internal Client](https://user-images.githubusercontent.com/74129725/229818863-61fc7ec9-3f95-44a6-86fc-086aef37e92c.png)
![Internal Client](https://user-images.githubusercontent.com/74129725/229823328-9edbe3f1-cb76-469e-a54d-4804c0a8dd94.png)
- if internal clients is not specified and multiple same provider is present it will post some error.
```js
{
    "non_field_errors": [
        "You have multiple google Social App. internal_client_id is required to associated it on one of those apps!"
    ]
}
```
## **`HOW TO USE`**
#### **via `AUTHORIZATION CODE`**
```js
{
    internal_client_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
    code: "{{authorization code}}",

    // optional: used if FE wants to redirect it to different url
    callback_url: redirect_uri
}
```
---
#### **via `ID TOKEN`**
```js
{
    internal_client_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
    id_token: "{{id_token}}",

    // optional:
    access_token: "{{access token if present}}"
}
```
---
#### **via `ACCESS TOKEN`**:
```js
{
    internal_client_id: "09eea429-545d-4aa9-b36f-66081a1472bc",
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