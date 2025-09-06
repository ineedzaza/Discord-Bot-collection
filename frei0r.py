import discord
from discord.ext import commands
import subprocess
import os

# Bot prefix
bot = commands.Bot(command_prefix=".t", intents=discord.Intents.all())

# A dictionary of 50 frei0r effects
frei0r_effects = {
    "glow": "frei0r=glow",
    "edgeglow": "frei0r=edgeglow",
    "twirl": "frei0r=twirl",
    "pixeliz0r": "frei0r=pixeliz0r",
    "water": "frei0r=water",
    "distort0r": "frei0r=distort0r",
    "invert0r": "frei0r=invert0r",
    "posterize": "frei0r=posterize",
    "cartoon": "frei0r=cartoon",
    "scanline0r": "frei0r=scanline0r",
    "threshold0r": "frei0r=threshold0r",
    "sharpen": "frei0r=sharpen",
    "colordistance": "frei0r=colordistance",
    "sobel": "frei0r=sobel",
    "colorize": "frei0r=colorize",
    "perspective": "frei0r=perspective",
    "emboss": "frei0r=emboss",
    "mosaic": "frei0r=mosaic",
    "glitch0r": "frei0r=glitch0r",
    "brightness": "frei0r=brightness",
    "contrast": "frei0r=contrast0r",
    "gamma": "frei0r=gamma",
    "noise": "frei0r=noise",
    "defish": "frei0r=defish",
    "bulge": "frei0r=bulge",
    "kaleidoscope": "frei0r=kaleidoscope",
    "chromakey": "frei0r=chromakey",
    "saturat0r": "frei0r=saturat0r",
    "vignette": "frei0r=vignette",
    "letterb0xed": "frei0r=letterb0xed",
    "delaygrab": "frei0r=delaygrab",
    "ripple": "frei0r=ripple",
    "mirror": "frei0r=mirror",
    "flippo": "frei0r=flippo",
    "spin": "frei0r=spin",
    "waves": "frei0r=waves",
    "lightgraffiti": "frei0r=lightgraffiti",
    "curves": "frei0r=curves",
    "scanlines": "frei0r=scanlines",
    "baltan": "frei0r=baltan",
    "alphagrad": "frei0r=alphagrad",
    "alphaspot": "frei0r=alphaspot",
    "alphatrans": "frei0r=alphatrans",
    "nosync0r": "frei0r=nosync0r",
    "burn": "frei0r=burn",
    "invert": "frei0r=invert",
    "posteriz0r": "frei0r=posteriz0r",
    "threelay0r": "frei0r=threelay0r",
    "bluescreen": "frei0r=bluescreen",
}

# Command to apply frei0r effect
@bot.command()
async def effect(ctx, effect: str):
    if not ctx.message.attachments:
        await ctx.send("Please attach a video file to use this command.")
        return

    if effect not in frei0r_effects:
        await ctx.send(f"Effect not found. Available effects: {', '.join(frei0r_effects.keys())}")
        return

    # Download attached video
    attachment = ctx.message.attachments[0]
    input_file = f"input_{ctx.author.id}.mp4"
    output_file = f"output_{ctx.author.id}.mp4"
    await attachment.save(input_file)

    # Run ffmpeg with frei0r effect
    ffmpeg_command = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", frei0r_effects[effect],
        "-c:a", "copy", output_file
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError:
        await ctx.send("Error while applying effect.")
        os.remove(input_file)
        return

    # Send processed video back
    await ctx.send(file=discord.File(output_file))

    # Cleanup
    os.remove(input_file)
    os.remove(output_file)

bot.run("YOUR_DISCORD_BOT_TOKEN")
