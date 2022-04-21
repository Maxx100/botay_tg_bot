import telebot
from telebot import types
from random import randint
import datetime
from threading import Thread
from time import sleep

bot = telebot.TeleBot("")

"""menu = types.InlineKeyboardMarkup(row_width=3)
menu.add(
    types.InlineKeyboardButton(text='Hi!', callback_data='b1'),
    types.InlineKeyboardButton(text='Hello!', callback_data='b2')
)"""

users = {}
# tg-name: chat_id, score, <cmd?>
# cmd: 0 - None; 1 - Add push; 2 - Add points
push = {}
# date: text
id_group = -626030913


def data_import():
    with open("friends_rating.txt", "r") as f:
        for i in f.readlines():
            temp = i.split("\t")
            users[temp[0]] = [int(temp[1]), int(temp[2]), 0]
    with open("push.txt", "r", encoding="windows-1251") as f:
        for i in f.readlines():
            temp = i.split("\t")
            push[temp[0]] = temp[1]


def data_export():
    with open("friends_rating.txt", "w") as f:
        for i in users:
            f.write("{}\t{}\t{}\n".format(i, str(users[i][0]), str(users[i][1])))
    with open("push.txt", "w", encoding="windows-1251") as f:
        for i in push:
            f.write("{}\t{}\n".format(i, push[i]))


def phrase(cmd):
    base = {"menu": ["Что хочешь сделать?", "Куда теперь?", "Хорошо, идем дальше?"],
            "events": ["Смотри", "Что нас ожидает?", "Надеюсь, мы скоро пойдем спать"],
            "happy_s": ["CAACAgIAAxkBAAED5R5iBoS-V7KB_A_lZTb-ohopWQO-5AACHBAAAp5LaEpUW_Ve1AH_GiME",
                        "CAACAgIAAxkBAAED5SBiBoTMdA_CDvP09acDS_lBTRQraQACFhQAAiA6aUqQMnQOK8d-8iME",
                        "CAACAgIAAxkBAAED5SZiBoTXRkmrCw14ZcyotVryhpA7VgACKRYAAlZLMUhifRFGFW4tECME"],
            "sad_s": ["CAACAgIAAxkBAAED5SJiBoTRO_g12E-dgjNjyyQSRTu_egACXRcAAjcKKUheApuB32IDOCME"],
            "botay_s": ["CAACAgIAAxkBAAED5RxiBoSlFM7s-DmcKxOWWT4v24QwYQAC1RUAAhwmGUsXZXAzSwHxSyME",
                        "CAACAgIAAxkBAAED5SRiBoTUMh-i9GC1hC1LivXBD1bwWAACLREAAtAuIEuBrmFZA0alEiME"]}
    return base[cmd][randint(0, len(base[cmd]) - 1)]


def back_button(text, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Назад")
    markup.add(item)
    bot.send_message(chat_id, text, reply_markup=markup)


def mark(color):
    if color == "green":
        return "\033[42mLOG\033[0m   "
    elif color == "yellow":
        return "\033[43mLOG\033[0m   "
    elif color == "red":
        return "\033[41mLOG\033[0m   "


def push_check(chat):
    while True:
        today = datetime.date.today()
        for i in push.copy():
            if list(map(int, i.split("."))) == [today.day, today.month, today.year]:
                bot.send_message(chat, "Напоминание: " + push[i])
                del push[i]
        data_export()
        sleep(60 * 60 * 5)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')
    if message.from_user.username == "None":
        bot.send_message(message.chat.id, 'У тебя нет имени TG, проверь настройки!')
    else:
        if message.from_user.username not in users:
            print(mark("green") + "Новый пользователь:", message.chat.id, message.from_user.username)
            users[message.from_user.username] = [message.chat.id, 0, False]
            data_export()
        main(message)


@bot.message_handler(commands=['back'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рейтинг участников")
    markup.add(item1)
    item2 = types.KeyboardButton("Правила")
    markup.add(item2)
    item3 = types.KeyboardButton("Просмотр мероприятий")
    markup.add(item3)
    item4 = types.KeyboardButton("Добавить уведомление")
    markup.add(item4)
    item5 = types.KeyboardButton("Добавить очки")
    markup.add(item5)
    bot.send_message(message.chat.id, phrase("menu"), reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Рейтинг участников":
        ans = ""
        temp = []
        for i in users:
            temp.append([i, users[i][1]])
        temp.sort(key=lambda x: x[1], reverse=True)
        for i in temp:
            ans += i[0] + " - " + str(i[1]) + "\n"
        bot.send_message(message.chat.id, ans)
        main(message)
    elif message.text == "Правила":
        bot.send_message(message.chat.id, "Плохое не делай, а хорошее делай")
        bot.send_message(message.chat.id, "Перед тем, как добавить себе очки, необходимо написать, за что они")
        bot.send_message(message.chat.id, "Всё основывается на честной игре")
        bot.send_sticker(id_group, phrase("happy_s"))
    elif message.text == "Просмотр мероприятий":
        bot.send_message(message.chat.id, (phrase("events")))
        temp = ""
        for i in push:
            temp += str(i) + ": " + push[i] + "\n"
        if temp:
            bot.send_message(message.chat.id, temp)
        else:
            bot.send_message(message.chat.id, "Ничего...")
        main(message)
    elif message.text == "Добавить уведомление":
        users[message.from_user.username][2] = 1
        back_button("Отправь дату и сообщение, я тебе напомню\n(11.02.2022 Мой день рождения)", message.chat.id)
    elif message.text == "Назад":
        main(message)
    elif message.text == "Добавить очки":
        users[message.from_user.username][2] = 2
        back_button("Сколько?", message.chat.id)
    else:
        if users[message.from_user.username][2] == 1:
            print(mark("green") + "New push!")
            temp = message.text.split()
            if temp[0] in push:
                push[temp[0]] += " | " + " ".join(temp[1:])
            else:
                push[temp[0]] = " ".join(temp[1:])
            data_export()
            main(message)
        elif users[message.from_user.username][2] == 2:
            users[message.from_user.username][1] += int(message.text)
            data_export()
            main(message)
        users[message.from_user.username][2] = 0


if __name__ == "__main__":
    print(mark("yellow") + "Data importing...", end=" ")
    data_import()
    print("Completed")
    print(mark("yellow") + "Starting new process (push checker)...", end=" ")
    push_checking = Thread(target=push_check, args=(id_group,))
    push_checking.start()
    print("Completed")
    print(mark("yellow") + "Bot online!")
    bot.infinity_polling()
