import discord
from discord.ext import commands
import os
import asyncio
import subprocess

# --- Bot setup ---
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = commands.Bot(command_prefix="veb", intents=discord.Intents.all())

# 100 frei0r filters list (shortened for demo)
FREI0R_FILTERS = [
    "3dflippo", "alphagrad", "alphaspot", "balanc0r", "baltan",
    "blend", "brightness", "burn", "cartoon", "cluster",
    "colgate", "contrast0r", "defish0r", "delay0r", "dither",
    "edgeglow", "emboss", "equaliz0r", "facebl0r", "glow",
    "grain", "hueshift0r", "invert0r", "kaleid0r", "letterb0xed",
    "median", "mirror", "nosync0r", "plasma", "posterize",
    "primaries", "quark", "rgbnoise", "sat0r", "scanline0r",
    "select0r", "sharpen", "sigmoidaltransfer", "sobel", "softglow",
    "spillsupress", "squareblur", "tehroxx0r", "threshold0r", "timedelay0r",
    "tint0r", "twolay0r", "vertigo", "vignette", "water",
    "xglow", "zscale", "cartoon", "mosaic", "grayscale",
    "sepia", "polar", "distort", "fish", "wobble",
    "waves", "mirror", "blur", "sharpen", "glow2",
    "echo", "contrast", "zoom", "tile", "swirl",
    "motionblur", "sparkle", "heat", "warp", "pulse",
    "shift", "oilpainting", "stretch", "droste", "feedback",
    "lines", "lighttunnel", "cube", "snow", "spin",
    "chromakey", "keysaturation", "keyspill", "softfocus", "facedetect",
    "bulge", "pinch", "circleblur", "glass", "lensdistortion"
]

# --- Helper: run ffmpeg command ---
async def run_ffmpeg(input_file, output_file, filter_name):
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", f"frei0r={filter_name}",  # apply frei0r filter
        "-preset", "fast", output_file
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()

# --- Command: apply frei0r filter ---
@bot.command()
async def frei0r(ctx, filter_name: str):
    if filter_name not in FREI0R_FILTERS:
        await ctx.send(f"❌ Invalid filter. Choose from:\n`{', '.join(FREI0R_FILTERS[:20])}...`")
        return

    if not ctx.message.attachments:
        await ctx.send("📎 Please attach a video file.")
        return

    attachment = ctx.message.attachments[0]
    input_file = f"input_{ctx.author.id}.mp4"
    output_file = f"output_{ctx.author.id}.mp4"

    await attachment.save(input_file)
    await ctx.send(f"🎥 Applying `{filter_name}` filter...")

    await run_ffmpeg(input_file, output_file, filter_name)

    if os.path.exists(output_file):
        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)
    if os.path.exists(input_file):
        os.remove(input_file)

# --- Run bot ---
bot.run(TOKEN)
