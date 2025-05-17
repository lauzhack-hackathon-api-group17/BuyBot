"""
Telegram bot to filter and format a list of laptop models using a Together AI LLM.

Run:
    python telegram_laptop_bot.py

BotFather commands:
clear - Clear chat history.
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)
from input_parser import create_specs_database
import sql_database.sql_database_interface as SDI
from keys import TELEGRAM_KEY, TOGETHER_AI
from together import Together
from pprint import pprint
from data_categories_entries.data_categories import Categories

# Constants
MAX_CHAT_HISTORY = 10
TELEGRAM_MAX_OUTPUT = 4096
VERBOSE = True
N_SUGGESTIONS = 5
DEBUG = True

# Global storage
USER_MESSAGES = dict()

# LLM Configuration
print("Using Together AI")
llm_model = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
client = Together(api_key=TOGETHER_AI)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def query_llm(user_input, laptops_list, user_id):
    """Query the LLM with structured laptop data."""
    # Format list-of-lists into readable string for LLM
    laptop_text = "\n".join(
        f"{i+1}. " + " | ".join(row) for i, row in enumerate(laptops_list)
    )

    prompt = (
        "You are an expert tech assistant. "
        "Given the following list of laptop models, and the original user request, "
        f"provide a clean, formatted list with short descriptions for the {N_SUGGESTIONS} best laptops.\n"
        "Please ensure your output is in a clean, structured format for a Telegram message. "
        "Add some basic specifications and how they meet the user's needs, without going too deep.\n"
        "Include the price and a link to the product. "
        "Finally, filter based on the best specs/price ratio.\n\n"
        f"Laptop List:\n{laptop_text}"
        f"\n\nOriginal User Request:\n{user_input}"
    )

    # Maintain simple chat history
    if user_id not in USER_MESSAGES:
        USER_MESSAGES[user_id] = []
    USER_MESSAGES[user_id].append({"role": "user", "content": prompt})

    # Query Together AI
    response = client.chat.completions.create(
        model=llm_model,
        messages=USER_MESSAGES[user_id]
    )
    text_response = response.choices[0].message.content

    USER_MESSAGES[user_id].append({"role": "assistant", "content": text_response})

    if VERBOSE:
        pprint(USER_MESSAGES[user_id])

    # Trim chat history
    if len(USER_MESSAGES[user_id]) > 2 * MAX_CHAT_HISTORY:
        USER_MESSAGES[user_id] = USER_MESSAGES[user_id][-2 * MAX_CHAT_HISTORY:]

    # Truncate if response is too long
    if len(text_response) > TELEGRAM_MAX_OUTPUT:
        text_response = text_response[:TELEGRAM_MAX_OUTPUT - 20] + "\n\nOUTPUT TRUNCATED"

    return f"MODEL: {llm_model}\n\n{text_response}"


async def handle_laptop_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle raw list input of laptop models from user."""
    input_text = update.message.text
    user_id = update.message.from_user.id

    if DEBUG:
        print(f"Received input from user {user_id}: {input_text}")

    try:
        # Generate specs database from input text
        specs_database = create_specs_database(input_text)

        if DEBUG:
            print(f"Generated specs database: {specs_database}")

        # Filter results
        filtered_laptops = SDI.sql_database_interface(Categories.LAPTOPS).filter_database()

        if DEBUG:
            print(f"Filtered laptops: {filtered_laptops}")

        if not filtered_laptops:
            await update.message.reply_text("⚠️ No suitable laptops found after filtering.")
            return

        # Format using LLM
        formatted = query_llm(input_text, filtered_laptops, user_id)

        if DEBUG:
            print(f"Formatted output: {formatted}")

        if VERBOSE:
            logger.info("Filtered laptops: %s", filtered_laptops)

        # Send result
        await update.message.reply_text(formatted, parse_mode="Markdown")
    except Exception as e:
        logger.error("Error processing laptops: %s", str(e))
        await update.message.reply_text("❌ An error occurred while processing the laptops.")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear chat history."""
    user_id = update.message.from_user.id
    if user_id in USER_MESSAGES:
        del USER_MESSAGES[user_id]
    await update.message.reply_text("✅ Chat history cleared.")


def main() -> None:
    """Start the Telegram bot."""
    application = Application.builder().token(TELEGRAM_KEY).build()

    print("Starting Telegram bot...")

    # Handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_laptop_input))
    application.add_handler(CommandHandler("clear", clear, block=False))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

main()