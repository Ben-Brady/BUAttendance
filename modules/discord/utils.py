from . import Response
import discord
import io


async def download_image(message: discord.Message) -> bytes:
    attachments = message.attachments
    if len(attachments) == 0:
        raise Response("Please submit a qr code image")

    if len(attachments) != 1:
        raise Response("Please submit only one image")
    
    image = attachments[0]
    if image.content_type and "image" not in image.content_type:
        raise Response("Please submit an image")

    buf = io.BytesIO()
    await image.save(buf)
    return buf.read()
