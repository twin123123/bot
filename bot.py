import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '7588268422:AAGfXxTO_2rme-goLJ0MdxwF_5tsy3E_GSA'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Рулетка', 'Красное/Черное'], ['Курс']]
    await update.message.reply_text(
        'Привет! Выбери опцию:',
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

if __name__ == '__main__':
    main()
