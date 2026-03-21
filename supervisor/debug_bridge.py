# debug_bridge.py
# Temporary script to bridge messages from architect bot to main chat for debugging
# This will be removed once the main handler is properly configured

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import logging
import os

# Configure logging
telebot_logger = logging.getLogger('telegram')
telebot_logger.setLevel(logging.DEBUG)

async def bridge_message(update: Update, context: CallbackContext) -> None:
    """
    Handle incoming messages from architect bot and mirror them to the owner chat.
    """
    try:
        # Get message data
        message = update.effective_message
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id if update.effective_user else 'unknown'
        
        # Create debug message with message details
        debug_msg = f"""
🔧 DEBUG BRIDGE: Received message from architect bot

Chat ID: {chat_id}
User ID: {user_id}
Message ID: {message.message_id}
Text: {message.text or '[no text]'}
Date: {message.date}

Raw update object:
{update.to_dict()}
        """
        
        # Send to owner chat (your chat)
        owner_chat_id = int(os.getenv('OWNER_CHAT_ID', '89033877'))
        await context.bot.send_message(
            chat_id=owner_chat_id,
            text=debug_msg
        )
        
        # Log receipt
        logging.info(f"Bridged message from {chat_id}: {message.text}")
        
    except Exception as e:
        error_msg = f"Error in debug bridge: {str(e)}"
        logging.error(error_msg)
        # Still try to notify owner
        try:
            owner_chat_id = int(os.getenv('OWNER_CHAT_ID', '89033877'))
            await context.bot.send_message(
                chat_id=owner_chat_id,
                text=error_msg
            )
        except:
            pass

# Application setup function (called by supervisor)
def create_bridge_app() -> Application:
    """
    Create and configure the bridge application.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN_ARCHITECT')
    if not token:
        raise ValueError('TELEGRAM_BOT_TOKEN_ARCHITECT is not set')
        
    application = Application.builder().token(token).build()
    
    # Add handler for all messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bridge_message))
    application.add_handler(MessageHandler(filters.COMMAND, bridge_message))
    
    return application