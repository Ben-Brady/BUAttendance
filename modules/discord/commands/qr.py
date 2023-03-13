from modules import qrcode, discord
from discord import ApplicationContext, SlashCommand


async def _command(ctx: ApplicationContext):
    if ctx.message == None:
        await ctx.send_response("You did not attach a QR code")
        return

    try:
        data = await discord.download_image(ctx.message)
        value = qrcode.read(data)
        await ctx.send_response(value)
    except qrcode.InvalidQRCode:
        await ctx.send_response.reply("Invalid QR Code")
    except discord.ImageDownloadFailure as e:
        await ctx.send_response(str(e))

qr_command = SlashCommand(
    func=_command,
    name="qr",
    description="",
)