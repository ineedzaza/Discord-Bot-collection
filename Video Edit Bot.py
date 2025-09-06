import discord
from discord.ext import commands
import subprocess
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ensure you have a folder for processed videos
OUTPUT_FOLDER = "processed_videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# List of 100 Frei0r filters (example names; you can customize)
frei0r_filters = [
    "blur0", "brightness", "contrast", "invert", "flip", "mirror",
    "rotate", "saturate", "hue", "grayscale", "edge_detect", "sharpen",
    "fadeblack", "fadewhite", "colorize", "vignette", "kaleidoscope",
    "oldfilm", "pixelize", "solarize", "noise", "posterize", "wave",
    "swirl", "zoomblur", "oilpaint", "glow", "emboss", "cartoon",
    "lensflare", "motionblur", "deinterlace", "fade", "flash", "negative",
    "lighten", "darken", "soften", "roughen", "twirl", "sketch", "sepia",
    "chromakey", "threshold", "edge", "median", "bloom", "sine", "ripple",
    "glitch", "fractal", "colorbalance", "blend", "tile", "distort",
    "fisheye", "blurtilt", "zoom", "lens", "vhs", "grain", "hblur",
    "vblur", "shrink", "stretch", "rotatex", "rotatey", "rotatez",
    "motion", "pixel", "invertcolors", "poster", "flashwhite", "fadein",
    "fadeout", "brightnesscontrast", "solar", "halo", "edgeglow", "softglow",
    "bokeh", "filmgrain", "noisegrain", "sparkle", "dotscreen", "halftone",
    "radialblur", "circleblur", "swirl2", "kaleido2", "waves", "ripple2",
    "mosaic", "emboss2", "glow2", "oilpaint2", "cartoon2", "lens2", "vhs2"
]

# Command to apply a Frei0r filter
@bot.command()
async def applyfilter(ctx, filter_index: int):
    if not ctx.message.attachments:
        await ctx.send("Please attach a video file.")
        return

    if filter_index < 0 or filter_index >= len(frei0r_filters):
        await ctx.send(f"Filter index must be between 0 and {len(frei0r_filters)-1}.")
        return

    attachment = ctx.message.attachments[0]
    input_path = f"{OUTPUT_FOLDER}/{attachment.filename}"
    output_path = f"{OUTPUT_FOLDER}/filtered_{attachment.filename}"

    await attachment.save(input_path)

    filter_name = frei0r_filters[filter_index]
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"frei0r={filter_name}",
        "-y",  # overwrite if exists
        output_path
    ]

    # Run FFmpeg
    process = subprocess.run(ffmpeg_command, capture_output=True, text=True)

    if process.returncode == 0:
        await ctx.send(file=discord.File(output_path))
        os.remove(input_path)
        os.remove(output_path)
    else:
        await ctx.send(f"Error applying filter: {process.stderr}")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
