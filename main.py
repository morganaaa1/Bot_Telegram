import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Replace YOUR_BOT_TOKEN with the token you received from BotFather
bot = telegram.Bot(token='TOKEN_BOT')

# Replace YOUR_CHANNEL_ID with the ID of the channel you want to post messages to
channel_id = '@morganaaafjb'

# Log a message to indicate that your bot is running
print('Bot is running...')

# Define a function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a photo or text and I'll post it to the channel.")

def post_to_channel(update, context):
    message = update.message
    if not bot.get_chat_member(chat_id=channel_id, user_id=update.message.from_user.id).status in ["member", "administrator", "creator"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please join the channel first: " + channel_id)
        return  # Return without sending any message if user is not a member of the channel
    
    # Check if the message contains both a photo and text
    if message.photo and message.caption:
        # If the message contains both a photo and text, post them together to the channel
        bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=message.caption)
    elif message.photo:
        # If the message contains only a photo, post it to the channel
        bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id)
    elif message.text:
        # If the message contains only text, post it to the channel
        bot.send_message(chat_id=channel_id, text=message.text)

# Set up a MessageHandler to call the post_to_channel function whenever the bot receives a message
updater = Updater(token='TOKEN_BOT', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.all, post_to_channel))

# Start the bot
updater.start_polling()
updater.idle()
