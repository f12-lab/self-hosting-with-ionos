import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters, ContextTypes
import requests # type: ignore

load_dotenv()

# Define los estados de la conversación
ASK_URL = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Share a link to stream videos or audio.")

async def dv(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please, send the video URL.")
    return ASK_URL

async def da(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please, send the audio URL.")
    return ASK_URL

async def receive_url(update: Update, context: CallbackContext) -> int:
    # Capturar la URL proporcionada por el usuario
    url = update.message.text

    if not url.startswith("http://") and not url.startswith("https://"):
        await update.message.reply_text("Invalid URL. Please provide a valid link.")
        return ASK_URL

    try:
        # Enviar la URL al servidor de procesamiento
        backend_url = "http://localhost:5000/process"  # URL de tu backend
        response = requests.post(backend_url, json={"url": url})

        if response.status_code == 200:
            stream_link = response.json().get("stream_link", "")
            mobile_link = "https://fondomarcador.com/videos/hls/stream.m3u8"
            if stream_link:
                await update.message.reply_text(f"Your stream is live here:\n"
                                            f"- Mobile: {mobile_link}\n"
                                            f"- PC: {stream_link}")
            else:
                await update.message.reply_text("Streaming started but no stream link available.")
        else:
            await update.message.reply_text("Error while starting the streaming.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Available commands:\n/start\n/dv\n/da\n/cancel")

def main() -> None:
    token = os.getenv("TELEGRAM_APITOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("dv", dv), CommandHandler("da", da)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_url)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conversation_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
