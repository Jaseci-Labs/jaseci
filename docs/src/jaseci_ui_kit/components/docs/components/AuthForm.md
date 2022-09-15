#### Summary

Quickly add user login and sign up to your jaseci site

<u>Example:</u>

```JSON
{
      "component": "AuthForm",
      "props": {
        "mode": "login",
        "serverURL": "http://localhost:8000",
        "tokenKey": "tokenKey",
        "hideNameField": true
      }
}
```

### Props

| name          | type                | description                                                |
| ------------- | ------------------- | ---------------------------------------------------------- |
| mode          | "login" or "signup" | Determines which form to display                           |
| serverURL     | string              | Jaseci Server URL                                          |
| tokenKey      | tokenKey            | Location used to store the token in localstorage           |
| hideNameField | boolean             | Opt-in/out of collecting the user's name when they sign up |
