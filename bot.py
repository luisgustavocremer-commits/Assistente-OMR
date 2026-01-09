from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
import os

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQTOKEN")
RENDER_URL = os.getenv("https://assistente-omr.onrender.com")  # URL que o Render vai gerar

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔷✨ *Bem-vindo ao Assistente OMR Claro* ✨🔷\n\n"
        "Sou seu suporte inteligente com IA para operações em campo.\n\n"
        "📡 *Huawei* (BBU, RRU, RF)\n"
        "📶 *MW* Ceragon | Ericsson\n"
        "🌐 *Roteadores* Cisco ASR-920 | ZTE\n"
        "🔌 *Energia* e infraestrutura\n"
        "📍 *Localização* de sites + rotas\n"
        "📦 *Gestão* de sobressalentes\n"
        "⏰ *Lembretes* e tarefas\n\n"
        "Digite sua dúvida! 👇",
        parse_mode="Markdown"
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem_usuario = update.message.text

    # Envia para a IA
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente técnico especializado em OMR da Claro no Paraná e Santa Catarina. "
                    "Ajuda com: Huawei RF (BBU 5900/5910/5920, RRU 3900/3910/5900), "
                    "MW (Ceragon CeraOS/LACP, Ericsson MINI-LINK), "
                    "roteadores Cisco ASR-920 e ZTE M6000-2S16, "
                    "energia (retificadores, baterias, A/C, geradores), "
                    "infraestrutura (aterramento, torres, acesso), "
                    "lembretes, tarefas e organização. "
                    "Sempre pergunte o modelo do equipamento quando necessário. "
                    "Seja direto, claro, técnico e use emojis quando apropriado. "
                    "Formate respostas com Markdown quando útil."
                )
            },
            {
                "role": "user",
                "content": mensagem_usuario
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )

    resposta = chat_completion.choices[0].message.content
    await update.message.reply_text(resposta, parse_mode="Markdown")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # WEBHOOK (para Render Web Service)
    await app.bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

    # Inicia o servidor
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=f"{RENDER_URL}/{TOKEN}"
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

