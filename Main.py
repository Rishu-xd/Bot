import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace 'YOUR_BOT_API_TOKEN' with your bot's API token
API_TOKEN = '7160413938:AAGT0KjtuV9727c0sdBgFxCwE2cdELJsBVs'
bot = telebot.TeleBot(API_TOKEN)

# To store user data
user_data = {}

# To track user actions
user_states = {}

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = {"action": None}  # Reset user action

    # Create inline buttons for Login and Register
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Login", callback_data="login"),
        InlineKeyboardButton("Register", callback_data="register")
    )

    bot.send_message(
        chat_id,
        "Welcome! Please choose an option:",
        reply_markup=markup
    )

# Callback handler for button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "register":
        user_states[chat_id]["action"] = "register_username"
        bot.send_message(chat_id, "Enter a username to register:")
    elif call.data == "login":
        user_states[chat_id]["action"] = "login_username"
        bot.send_message(chat_id, "Enter your username to login:")

# Handle user input for login and registration
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get("action") is not None)
def handle_user_input(message):
    chat_id = message.chat.id
    action = user_states[chat_id]["action"]

    if action == "register_username":
        username = message.text
        if username in user_data:
            bot.send_message(chat_id, "Username already registered. Try a different one.")
        else:
            user_states[chat_id]["temp_username"] = username
            user_states[chat_id]["action"] = "register_password"
            bot.send_message(chat_id, "Username is available! Now enter a password:")

    elif action == "register_password":
        password = message.text
        username = user_states[chat_id].pop("temp_username")
        user_data[username] = {"password": password}
        user_states[chat_id]["action"] = None
        bot.send_message(chat_id, "Registration successful! You can now login.")

    elif action == "login_username":
        username = message.text
        if username in user_data:
            user_states[chat_id]["temp_username"] = username
            user_states[chat_id]["action"] = "login_password"
            bot.send_message(chat_id, "Username found! Enter your password:")
        else:
            bot.send_message(chat_id, "Username not registered. Please register first.")
            user_states[chat_id]["action"] = None

    elif action == "login_password":
        password = message.text
        username = user_states[chat_id].pop("temp_username")
        if user_data[username]["password"] == password:
            user_states[chat_id]["action"] = None
            bot.send_message(chat_id, "Login successful! Here are your links:")
            send_links(chat_id)
        else:
            bot.send_message(chat_id, "Incorrect password. Please try again.")
            user_states[chat_id]["action"] = None

# Function to send links after successful login
def send_links(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2  # Number of buttons per row
    markup.add(
        InlineKeyboardButton("Google", url="https://www.google.com"),
        InlineKeyboardButton("YouTube", url="https://www.youtube.com"),
        InlineKeyboardButton("GitHub", url="https://github.com"),
        InlineKeyboardButton("Telegram", url="https://telegram.org")
    )
    bot.send_message(
        chat_id,
        "Click any of the links below:",
        reply_markup=markup
    )

# Polling to keep the bot running
print("Bot is running...")
bot.infinity_polling()
