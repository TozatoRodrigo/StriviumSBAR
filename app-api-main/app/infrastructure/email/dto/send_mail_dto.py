from pydantic import BaseModel, Field


class SendMailDTO(BaseModel):
    destination: str = Field(description="Email address to send to")
    subject: str = Field(description="Email subject")
    body: str | None = Field(default=None, description="Email body content (text)")
    html_body: str | None = Field(
        default=None, description="HTML version of the email body"
    )
    cc: list[str] | None = Field(default=None, description="CC recipients")
    bcc: list[str] | None = Field(default=None, description="BCC recipients")


class SendMultipleMailDTO(BaseModel):
    destinations: list[str] = Field(description="List of email addresses to send to")
    subject: str = Field(description="Email subject")
    body: str | None = Field(default=None, description="Email body content (text)")
    html_body: str | None = Field(
        default=None, description="HTML version of the email body"
    )
    cc: list[str] | None = Field(default=None, description="CC recipients")
    bcc: list[str] | None = Field(default=None, description="BCC recipients")
