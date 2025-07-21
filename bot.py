import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime  # ✅ Para formatar datas

TOKEN = '7749292496:AAGL5ciM9VgGuNj4LQzcMDQ51c11Yodc4ho'
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxQqw8MbxL96sd0rmgijGO7GzJ91nrshT97hyw4S9mFi3-rtBsoJOB_YeAGtNZUy04/exec'

# ✅ Função para formatar datas no formato brasileiro
def format_data(data_iso):
    data = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
    return data.strftime('%d/%m/%Y')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    try:
        response = requests.get(APPS_SCRIPT_URL, params={'user_id': user_id})
        data = response.json()
    except Exception as e:
        await update.message.reply_text('Erro ao consultar o servidor. Tente novamente mais tarde.')
        return

    if 'error' in data:
        await update.message.reply_text('Você não está registrado. Por favor, realize a compra e tente novamente.')
    else:
        # ✅ Formata as datas
        data_inicio_formatada = format_data(data['data_inicio'])
        data_fim_formatada = format_data(data['data_fim'])

        mensagem = (
    f"👋 Olá, {data['nome']}!\n\n"
    f"📦 Plano ativo: {data['plano']}\n"
    f"📅 Início: {data_inicio_formatada}\n"
    f"⏳ Término: {data_fim_formatada}\n\n"
    "✅ Seu acesso foi liberado!\n\n"
    "👇 Clique no botão abaixo para entrar no *Grupo VIP* exclusivo:"
        )

        # ✅ BOTÃO com o link do grupo
        keyboard = [[InlineKeyboardButton("🔓 Entrar no Grupo VIP🔥", url="https://t.me/+q_W1Wq63r8pmZGMx")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(mensagem, reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

if __name__ == '__main__':
    main()
