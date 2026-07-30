import telebot
import requests
from datetime import datetime

TOKEN = "8779938611:AAHN9kUZoSNsa7SMQRMv4BUF04k2yA0PnKU"
bot = telebot.TeleBot(TOKEN)
SERVER_URL = "http://127.0.0.1:5000"






@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    text = """Привет! я бот для заказов.

Доступные команды:
/add <> - добавить ордер
/items - посмротреть предметы
/delete <id> - удалить предмет"""

    bot.reply_to(message, text)
@bot.message_handler(commands=['add'])
def add(message):
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "введите все данные")
            return
        try:
            user_id = int(parts[1])
            cost = float(parts[2])
        except ValueError:
            bot.reply_to(message, "введите пользователя и цену в числах")
            return
        data = {
            "user_id": user_id,
            "cost": cost,
            "renewal_date": parts[3],
            "name": parts[4],
        }
        response = requests.post(SERVER_URL + "/subscribe", json=data)
        if response.status_code == 200:
            bot.reply_to(message, "success")
        else:
            bot.reply_to(message, "error")
            return
    except Exception as e:
        bot.reply_to(message, str(e))
        return

@bot.message_handler(commands=['list'])
def list(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "введите id")
            return
        try:
            user_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "введите число")
            return
        response = requests.get(SERVER_URL + f"/subscribe/{user_id}")
        if response.status_code == 200:
            data = response.json()
            list = data.get('result')
            if not list:
                bot.reply_to(message, "нету подписок")
                return
            for item in list:
                text = f"id : {item['id']}\n cost : {item['cost']}\n renewal_date : {item['renewal_date']}\n name : {item['name']}\n"
                bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, str(e))
        return

@bot.message_handler(commands=['expiring'])
def expiring(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "введите id")
            return
        try:
            user_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "введите число")
            return
        response = requests.get(SERVER_URL + f"/subscribe/{user_id}/expiring")
        if response.status_code == 200:
            data = response.json()
            sub = data.get('result')
            if not sub:
                bot.reply_to(message, "нету подписок")
                return
            text = f"список подписок\n"
            for s in sub:
                text += f"id : {s['id']}\n cost: {s['cost']}\n renewal_date: {s['renewal_date']}\n name: {s['name']}\n days_left: {s['days_left']}\n"
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, str(e))
        return

@bot.message_handler(commands=['renew'])
def renew(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "введите id")
            return
        try:
            user_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "введите число")
            return
        data = {"renewal_date": parts[2]}
        response = requests.put(SERVER_URL + f"/subscribe/{user_id}", json=data)
        if response.status_code == 200:
            bot.reply_to(message, "success")
    except Exception as e:
        bot.reply_to(message, str(e))
        return




bot.infinity_polling()