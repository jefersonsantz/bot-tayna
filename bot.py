import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
from flask import Flask
from threading import Thread

# Configurações
TOKEN = '7749292496:AAGL5ciM9VgGuNj4LQzcMDQ51c11Yodc4ho'
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxQqw8MbxL96sd0rmgijGO7GzJ91nrshT97hyw4S9mFi3-rtBsoJOB_YeAGtNZUy04/exec'
LINK_GRUPO_VIP = "https://t.me/+q_W1Wq63r8pmZGMx"  # <-- SUBSTITUA PELO SEU LINK CORRETO

# Função para formatar datas
def format_data(data_iso):
    data = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
    return data.strftime('%d/%m/%Y')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    try:
        response = requests.get(APPS_SCRIPT_URL, params={'user_id': user_id})
        data = response.json()
    except Exception as e:
        await update.message.reply_text('❌ Erro ao consultar o servidor. Tente novamente mais tarde.')
        return

    if 'error' in data:
        await update.message.reply_text('🚫 Você não está registrado. Realize a compra para liberar o acesso.')
    else:
        data_inicio = format_data(data['data_inicio'])
        data_fim = format_data(data['data_fim'])

        mensagem = (
            f"👋 Olá, {data['nome']}!\n"
            f"📦 Plano: {data['plano']}\n"
            f"📅 Início: {data_inicio}\n"
            f"📅 Término: {data_fim}\n\n"
            "✅ Seu acesso foi liberado!\n"
            "Clique no botão abaixo para entrar no grupo VIP: 👇"
        )

        # Botão com link
        keyboard = [[InlineKeyboardButton("🚪 Entrar no Grupo VIP", url=LINK_GRUPO_VIP)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(mensagem, reply_markup=reply_markup)

# Função principal do bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

# FLASK para manter Railway ativo
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "✅ Bot do Telegram está rodando!"

def run():
    flask_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = Thread(target=run)
    thread.start()

# Inicializa tudo
if __name__ == '__main__':
    keep_alive()
    main()
