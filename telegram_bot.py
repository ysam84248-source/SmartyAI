import telebot
import json

BOT_TOKEN = '8431067819:AAFyTy-Rww700QgUlbyRUa75Ttivw6tlq0E'
ORDERS_FILE = 'orders.json'

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# Save order to JSON
def save_order(order):
    try:
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
    except:
        orders = []

    orders.append(order)
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

# START command
@bot.message_handler(commands=['start', 'order'])
def start_order(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "👋 Welcome to *SmartyAI Anime Plaza!*\nWhat's your name?", parse_mode="Markdown")

# Step 1: Get Name
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) is not None and 'name' not in user_data[msg.chat.id])
def get_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text
    bot.send_message(user_id, "🧸 Which *anime product* would you like to order?", parse_mode="Markdown")

# Step 2: Get Product
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) is not None and 'product' not in user_data[msg.chat.id])
def get_product(message):
    user_id = message.chat.id
    user_data[user_id]['product'] = message.text
    bot.send_message(user_id, "🏠 Please enter your *delivery address*.", parse_mode="Markdown")

# Step 3: Get Address
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) is not None and 'address' not in user_data[msg.chat.id])
def get_address(message):
    user_id = message.chat.id
    user_data[user_id]['address'] = message.text
    bot.send_message(user_id, "💳 What's your *payment method*? (e.g., UPI, COD)", parse_mode="Markdown")

# Step 4: Get Payment and Confirm Order
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) is not None and 'payment' not in user_data[msg.chat.id])
def get_payment(message):
    user_id = message.chat.id
    user_data[user_id]['payment'] = message.text

    order = {
        "name": user_data[user_id]['name'],
        "product": user_data[user_id]['product'],
        "address": user_data[user_id]['address'],
        "payment": user_data[user_id]['payment'],
        "status": "Pending"
    }

    save_order(order)

    summary = (
        f"✅ *Order Received!*\n\n"
        f"👤 Name: {order['name']}\n"
        f"🧸 Product: {order['product']}\n"
        f"🏠 Address: {order['address']}\n"
        f"💳 Payment: {order['payment']}\n"
        f"📦 Status: {order['status']}"
    )

    bot.send_message(user_id, summary, parse_mode="Markdown")
    user_data.pop(user_id, None)

# Start bot
if __name__ == '__main__':
    print("🤖 Telegram bot is running...")
    bot.polling(none_stop=True)
    