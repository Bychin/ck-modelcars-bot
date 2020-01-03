from telegram.ext import Updater, CommandHandler

from parsers.f1_page import get_models_id
from parsers.model import get_amount
from utils.cfg import get_param


BOT_TOKEN = get_param('bot_token')
CHAT_ID = '@ck_modelcars_scraper_bot'


def check_model(update, context):
    model_id = context.args[0]
    update.message.reply_text(
        'Amount for {}: {}'.format(model_id, get_amount(model_id)))

def update_fresh_listings(context):
    models_id = get_models_id()
    context.bot.send_message(chat_id=CHAT_ID, 
                             text='\n'.join(models_id))


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('check', check_model))

job_queue = updater.job_queue
job = job_queue.run_repeating(update_fresh_listings, interval=30, first=1)

updater.start_polling()
updater.idle()