import logging

from telegram import ParseMode
from telegram.error import TimedOut
from telegram.ext import Updater, CommandHandler

from parsers.listing import new_F1_listing
from parsers.model import Model
from utils.cfg import get_param


BOT_TOKEN = get_param('bot_token')
NEW_LISTING_JOB = 'new_listings_job'


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=get_param('log_path'), filemode='a')
logger = logging.getLogger(__name__)

#  parser setup

F1_listing = new_F1_listing()

#  bot setup

def check_availability_for_model(update, context):
    user = update.message.from_user
    logger.info("debug: check_availability_for_model entry, user: %s", user.id)

    if len(context.args) == 0:
        update.message.reply_text(
            'Please pass an URL for a model after the command.')

    model_url = context.args[0]
    model = Model.from_url(model_url)

    update.message.reply_text(
        'Available to order amount: {}'.format(model.available_amount()))

def update_new_listings(context):
    chat_id = context.job.context
    logger.info("debug: update_new_listings entry, chat_id: %s", chat_id)

    models_id = sorted(F1_listing.get_new_models_id(), reverse=True)
    logger.info("debug: got new models: %s, chat_id: %s", models_id, chat_id)

    for model_id in models_id:
        m = Model(model_id, parse=True)
        context.bot.send_message(chat_id, m.str_html(), parse_mode=ParseMode.HTML)

def subscribe_for_new_listings(update, context):
    user = update.message.from_user
    logger.info("debug: subscribe_for_new_listings entry, user: %s, chat_id: %s", user.id, update.message.chat_id)

    if NEW_LISTING_JOB in context.chat_data:
        update.message.reply_text('You have an active subscription for new listings.')
        return

    job = context.job_queue.run_repeating(
        update_new_listings, interval=60, first=1, context=update.message.chat_id)
    context.chat_data[NEW_LISTING_JOB] = job

    update.message.reply_text(
        'You have successfully subscribed for receiving notifications about new listings!')

def unsubscribe_from_new_listings(update, context):
    user = update.message.from_user
    logger.info("debug: unsubscribe_from_new_listings entry, user: %s", user.id)

    if NEW_LISTING_JOB not in context.chat_data:
        update.message.reply_text('You do not have an active subscription for new listings.')
        return

    job = context.chat_data[NEW_LISTING_JOB]
    job.schedule_removal()
    del context.chat_data[NEW_LISTING_JOB]

    update.message.reply_text(
        'You have successfully unsubscribed from receiving notifications about new listings.')


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('check', check_availability_for_model))
updater.dispatcher.add_handler(
    CommandHandler('subscribe', subscribe_for_new_listings))
updater.dispatcher.add_handler(
    CommandHandler('unsubscribe', unsubscribe_from_new_listings))

updater.start_polling()
updater.idle()
