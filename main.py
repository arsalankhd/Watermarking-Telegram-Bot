from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image, ImageDraw, ImageFont

# Define your bot token here
TOKEN = '5974826484:AAG5K_drboV65jqouJtfGdrVQPoOlA6YyMw'

# Define the watermark text here
WATERMARK_TEXT = 'Marinoperfume'

# Define the font used for the watermark here
FONT = ImageFont.load_default()

# Define a function that adds a watermark to an image
def add_watermark_to_image(file):
    image = Image.open(file)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), WATERMARK_TEXT, fill=(255, 255, 255), font=FONT)
    watermarked_file = 'watermarked_' + file
    image.save(watermarked_file)
    return watermarked_file

# Set up the telegram bot webhook
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define a function to handle incoming messages
def handle_message(update, context):
    # Check if the message contains an image
    if update.message.photo:
        # Get the highest quality version of the image
        photo_file = update.message.photo[-1].get_file()
        # Download the image file
        file_path = photo_file.download()
        # Add the watermark to the image
        watermarked_file = add_watermark_to_image(file_path)
        # Send the watermarked image back to the user
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(watermarked_file, 'rb'))
    else:
        # If the message doesn't contain an image, send an error message
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please send an image.')

# Set up the message handler and start the bot
message_handler = MessageHandler(Filters.photo, handle_message)
dispatcher.add_handler(message_handler)
updater.start_polling()
