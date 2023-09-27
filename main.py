import logging
import os
from chatgpt import request_chat_gpt
from dotenv import load_dotenv
from telegram import Update, Message, MessageEntity
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
TELEGRAM_API_TOKEN = os.getenv("6535941946:AAFkn48yUIyDFuqr02ufla_TvhJemD-mbhc")


def message_text(message: Message) -> str:
    message_text = message.text
    if message_text is None:
        return ''
    for _, text in sorted(message.parse_entities([MessageEntity.BOT_COMMAND]).items(), key=(lambda item: item[0].offset)):
        message_text = message_text.replace(text, '').strip()
    return message_text if len(message_text) > 0 else ''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_allowed(update, context):
            logging.warning(f'User {update.message.from_user.name} (id: {update.message.from_user.id}) '
                f'is not allowed to reset the conversation')
            await self.send_disallowed_message(update, context)
            return

        logging.info(f'Resetting the conversation for user {update.message.from_user.name} '
            f'(id: {update.message.from_user.id})...')

        chat_id = update.effective_chat.id
        reset_content = message_text(update.message)
        self.openai.reset_chat_history(chat_id=chat_id, content=reset_content)
        await context.bot.send_message(chat_id=chat_id, text='Done!')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = request_chat_gpt(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
    application = ApplicationBuilder().token("6535941946:AAFkn48yUIyDFuqr02ufla_TvhJemD-mbhc").build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
