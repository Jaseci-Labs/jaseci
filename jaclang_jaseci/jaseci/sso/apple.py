"""Apple SSO."""

from json import dumps
from typing import Any, ClassVar, Dict, Literal, Optional, Union, cast
from warnings import warn

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from fastapi import HTTPException, Request

from fastapi_sso.sso.base import (
    DiscoveryDocument,
    OpenID,
    ReusedOauthClientWarning,
    SSOBase,
)

from httpx import AsyncClient, BasicAuth

from jwt import algorithms, decode, get_unverified_header


class AppleSSO(SSOBase):
    """Class providing login via Apple OAuth."""

    provider = "apple"
    base_url = "https://appleid.apple.com/auth"
    scope: ClassVar = ["name", "email"]

    async def get_discovery_document(self) -> DiscoveryDocument:
        """Get document containing handy urls."""
        return {
            "authorization_endpoint": f"{self.base_url}/authorize",
            "token_endpoint": f"{self.base_url}/oauth2/v2/token",
            "userinfo_endpoint": f"{self.base_url}/me?fields=id,name,email,first_name,last_name,picture",
        }

    async def get_public_key(
        self, id_token: str
    ) -> RSAPrivateKey | RSAPublicKey | None:
        """Get the public key which matches the `kid` in the id_token header."""
        kid = get_unverified_header(id_token)["kid"]
        async with AsyncClient() as session:
            response = await session.get(f"{self.base_url}/keys")
            for key in response.json()["keys"]:
                if key["kid"] == kid:
                    return algorithms.RSAAlgorithm.from_jwk(dumps(key))
        return None

    async def verify_and_process(  # type: ignore[override]
        self,
        request: Request,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        redirect_uri: Optional[str] = None,
        convert_response: Union[Literal[True], Literal[False]] = True,
    ) -> Union[Optional[OpenID], Optional[Dict[str, Any]]]:
        """Verify and process Apple SSO."""
        if params and (id_token := request.query_params.get("id_token")):
            return await self.get_open_id(id_token)
        return await super().verify_and_process(
            request,
            params=params,
            headers=headers,
            redirect_uri=redirect_uri,
            convert_response=convert_response,
        )

    async def process_login(  # type: ignore[override]
        self,
        code: str,
        request: Request,
        *,
        params: Optional[Dict[str, Any]] = None,
        additional_headers: Optional[Dict[str, Any]] = None,
        redirect_uri: Optional[str] = None,
        pkce_code_verifier: Optional[str] = None,
        convert_response: Union[Literal[True], Literal[False]] = True,
    ) -> Union[Optional[OpenID], Optional[Dict[str, Any]]]:
        """Process login for Apple SSO."""
        if self._oauth_client is not None:  # type: ignore[has-type]
            self._oauth_client = None
            self._refresh_token = None
            self._id_token = None
            warn(
                (
                    "Reusing the SSO object is not safe and caused a security issue in previous versions."
                    "To make sure you don't see this warning, please use the SSO object as a context manager."
                ),
                ReusedOauthClientWarning,
            )
        params = params or {}
        params.update(self._extra_query_params)
        additional_headers = additional_headers or {}
        additional_headers.update(self.additional_headers or {})

        url = request.url

        if not self.allow_insecure_http and url.scheme != "https":
            current_url = str(url).replace("http://", "https://")
        else:
            current_url = str(url)

        current_path = f"{url.scheme}://{url.netloc}{url.path}"

        if pkce_code_verifier:
            params.update({"code_verifier": pkce_code_verifier})

        params.update({"client_secret": self.client_secret})

        token_url, headers, body = self.oauth_client.prepare_token_request(
            await self.token_endpoint,
            authorization_response=current_url,
            redirect_url=redirect_uri or self.redirect_uri or current_path,
            code=code,
            **params,
        )  # type: ignore

        if token_url is None:  # pragma: no cover
            return None

        headers.update(additional_headers)

        auth = BasicAuth(self.client_id, self.client_secret)

        async with AsyncClient() as session:
            response = await session.post(
                token_url, headers=headers, content=body, auth=auth
            )
            content: dict = response.json()
            self._refresh_token = content.get("refresh_token")
            if id_token := content.get("id_token"):
                self._id_token = id_token
                return await self.get_open_id(id_token)
            raise HTTPException(401, "Failed to get access token!")

    async def get_open_id(self, id_token: str) -> OpenID:
        """Get OpenID from id_tokens provided by Apple."""
        identity_data: dict = decode(
            id_token,
            cast(RSAPublicKey, await self.get_public_key(id_token)),
            algorithms=["RS256"],
            audience=self.client_id,
            issuer="https://appleid.apple.com",
        )

        return OpenID(id=identity_data.get("sub"), email=identity_data.get("email"))
