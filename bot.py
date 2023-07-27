from funcs import *

bot = telebot.TeleBot(token=token)
db = {}


def get_goroscope(message):
    '''
    api call to get goroscope. send message to user
    :param message:
    :return:
    '''
    try:
        s = get_zodiac_sign(message.text)
        r = requests.post(f'https://ohmanda.com/api/horoscope/{s}')
        result = translate_text(r.json()['horoscope'])
        bot.send_message(message.chat.id, result)

    except Exception as ex:
        bot.send_message(message.chat.id, 'что-то пошло не так, сорьки')
        print(ex)


@bot.message_handler(commands=['start'])
def start(message):
    '''
    function that handle comand /start
    :param message:
    :return:
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('аркан дня🪐')
    item2 = types.KeyboardButton('число дня🪷')
    item3 = types.KeyboardButton('цвет дня🧚🏻‍♂️')
    item4 = types.KeyboardButton('расклад🦋')
    item5 = types.KeyboardButton('гороскоп на сегодня💫')
    item6 = types.KeyboardButton('другое...')

    markup.add(item1, item2, item3, item4, item5, item6)
    text = '✨приветствую тебя, {0.first_name}!✨'
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)


def process_rasclad(message):
    '''
    a function for creating a tarot layout. the function uses the call to openair api. an api key is required
    :param message:
    :return:
    '''
    question = message.text
    temp_daycard, temp_daycard2, temp_daycard3 = random.sample(range(0, 21), 3)
    path = r'C:\Users\red1c\OneDrive\Рабочий стол\taro_bot-master\cards\card'
    with open(path + str(temp_daycard) + '.jpeg',
              'rb') as img:
        bot.send_photo(message.chat.id, img, caption=card_desc[temp_daycard])
    with open(path + str(temp_daycard2) + '.jpeg',
              'rb') as img2:
        bot.send_photo(message.chat.id, img2, caption=card_desc[temp_daycard2])
    with open(path + str(temp_daycard3) + '.jpeg',
              'rb') as img3:
        bot.send_photo(message.chat.id, img3, caption=card_desc[temp_daycard3])
    bot.send_message(message.chat.id, get_tarot_reading(question=f'вопрос: {question} напиши расклад '
                                                                 f' по картам и вопросу',
                                                        cards=f'перая выпавшая карта: {card_desc[temp_daycard]}\
                                                         вторая выпавшая карта: {card_desc[temp_daycard2]} \
                                                         третья выпавшая карта: {card_desc[temp_daycard3]}'))


@bot.message_handler(content_types=['text'])
def bot_message(message):
    '''
    function that handle text messages
    :param message:
    :return:
    '''
    try:
        if message.chat.type == 'private':
            if not message.chat.id in db:
                db[message.chat.id] = {'temp_daynum': None,
                                       'temp_daycard': None,
                                       'temp_color': None}
            if message.text == 'число дня🪷':
                if not db[message.chat.id]['temp_daynum'] is None:
                    bot.send_message(message.chat.id, 'ваше число дня: ' + str(db[message.chat.id]['temp_daynum']))
                    print('число дня не none')
                else:
                    temp_daynum = random.randint(1, 77)
                    db[message.chat.id]['temp_daynum'] = temp_daynum
                    bot.send_message(message.chat.id, 'ваше число дня: ' + str(temp_daynum))
            elif message.text == 'аркан дня🪐':
                if not db[message.chat.id]['temp_daycard'] is None:
                    temp_daycard = db[message.chat.id]['temp_daycard']
                    text_for_openai = db[message.chat.id]["text_for_openai"]
                    print('аркан дня не None')
                else:
                    temp_daycard = random.randint(0, 20)
                    db[message.chat.id]['temp_daycard'] = temp_daycard
                    text_for_openai = get_tarot_reading(question='напиши описание аркана дня по карте',
                                                cards=card_desc[temp_daycard])
                    db[message.chat.id]["text_for_openai"] = text_for_openai
                bot.send_message(message.chat.id, 'ваш аркан дня: ' + str(temp_daycard))
                db[message.chat.id]['temp_daycard'] = temp_daycard
                bot.send_message(message.chat.id, 'описание вашего аркана дня: \n')
                img = open(
                    path + str(temp_daycard) + '.jpeg', 'rb'
                )
                bot.send_photo(message.chat.id, img,)
                bot.send_message(message.chat.id, text_for_openai)
            elif message.text[:8] == 'цвет дня':
                if not db[message.chat.id]['temp_color'] is None:
                    bot.send_message(message.chat.id, 'ваш цвет дня: ' + str(db[message.chat.id]['temp_color']))
                else:
                    temp_color = random.choice(colors_array)
                    db[message.chat.id]['temp_color'] = temp_color
                    bot.send_message(message.chat.id, 'ваш цвет дня: ' + str(temp_color))
            elif message.text == 'гороскоп на сегодня💫':
                bot.send_message(message.chat.id, 'когда вы родились?\n отправляй в формате DD:MM:YYYY')
                bot.register_next_step_handler(message, get_goroscope)
            elif message.text == 'другое...':
                bot.send_message(message.chat.id,
                                 'я начинающий маг, поэтому другие возможности покажу позже...\nнажмите /start и '
                                 'попробуйте снова')
            elif message.text == 'расклад🦋':
                bot.send_message(message.chat.id,
                                 'какой запрос в космос, во вселенную вы хотите отправить?')
                bot.register_next_step_handler(message, process_rasclad)
            else:
                bot.send_message(message.chat.id,
                                 'проводя различные манипуляции с магией, я перестал вас понимать,\nнажмите /start и '
                                 'попробуйте снова')

    except Exception as ex:
        print(ex)


bot.polling(none_stop=True)
