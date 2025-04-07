from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import random
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send introduction first
    await update.message.reply_text(
        "Hello! 👋\n\nI'm your personal assistant bot. You can interact with me by choosing any of the options below. "
        "I can send you cute photos, play a guessing game with you, or tell you a random joke. "
        "Just click the buttons to get started!"
    )
    
    # Now, show the menu with buttons
    keyboard = [
        [InlineKeyboardButton("Send Photo 📷", callback_data='photo')],
        [InlineKeyboardButton("Guess Game 🎯", callback_data='game')],
        [InlineKeyboardButton("Random Joke 😂", callback_data='joke')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)




async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'photo':
        await query.message.reply_photo('https://placekitten.com/400/300', caption="Here's a cute cat 🐱")

    elif query.data == 'game':
        number = random.randint(1, 10)
        context.user_data['number'] = number
        await query.message.reply_text("I'm thinking of a number between 1 and 10. Guess it by typing /guess <number>!")

    elif query.data == 'joke':
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to therapy? It had too many bytes.",
            "Why do cows have hooves instead of feet? Because they lactose."
        ]
        await query.message.reply_text(random.choice(jokes))

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'number' not in context.user_data:
        await update.message.reply_text("Start the game first by clicking 'Guess Game 🎯'!")
        return

    try:
        user_guess = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /guess <number>")
        return

    number = context.user_data['number']

    if user_guess == number:
        await update.message.reply_text(f"🎉 Correct! You guessed it: {number}")
        del context.user_data['number']  # Reset after correct guess
    else:
        await update.message.reply_text(f"❌ Nope! Try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Use /start to see the menu!')

# --- MAIN ---

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("guess", guess))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running... 🚀")
    app.run_polling()

if __name__ == '__main__':
    main()
