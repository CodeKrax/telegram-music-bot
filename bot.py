from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import os
import uuid

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Use env variable

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Send /play <song name> to play music!")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Example: /play tum hi ho")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching: {query}")

    temp_filename = f"{uuid.uuid4().hex}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])

        with open(temp_filename, 'rb') as audio:
            await update.message.reply_audio(audio, title=query)
        os.remove(temp_filename)

    except Exception as e:
        await update.message.reply_text("⚠️ Song not found.")
        print("Error:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.run_polling()
