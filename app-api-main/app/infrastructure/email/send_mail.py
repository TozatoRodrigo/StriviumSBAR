import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.environment import envs

from .dto.send_mail_dto import SendMailDTO, SendMultipleMailDTO


class SendMail:
    def __init__(self) -> None:
        self.host = envs.MAIL_HOST
        self.port = envs.MAIL_PORT
        self.username = envs.MAIL_USERNAME
        self.password = envs.MAIL_PASSWORD
        self.from_email = envs.MAIL_FROM
        self.use_tls = envs.MAIL_USE_TLS

    def send(self, send_mail_dto: SendMailDTO) -> None:
        self.__validate_envs()
        try:
            if send_mail_dto.html_body:
                message = MIMEMultipart("alternative")
            else:
                message = MIMEMultipart()

            message["From"] = self.from_email
            message["To"] = send_mail_dto.destination
            message["Subject"] = send_mail_dto.subject
            if send_mail_dto.cc:
                message["Cc"] = ", ".join(send_mail_dto.cc)

            if send_mail_dto.body:
                text_part = MIMEText(send_mail_dto.body, "plain")
                message.attach(text_part)

            if send_mail_dto.html_body:
                html_part = MIMEText(send_mail_dto.html_body, "html")
                message.attach(html_part)

            recipients = [send_mail_dto.destination]
            if send_mail_dto.cc:
                recipients.extend(send_mail_dto.cc)
            if send_mail_dto.bcc:
                recipients.extend(send_mail_dto.bcc)

            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)

                text = message.as_string()
                server.sendmail(self.from_email, recipients, text)

        except smtplib.SMTPException as e:
            msg = f"Failed to send email: {e!s}"
            raise Exception(msg) from e
        except Exception as e:
            msg = f"Unexpected error sending email: {e!s}"
            raise Exception(msg) from e

    def send_multiple(self, send_multiple_mail_dto: SendMultipleMailDTO) -> None:
        self.__validate_envs()
        try:
            if send_multiple_mail_dto.html_body:
                message = MIMEMultipart("alternative")
            else:
                message = MIMEMultipart()

            message["From"] = self.from_email
            message["To"] = ", ".join(send_multiple_mail_dto.destinations)
            message["Subject"] = send_multiple_mail_dto.subject

            if send_multiple_mail_dto.cc:
                message["Cc"] = ", ".join(send_multiple_mail_dto.cc)

            if send_multiple_mail_dto.body:
                text_part = MIMEText(send_multiple_mail_dto.body, "plain")
                message.attach(text_part)

            if send_multiple_mail_dto.html_body:
                html_part = MIMEText(send_multiple_mail_dto.html_body, "html")
                message.attach(html_part)

            recipients = send_multiple_mail_dto.destinations.copy()
            if send_multiple_mail_dto.cc:
                recipients.extend(send_multiple_mail_dto.cc)
            if send_multiple_mail_dto.bcc:
                recipients.extend(send_multiple_mail_dto.bcc)

            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)

                text = message.as_string()
                server.sendmail(self.from_email, recipients, text)

        except smtplib.SMTPException as e:
            msg = f"Failed to send multiple emails: {e!s}"
            raise Exception(msg) from e
        except Exception as e:
            msg = f"Unexpected error sending multiple emails: {e!s}"
            raise Exception(msg) from e

    def __validate_envs(self) -> None:
        if not self.host:
            msg = "mail host is not set"
            raise Exception(msg)
        if not self.port:
            msg = "mail port is not set"
            raise Exception(msg)
        if not self.username:
            msg = "mail username is not set"
            raise Exception(msg)
        if not self.password:
            msg = "mail password is not set"
            raise Exception(msg)
        if not self.from_email:
            msg = "mail from email is not set"
            raise Exception(msg)
