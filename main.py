import os
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace with your Telegram bot token
TOKEN = 'Your Bot Token Here'

# Define the watermark text and font size
WATERMARK_TEXT = 'Your Watermark Text'

def add_watermark(image_file):
    # Open the image and get its width and height
    img = Image.open(image_file)
    img = img.convert("RGBA")
    # Create a new transparent layer for the watermark
    watermark = Image.new(mode='RGBA', size=img.size, color=(0, 0, 0, 0))
    # Use a Draw object to write the watermark text on the transparent layer
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.truetype('fonts/micross.ttf', 38)
    x = 13
    y = 0
    for i in range(4):
        for j in range(25):
            draw.text((x, y), WATERMARK_TEXT, fill=(225, 234, 235, 50), font=font)
            y = y+60
        y = 0
        x = x + 265
    # Rotate the watermark layer by the specified angle
    # watermark = watermark.rotate(ANGLE, expand=True)
    watermark = watermark.resize(img.size)

    # Blend the watermark layer with the original image using alpha compositing
    return Image.alpha_composite(img, watermark).convert("RGB")

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Send me an image and I\'ll add a watermark to it.')

def echo(update, context):
    """Echo the user message."""
    file_id = update.message.photo[-1].file_id
    new_file = context.bot.get_file(file_id)
    filename = os.path.join('downloads', f'{file_id}.jpg')
    new_file.download(filename)
    new_image = add_watermark(filename)
    new_filename = os.path.join('downloads', f'{file_id}_watermarked.jpg')
    new_image.save(new_filename, 'JPEG')
    context.bot.send_photo(update.message.chat_id, photo=open(new_filename, 'rb'))

def main():
    """Start the bot."""
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))

    # Add message handler for images
    dp.add_handler(MessageHandler(Filters.photo, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
