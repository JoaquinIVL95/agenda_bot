import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import datetime

# Configuración del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Diccionario para almacenar los recordatorios
reminders = {}

# Función de inicio
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu asistente personal. Usa /add para añadir un recordatorio.')

# Función para añadir recordatorios
def add(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        # Comando /add debe ir seguido por la fecha y hora del recordatorio y el mensaje
        datetime_str = context.args[0] + ' ' + context.args[1]
        message = ' '.join(context.args[2:])
        reminder_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        # Agregar recordatorio
        scheduler.add_job(send_reminder, DateTrigger(reminder_time), args=[chat_id, message])
        update.message.reply_text(f'Recordatorio añadido para {reminder_time}.')
    except (IndexError, ValueError):
        update.message.reply_text('Uso: /add <YYYY-MM-DD> <HH:MM> <mensaje>')

# Función para enviar recordatorios
def send_reminder(chat_id, message):
    context.bot.send_message(chat_id=chat_id, text=f'Recordatorio: {message}')

def main() -> None:
    # Token de tu bot
    token = '6725148398:AAG6Cgwkw66ynlQMGJywKFfhJxQPEe8H3-k'
    
    # Inicializar Updater y Dispatcher
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Inicializar Scheduler
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Registrar comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
