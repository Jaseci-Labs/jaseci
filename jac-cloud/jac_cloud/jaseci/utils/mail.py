"""Mail Handler."""

from os import getenv
from typing import cast

from sendgrid import SendGridAPIClient


class Emailer:
    """Email Handler."""

    __client__: object | None = None

    @classmethod
    def start(cls) -> None:
        """Initialize email client."""
        if not cls.get_client():
            raise Exception("Error generating email client!.")

    @staticmethod
    def has_client() -> bool:
        """Check if has client."""
        return bool(Emailer.__client__)

    @classmethod
    def generate_client(cls) -> object | None:
        """Generate client."""
        pass

    @classmethod
    def get_client(cls) -> object | None:
        """Retrieve client."""
        if Emailer.__client__:
            return Emailer.__client__
        Emailer.__client__ = cls.generate_client()
        return Emailer.__client__

    @classmethod
    def send_email(
        cls,
        subject: str,
        recipients: list[dict],
        content: list[dict],
        sender: str = "no-reply@jac-lang.org",
    ) -> None:
        """Send Email."""
        raise Exception("send_email not implemented yet.")

    @classmethod
    def send_verification_code(cls, code: str, email: str) -> None:
        """Send Verification Code."""
        raise Exception("send_verification_code not implemented yet.")

    @classmethod
    def send_reset_code(cls, code: str, email: str) -> None:
        """Send Verification Code."""
        raise Exception("send_reset_code not implemented yet.")


class SendGridEmailer(Emailer):
    """SendGrid Handler."""

    __host__: str = getenv("SENDGRID_HOST") or "http://localhost:8000"

    @classmethod
    def generate_client(cls) -> SendGridAPIClient | None:
        """Generate client."""
        if sendgrid_api_key := getenv("SENDGRID_API_KEY"):
            return SendGridAPIClient(api_key=sendgrid_api_key)
        return None

    @classmethod
    def send_email(
        cls,
        subject: str,
        recipients: list[dict],
        content: list[dict],
        sender: str = "no-reply@jac-lang.org",
    ) -> None:
        """Send Email."""
        if client := cast(SendGridAPIClient, cls.get_client()):
            client.client.mail.send.post(
                request_body={
                    "personalizations": [{"to": recipients, "subject": subject}],
                    "from": {"email": sender},
                    "content": content,
                }
            )

    @classmethod
    def send_verification_code(cls, code: str, email: str) -> None:
        """Send Verification Code."""
        url = f"{cls.__host__}/verify?code={code}"
        cls.send_email(
            subject="Account Verification",
            recipients=[{"email": email}],
            content=[
                {
                    "type": "text/plain",
                    "value": f"{code}\n\n{url}",
                },
                {
                    "type": "text/html",
                    "value": f'{code}<br><a href="{url}">Verify</a>',
                },
            ],
        )

    @classmethod
    def send_reset_code(cls, code: str, email: str) -> None:
        """Send Reset Code."""
        url = f"{cls.__host__}/reset_password?code={code}"
        cls.send_email(
            subject="Password Reset",
            recipients=[{"email": email}],
            content=[
                {
                    "type": "text/plain",
                    "value": f"{code}\n\n{url}",
                },
                {
                    "type": "text/html",
                    "value": f'{code}<br><a href="{url}">Reset Password</a>',
                },
            ],
        )
