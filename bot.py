from telegram.ext import Updater, CommandHandler

from model_parser import get_amount

BOT_TOKEN = '1009278594:AAHsRiNo9n0gFWugQH2fcJog7mKHoF98iMQ'

def hello(update, context):
    update.message.reply_text(
        'Hello {}, args: {}'.format(update.message.from_user.first_name, context.args))

def check_model(update, context):
    model_id = context.args[0]
    update.message.reply_text(
        'Amount for {}: {}'.format(model_id, get_amount(model_id)))

updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('check', hello))

updater.start_polling()
updater.idle()