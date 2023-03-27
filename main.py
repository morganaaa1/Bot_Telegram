import telegram
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Replace YOUR_BOT_TOKEN with the token you received from BotFather
bot = telegram.Bot(token='TOKEN_BOT')

# Replace YOUR_CHANNEL_ID with the ID of the channel you want to post messages to
channel_id = 'CHANNEL_ID'

channel_name = 'CHANNEL_NAME'

# Log a message to indicate that your bot is running
print('Bot is running...')

# Define the link button
button = InlineKeyboardButton(text="Join FJB Jual Beli Genshin Impact Indonesia", url="https://t.me/morganaaafjb")

# Define the keyboard markup with the button
keyboard = InlineKeyboardMarkup([[button]])

# Define the image and description to send
image_url = "https://i.imgur.com/ZGzG7Gz.png"
description = (
"<b>Waspada akun Palsu! Contact MM Group :</b>\n"
    "Facebook : www.facebook.com/alinabilah.ramadhan/\n"
    "Telegram : @gorengannyender\n"
    "Whatsapp : 0895344218271\n\n"
    "<b>Rules :</b>\n"
    "1. Selalu gunakan MM grup agar terhindar dari hal penipuan\n"
    "2. Dilarang toxic berlebih\n"
    "3. Price police awto kick\n"
    "4. Apabila terjadi HB / lainnya diluar tanggung jawab admin\n"
    "5. Dilarang Share link Grup\n"
    "6. No Lelang\n\n"
    "<b>Fee MM :</b>\n"
    "5k → 0-199k\n"
    "10k → 200k-399k\n"
    "15k → 400k-899K\n"
    "20k → 900k-1000k\n"
    "3% → 1jt keatas\n\n"
    "<b>Penggunaan BOT :</b>\n"
    "Kirim command /post terlebih dahulu agar kalian bisa mengirimkan detail account yang akan kalian jual\n\n"
    "NOTE :\n"
    "Gunakan selalu hastag #WTB untuk Mencari akun atau #WTS untuk mencari akun. dan jangan lupa cantumkan contact seller\n"
)

# Define a function to handle the /start command
def start(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=description, parse_mode=ParseMode.HTML, reply_markup=keyboard)


# Set up a flag to indicate whether the bot is waiting for the /post command
awaiting_post_command = False

def post(update, context):
    global awaiting_post_command
    awaiting_post_command = True
    # Store the user ID in context to check if the user is a member of the channel later
    context.user_data['user_id'] = update.message.from_user.id
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sekarang kalian bisa kirim postingan kalian ke bot.")

def post_to_channel(update, context):
    global awaiting_post_command
    message = update.message

    # Check if the user sent the /post command before sending any message or image
    if not awaiting_post_command:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Kirim command /post terlebih dahulu yaa, sebelum kirim postingan kalian.")
        return  # Return without sending any message if the user didn't send the /post command first

    # Check if the user is a member of the channel
    if not bot.get_chat_member(chat_id=channel_id, user_id=update.message.from_user.id).status in ["member", "administrator", "creator"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Tolong masuk ke Channel nya terlebih dahulu yaa: " + channel_name)
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

    # Set the flag to indicate that the bot is not waiting for the /post command anymore
    awaiting_post_command = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="Terima Kasih! Jika kalian mau posting lagi kalian bisa kirim lagi command /post. Dan jangan lupa selalu gunakan admin setempat")



# Set up a MessageHandler to call the post_to_channel function whenever the bot receives a message
updater = Updater(token='BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("post", post))
dispatcher.add_handler(MessageHandler(Filters.all, post_to_channel))

# Start the bot
updater.start_polling()
updater.idle()
