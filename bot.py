import telebot;

TOKEN = '2101999977:AAEKiEsmjTbJmrruJmh1FRkQmsYoi8UPcko'
bot = telebot.TeleBot(TOKEN)
covid_list = ['covid', 'корона', 'ковид', 'вакцина', 'corona']

data_base = {}
name_base = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    data_base[message.chat.id] = {}
    bot.send_message(message.chat.id, "Приветик, я буду следить за активностью коронавируса в этом чате " + u'\U0001F637')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "/stats - Статистика пользователей сообщений")

@bot.message_handler(commands=['vaccine'])
def send_vaccine(message):
    bot.send_message(message.chat.id, u'\U0001F489')

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if data_base[message.chat.id] == {}:
        bot.send_message(message.chat.id, "Пока никто не интересовался коронавирусной инфекцией")
    else:
        Message = ''
        for i in data_base[message.chat.id]:
            Message += 'ID: ' + str(i) + ' Имя: ' + name_base[i] + '\nКол-во запросов: ' + str(data_base[message.chat.id][i]) + '\n'
        bot.send_message(message.chat.id, Message)

@bot.message_handler(content_types=['text'])
def get_message(message):

    res = -1
    list_text = message.text.split()
    for i in list_text:
        for j in covid_list:
            res = i.lower().find(j)
            if res != -1:
               bot.reply_to(message, "Интересуетесь коронавирусом?")
               ID = message.from_user.id
               Name = ''
               if message.from_user.first_name is not None:
                   Name += message.from_user.first_name + ' '
               if ID in data_base[message.chat.id]:
                   data_base[message.chat.id][ID] += 1
               else:
                   data_base[message.chat.id][ID] = 1
                   name_base[ID] = Name

@bot.my_chat_member_handler()
def get_message_update(message):
    new_chat = message.new_chat_member
    if new_chat.status == "left":
        del data_base[message.chat.id]
        print("delete bot from chat is successful")

bot.polling(none_stop=True, interval=0)