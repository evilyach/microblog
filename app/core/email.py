from threading import Thread

from flask import current_app
from flask_babel import _
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(
    subject: str,
    sender: str,
    recipients: str,
    text_body: str,
    html_body: str,
) -> None:
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    ).start()