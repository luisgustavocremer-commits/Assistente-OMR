from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

import os
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQTOKEN")

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Sou o Assistente OMR da Claro.\n"
        "Posso te ajudar com equipamentos, tarefas, lembretes e rotas.\n"
        "Digite sua dúvida!"
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem_usuario = update.message.text

    # Envia para a IA
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente técnico especializado em OMR da Claro. "
                    "Ajuda com: Huawei RF, MW (Ceragon/Ericsson), roteadores Cisco/ZTE, "
                    "energia, infraestrutura, lembretes e tarefas. "
                    "Sempre pergunte o modelo do equipamento quando necessário. "
                    "Seja direto, claro e técnico."
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
    await update.message.reply_text(resposta)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot com IA rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
