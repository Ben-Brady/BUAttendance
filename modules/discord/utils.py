import discord
import io


class ImageDownloadFailure(Exception): pass

async def download_image(message: discord.Message) -> bytes:
    attachments = message.attachments
    if len(attachments) == 0:
        raise ImageDownloadFailure("Please submit a qr code image")

    if len(attachments) != 1:
        raise ImageDownloadFailure("Please submit only one image")
    
    image = attachments[0]
    if image.content_type and "image" not in image.content_type:
        raise ImageDownloadFailure("Please submit an image")

    buf = io.BytesIO()
    await image.save(buf)
    return buf.read()
