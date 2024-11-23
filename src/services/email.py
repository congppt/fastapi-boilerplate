import logging
from email.message import EmailMessage
from typing import Sequence, Literal

from aiosmtplib import SMTP
from fastapi import UploadFile

from config.handler import aget_config
from constants.cache import EMAIL_SERVER
from db import aget_db


async def send_email(body: str,
                     sender: str,
                     recipients: Sequence[str],
                     subject: str,
                     attachments: Sequence[UploadFile | str] = None,
                     inline_images: dict[str, UploadFile | str] = None,
                     protocol: Literal['smtp', 'http'] = 'smtp') -> None:
    message = EmailMessage()
    message.add_header('Subject', subject)
    message.set_content(body, subtype='html')
    for attachment in attachments or []:
        if isinstance(attachment, UploadFile):
            data = await attachment.read()
            filename = attachment.filename
        else:
            try:
                with open(attachment, "rb") as f:
                    data = f.read()
                    filename = attachment.split("/")[-1]
            except FileNotFoundError:
                logging.warning(f'{attachment} was not found')
                continue
        message.add_attachment(data, maintype="application", subtype="octet-stream", filename=filename)
    inline_images = inline_images or {}
    for cid, image in inline_images.items():
        if isinstance(image, UploadFile):
            data = await image.read()
            ext = image.filename.split(".")[-1]
        else:
            try:
                with open(image, "rb") as f:
                    data = f.read()
                    ext = image.split(".")[-1]
            except FileNotFoundError:
                logging.warning(f'{image} was not found.')
                continue
        message.add_related(data, maintype="image",subtype=ext, cid=f"<{cid}>")
        if protocol == 'smtp':
            async for db in aget_db():
                email_server: dict = await aget_config(EMAIL_SERVER, db=db)
                smtp = SMTP(**email_server)
                await smtp.send_message(message, sender=sender, recipients=recipients)
        elif protocol == 'http':
            pass