from typing import ClassVar

import pytest

from app.core.environment import envs
from app.infrastructure.email import send_mail as send_mail_module
from app.infrastructure.email.dto.send_mail_dto import SendMailDTO, SendMultipleMailDTO
from app.infrastructure.email.send_mail import SendMail


class SMTPStub:
    instances: ClassVar[list["SMTPStub"]] = []

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.starttls_calls = 0
        self.login_args: tuple[str, str] | None = None
        self.sendmail_args: tuple[str, list[str], str] | None = None
        SMTPStub.instances.append(self)

    def __enter__(self) -> "SMTPStub":  # noqa: D105
        return self

    def __exit__(self, *_args: object) -> None:  # noqa: D105
        pass

    def starttls(self) -> None:
        self.starttls_calls += 1

    def login(self, username: str, password: str) -> None:
        self.login_args = (username, password)

    def sendmail(self, sender: str, recipients: list[str], message: str) -> None:
        self.sendmail_args = (sender, recipients, message)


def _set_mail_env(
    monkeypatch: pytest.MonkeyPatch, *, use_tls: bool, host: str | None = "smtp.test"
) -> None:
    monkeypatch.setattr(envs, "MAIL_HOST", host)
    monkeypatch.setattr(envs, "MAIL_PORT", 587)
    monkeypatch.setattr(envs, "MAIL_USERNAME", "mailer")
    monkeypatch.setattr(envs, "MAIL_PASSWORD", "secret")
    monkeypatch.setattr(envs, "MAIL_FROM", "noreply@strivium.test")
    monkeypatch.setattr(envs, "MAIL_USE_TLS", use_tls)


def test_send_should_starttls_when_mail_use_tls_is_true(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_mail_env(monkeypatch, use_tls=True)
    SMTPStub.instances = []
    monkeypatch.setattr(send_mail_module.smtplib, "SMTP", SMTPStub)

    SendMail().send(
        SendMailDTO(
            destination="doctor@strivium.test",
            subject="Convite",
            body="Mensagem de teste",
        )
    )

    smtp = SMTPStub.instances[0]
    assert smtp.starttls_calls == 1
    assert smtp.login_args == ("mailer", "secret")
    assert smtp.sendmail_args is not None


def test_send_should_not_starttls_when_mail_use_tls_is_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_mail_env(monkeypatch, use_tls=False)
    SMTPStub.instances = []
    monkeypatch.setattr(send_mail_module.smtplib, "SMTP", SMTPStub)

    SendMail().send(
        SendMailDTO(
            destination="doctor@strivium.test",
            subject="Convite",
            body="Mensagem de teste",
        )
    )

    smtp = SMTPStub.instances[0]
    assert smtp.starttls_calls == 0


def test_send_multiple_should_starttls_when_mail_use_tls_is_true(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_mail_env(monkeypatch, use_tls=True)
    SMTPStub.instances = []
    monkeypatch.setattr(send_mail_module.smtplib, "SMTP", SMTPStub)

    SendMail().send_multiple(
        SendMultipleMailDTO(
            destinations=["one@strivium.test", "two@strivium.test"],
            subject="Comunicado",
            body="Mensagem de teste",
        )
    )

    smtp = SMTPStub.instances[0]
    assert smtp.starttls_calls == 1
    assert smtp.sendmail_args is not None
    sender, recipients, _message = smtp.sendmail_args
    assert sender == "noreply@strivium.test"
    assert recipients == ["one@strivium.test", "two@strivium.test"]


def test_send_multiple_should_validate_envs_before_connecting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_mail_env(monkeypatch, use_tls=True, host=None)
    SMTPStub.instances = []
    monkeypatch.setattr(send_mail_module.smtplib, "SMTP", SMTPStub)

    with pytest.raises(Exception, match="mail host is not set"):
        SendMail().send_multiple(
            SendMultipleMailDTO(
                destinations=["one@strivium.test"],
                subject="Comunicado",
                body="Mensagem de teste",
            )
        )

    assert SMTPStub.instances == []
