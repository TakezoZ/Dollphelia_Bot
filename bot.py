from cgitb import text
from email import message
from importlib.metadata import entry_points
from tkinter import Entry
from telegram import Chat, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                        RegexHandler, ConversationHandler)

STATE1 = 1
STATE2 = 2


def welcome(update, context):
    message = 'Olá ' + update.message.from_user.first_name + '!'
    print(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def feedback(update, context):
    message = 'por favor, digite um feedback para o nosso tutorial:'
    update.message.reply_text(message, ReplyKeyboardMarkup([], one_time_keyboard=True))
    return STATE1




def main():
    token = '5457378367:AAGZp1NcmkLPnfR5KIDpwfWfYnfM9T2kR2Y'
    updater = Updater(token=token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', welcome))
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('feedback', feedback)],
        states={
            STATE1: [MessageHandler(Filters.text, inputFeedback)],
            STATE2: [MessageHandler(Filters.text, inputFeedback2)]
        },
        fallbacks=[CommandHandler('cancel', cancel)])
    updater.dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    print(str(updater))
    updater.idle()


if __name__ == "__main__":
    main()
    

def inputFeedback(update, context):
    feedback = update.message.text
    print(feedback)
    if len(feedback) < 10:
        message = """Seu feedback foi muito curtinho... 
                        \nInforma mais pra gente, por favor?"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return STATE1
    else:
        message = "Muito obrigada pelo seu feedback!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        
        
def inputFeedback2(update, context):
    feedback = update.message.text
    message = "Muito obrigada pelo seu feedback!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    
def cancel(update, context):
        return ConversationHandler.END
