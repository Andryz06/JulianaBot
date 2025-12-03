import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

# --- TRUCO PARA ENCONTRAR EL .ENV ---
# Obtenemos la ruta exacta donde está guardado este script
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_env = os.path.join(directorio_script, '.env')

# Cargamos el archivo .env especificando la ruta exacta
load_dotenv(ruta_env)

# Verificamos si los encontró (esto te ayudará a ver qué pasa)
print(f"Buscando .env en: {ruta_env}")
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('GEMINI_API_KEY')

if not TOKEN or not API_KEY:
    print(" ERROR CRÍTICO: Sigo sin encontrar las claves.")
    print("Asegúrate de que el archivo se llame exactamente '.env' y no '.env.txt'")
    exit() # Detener el programa para no dar más errores
else:
    print("✅ Claves encontradas. Iniciando Juliana...")

# Asignamos las variables
TELEGRAM_TOKEN = TOKEN
GEMINI_API_KEY = API_KEY
# --- CONFIGURACIÓN DE JULIANA (GEMINI) ---
genai.configure(api_key=GEMINI_API_KEY)

#  personalidad de Juliana
instrucciones_juliana = (
    "Eres Juliana, una asistente personal útil, amigable y muy eficiente. "
    "Tu misión es ayudar al usuario a organizar su día, responder dudas y charlar. "
    "Responde siempre de forma concisa y con un tono cálido."
)

# iniciar el modelo con gemini-2.5-flash
model = genai.GenerativeModel(
    'gemini-2.5-flash',
      system_instruction=instrucciones_juliana)

# Iniciar  chat ( memoria a corto plazo)
chat_session = model.start_chat(history=[])

# Conectamos con Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    bot.reply_to(message, "¡Hola! Soy Juliana. 🌸 Estoy lista para ayudarte con lo que necesites hoy.")

@bot.message_handler(func=lambda message: True)
def responder_mensaje(message):
    print(f"Usuario dice: {message.text}") # Esto te ayuda a ver qué pasa en la consola
    
    try:
        # Enviamos el mensaje a Gemini
        response = chat_session.send_message(message.text)
        
        # Enviamos la respuesta de vuelta a Telegram
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, "Lo siento, me he quedado en blanco un momento. ¿Puedes repetirlo?")
        print(f"Error: {e}")

# --- ENCENDER EL BOT ---
print(">>> Juliana está despierta y escuchando...")
bot.infinity_polling()