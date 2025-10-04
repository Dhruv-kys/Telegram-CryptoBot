import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration - Using environment variables for deployment
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '@Abhijeet_btc')
WELCOME_IMAGE_PATH = os.getenv('WELCOME_IMAGE_PATH', 'coin.jpeg')

# Validate bot token exists
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found! Please set it in .env file or environment variables")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start command is issued"""
    
    # Welcome message
    welcome_text = (
        "👋 Welcome to the ultimate launchpad for your crypto project!\n\n"
        "💡 Whether you're launching a new token or aiming to skyrocket an existing one, "
        "you're in the right place.\n\n"
        "✨ Click \"Launch Coin\" below to get started on your journey to the moon!"
    )
    
    # Create inline keyboard with Launch Coin button
    keyboard = [[InlineKeyboardButton("🚀 Launch Coin", callback_data='launch_coin')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the full image first without any resizing
    try:
        with open(WELCOME_IMAGE_PATH, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
    except FileNotFoundError:
        print(f"Image not found at {WELCOME_IMAGE_PATH}")
    
    # Then send text message with button
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'launch_coin':
        # Send typing action for more engaging experience
        await query.message.chat.send_action(action="typing")
        
        # Add a small delay for anticipation
        import asyncio
        await asyncio.sleep(1.5)
        
        # Send the promotional message (text only, no image)
        promo_text = (
            "🚀 Ready to Make Your Coin Go Viral?\n\n"
            "We help crypto projects launch, scale, and hit the moon with powerful marketing strategies, "
            "influencer pushes, and viral Telegram campaigns.\n\n"
            "🔥 Whether it's a meme coin or a serious project — we build the hype. "
            "You grow the market cap.\n\n"
            f"📩 DM {ADMIN_USERNAME} now to start your moon mission!"
        )
        
        # Create contact button
        keyboard = [[InlineKeyboardButton("💬 Contact Now", url=f'https://t.me/{ADMIN_USERNAME.replace("@", "")}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(promo_text, reply_markup=reply_markup)

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()