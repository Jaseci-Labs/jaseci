"""Google SSO."""

from typing import Any, Dict, Literal

from fastapi import HTTPException, Request

from fastapi_sso.sso.base import OpenID
from fastapi_sso.sso.google import GoogleSSO as _GoogleSSO

from google.auth.jwt import decode

from httpx import get


class GoogleSSO(_GoogleSSO):
    """Class providing login via Google Android OAuth."""

    id_token_issuer = "https://accounts.google.com"
    oauth_cert_url = "https://www.googleapis.com/oauth2/v1/certs"

    async def verify_and_process(  # type: ignore[override]
        self,
        request: Request,
        *,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
        redirect_uri: str | None = None,
        convert_response: Literal[True] | Literal[False] = True,
    ) -> OpenID | Dict[str, Any] | None:
        """Verify and process Apple SSO."""
        if id_token := request.query_params.get("id_token"):
            return await self.get_open_id(id_token)
        return await super().verify_and_process(
            request,
            params=params,
            headers=headers,
            redirect_uri=redirect_uri,
            convert_response=convert_response,
        )

    async def get_open_id(self, id_token: str) -> OpenID:
        """Get OpenID from id_tokens provided by Apple."""
        raw: dict = decode(
            id_token, certs=get(self.oauth_cert_url).json(), audience=self.client_id
        )

        if raw.get("email_verified") is not True:
            raise HTTPException(403, "You're trying to attach a non verified account!")

        return OpenID(
            id=raw.get("sub"),
            email=raw.get("email"),
            first_name=raw.get("given_name"),
            last_name=raw.get("family_name"),
        )
