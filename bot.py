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
    context.bot.send_message(
        chat_id=context.job.context, text='\n'.join(models_id))

def subscribe_for_fresh_listings(update, context):
    context.job_queue.run_repeating(update_fresh_listings, interval=60, first=5, context=update.message.chat_id)
    update.message.reply_text(
        'You have successfully subscribed for receiving notifications about new listings!')

def unsubscribe_from_fresh_listings(update, context):
    context.job_queue.stop()
    update.message.reply_text(
        'You have successfully unsubscribed from receiving notifications about new listings.')


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('check', check_model))
updater.dispatcher.add_handler(
    CommandHandler('subscribe', subscribe_for_fresh_listings))
updater.dispatcher.add_handler(
    CommandHandler('unsubscribe', unsubscribe_from_fresh_listings))

updater.start_polling()
updater.idle()

