# **`GITHUB`**

- [GitHub Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps) for Authorizing OAuth Apps
- Add Social App for GitHub in Admin Panel
![Add GitHub on SocialApp](https://user-images.githubusercontent.com/74129725/209335723-283fc800-78bd-47af-82e5-895720d8f382.png)
- Add GlobalVars for `GITHUB_REDIRECT_URI`
![GITHUB_REDIRECT_URI](https://user-images.githubusercontent.com/74129725/209336232-67c6918c-da37-4632-96cb-551b76f267ca.png)
- you need to redirect to this URL format
>https://github.com/login/oauth/authorize?client_id=`{{your GitHub OAuth App's client ID}}`&redirect_uri=`{{your GitHub OAuth App's allowed callback URI set in GitHub OAuth App}}`&scope=read:user,user:email&state=`{{your any random str}}`
- Try it on your local using `/auth/examples/github/`