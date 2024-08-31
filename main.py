import telebot
from telebot import types
import random

TOKEN=
bot = telebot.TeleBot(TOKEN)
users = {}


class Results:
    WIN = "WIN"
    LOSS = "LOSS"
    DRAW = "DRAW"


def pull(cur_id):
    if cur_id in users:
        card = random.randint(1, 9)
        users[cur_id][1].append(card)
        users[cur_id][3] += card
        text = (f"Вы вытянули {card}\n"
                f"Ваши карты: {' '.join(map(str, users[cur_id][1]))}\n"
                f"--------------------\n"
                f"Сумма: {users[cur_id][3]}")
        bot.send_message(cur_id, text)

        if users[cur_id][3] > 21:
            return Results.LOSS
        elif users[cur_id][3] == 21:
            return Results.WIN
        show(cur_id, "Продолжить?")
    else:
        bot.send_message(cur_id, "Вы еще не начали игру!")


def stop(cur_id):
    if cur_id in users:
        bot.send_message(cur_id, f"Карты дилера: {' '.join(map(str, users[cur_id][0]))}")

        while True:
            card = random.randint(1, 9)
            users[cur_id][0].append(card)
            users[cur_id][2] += card
            text = (f"Дилер вытянул {card}\n"
                    f"Карты дилера: {' '.join(map(str, users[cur_id][0]))}\n"
                    f"--------------------\n"
                    f"Сумма: {users[cur_id][2]}")
            bot.send_message(cur_id, text)

            if users[cur_id][2] > 21:
                return Results.WIN
            elif users[cur_id][2] > users[cur_id][3]:
                return Results.LOSS
            elif users[cur_id][2] == users[cur_id][3]:
                return Results.DRAW
    else:
        bot.send_message(cur_id, "Вы еще не начали игру!")


def show(cur_id, text):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Вытянуть карту", callback_data="pull")
    btn2 = types.InlineKeyboardButton("Пасс", callback_data="pass")
    markup.row(btn1, btn2)
    bot.send_message(cur_id, text, reply_markup=markup)


@bot.message_handler(commands=["start", "help"])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("/game"))
    markup.add(types.KeyboardButton("/rules"))
    markup.add(types.KeyboardButton("/help"))
    bot.send_message(message.chat.id, "Привет, я бот-дилер своеобразной версии игры БлэкДжек.\n"
                                      "Мои команды:\n"
                                      "/help - общая информация о боте\n"
                                      "/rules - правила игры\n"
                                      "/game - начать игру\n", reply_markup=markup)


@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.chat.id,
                     "Правила игры:\n"
                     "Цель игры: набрать из карт количество очков 21 или же больше, чем дилер\n"
                     "Этапы:\n"
                     "1. Дилер раздает себе и игроку по 2 карты. Из карт дилера игроку видна только 1\n"
                     "2. Игрок может либо вытянуть еще карту, либо остановиться."
                     "Если игрок наберет количество очков больше, чем 21, то проиграет\n"
                     "3. Если у игрока количество очков меньше 21, то начинает тянуть карты дилер до тех пор, "
                     "пока не наберет очков больше, чем игрок, либо же выйдет за 21")


@bot.message_handler(commands=["game"])
def game(message):
    random.seed()
    list1 = [random.randint(1, 11), random.randint(1, 9)]
    list2 = [random.randint(1, 11), random.randint(1, 9)]
    sum1 = sum(list1)
    sum2 = sum(list2)
    cur_id = message.chat.id
    users[cur_id] = [list1, list2, sum1, sum2]

    text = (f"Карты дилера: ? {list1[1]}\n\n"
            f"Ваши карты: {list2[0]} {list2[1]}\n"
            f"--------------------\n"
            f"Сумма: {sum2}")
    show(cur_id, text)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    cur_id = callback.message.chat.id
    res = Results.DRAW
    if callback.data == "pull":
        res = pull(cur_id)
    elif callback.data == "pass":
        res = stop(cur_id)

    if res == Results.WIN:
        bot.send_message(cur_id, "Вы победили")
        users.pop(cur_id)
    elif res == Results.LOSS:
        bot.send_message(cur_id, "Вы проиграли")
        users.pop(cur_id)
    elif res == Results.DRAW:
        bot.send_message(cur_id, "Ничья")
        users.pop(cur_id)


@bot.message_handler()
def default(message):
    if message.text == "Саша":
        bot.reply_to(message, "Мой создатель очень любит девушку с этим именем")
    else:
        bot.reply_to(message, "Я вас не понимаю")


bot.polling(none_stop=True)
