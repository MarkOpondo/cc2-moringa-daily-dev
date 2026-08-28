import smtplib
from email.message import EmailMessage
from flask import current_app


def send_password_reset_email(recipient_email, reset_url):
    mail_username = current_app.config.get("MAIL_USERNAME")
    mail_password = current_app.config.get("MAIL_PASSWORD")
    mail_server = current_app.config.get("MAIL_SERVER")
    mail_port = current_app.config.get("MAIL_PORT")
    mail_use_tls = current_app.config.get("MAIL_USE_TLS")

    if not mail_username or not mail_password:
        raise RuntimeError(
            "Email configuration is missing. "
            "Set MAIL_USERNAME and MAIL_PASSWORD."
        )

    message = EmailMessage()

    message["Subject"] = "Moringa Daily Dev - Password Reset"
    message["From"] = mail_username
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

We received a request to reset your Moringa Daily Dev password.

Click the link below to create a new password:

{reset_url}

This link will expire after 1 hour.

If you did not request a password reset, you can safely ignore this email.

Regards,
Moringa Daily Dev Team
"""
    )

    with smtplib.SMTP(mail_server, mail_port) as smtp:
        if mail_use_tls:
            smtp.starttls()

        smtp.login(mail_username, mail_password)
        smtp.send_message(message)