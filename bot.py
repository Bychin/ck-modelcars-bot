from telegram.error import TimedOut
from telegram.ext import Updater, CommandHandler

from parsers.f1_page import get_models_id
from parsers.model import Model
from utils.cfg import get_param


BOT_TOKEN = get_param('bot_token')
FRESH_LISTING_JOB = 'fresh_listings_job'


def check_model(update, context):
    model_id = context.args[0]
    update.message.reply_text(
        'Amount for {}: {}'.format(model_id, Model(model_id).available_amount()))

def update_fresh_listings(context):
    chat_id = context.job.context
    models_id = get_models_id()

    for model_id in models_id:
        m = Model(model_id, parse=True)
        try:
            context.bot.send_photo(chat_id, m.img_urls[0], caption=m.full_name, timeout=5)
        except TimedOut:
            context.bot.send_message(chat_id, m.full_name)

def subscribe_for_fresh_listings(update, context):
    job = context.job_queue.run_repeating(
        update_fresh_listings, interval=60, first=5, context=update.message.chat_id)
    context.chat_data[FRESH_LISTING_JOB] = job

    update.message.reply_text(
        'You have successfully subscribed for receiving notifications about new listings!')

def unsubscribe_from_fresh_listings(update, context):
    if FRESH_LISTING_JOB not in context.chat_data:
        update.message.reply_text('You do not have an active subscription for new listings.')
        return

    job = context.chat_data[FRESH_LISTING_JOB]
    job.schedule_removal()
    del context.chat_data[FRESH_LISTING_JOB]

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
