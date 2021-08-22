import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import lyrics_data as lyric

bot = telebot.TeleBot('', parse_mode='MARKDOWN')

states = {
    'answer': '',
    'game_state': False,
    'song_text' : None,
    'hints_count': 3
}

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Подсказка', callback_data='take_hint'))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'take_hint':
        if states['song_text'] != None:
            if states['hints_count'] > 0:

                text = ''
                if len(states['song_text'])-3 > 0:
                    to_rand = len(states['song_text'])-3
                else:
                    to_rand = 0
                try:
                    num = random.randint(0, to_rand)
                except:
                    num = 0
                for i in range(2):
                    text += states['song_text'][num]
                    num+=1
                    
                states['hints_count'] -= 1
                hint_text = 'Осталось ' + str(states['hints_count']) + ' подсказки'
                bot.answer_callback_query(call.id, hint_text)
                bot.send_message(call.message.chat.id, 'Мы тут ещё черканули, зацени)')
                bot.send_message(call.message.chat.id, text)
            else:
                bot.answer_callback_query(call.id, 'Попытки закончились')
        else:
            bot.answer_callback_query(call.id, 'Промахнулся чел')
    else:
        pass
@bot.message_handler(commands=['names'])
def get_songs_names(message):
    with open('songs_names.md', 'r') as file:
        names = file.read()
        bot.send_message(message.chat.id, names)


@bot.message_handler(commands=['start_game'])
def send_text(message, states=states):
    if states['game_state']:
        bot.send_message(message.chat.id, 'Сорян братан ты уже думаешь над одним названием. Либо думай, либо думай над другим [/stop_game](/stop_game)')
    else:
        introduction = 'ООО здорова мужик(или нет) спс, что заглянул. Хотим выслушать твоё мнение на счёт этого отрывка. Ну что как назовёшь?¿!'
        states['answer'] = ''
        states['game_state'] = True
        song = lyric.song()
        states['song_text'] = song['song_text']
        
        text = ''
        if len(song['song_text'])-7 < 0:
            to_rand = 0
        else:
            to_rand = len(song['song_text'])-7
        try:
            num = random.randint(0, to_rand)
        except:
            num = 0
        for i in range(6):
            text += song['song_text'][num]
            num+=1
    
        states['answer'] = song['song_name'].rstrip()

        bot.send_message(message.chat.id, introduction)    
        bot.send_message(message.chat.id, text, reply_markup=gen_markup(), parse_mode=None)

@bot.message_handler(commands=['stop_game'])
def stop(message, states=states):
    if states['game_state']:
        denied = 'Ладно мы сами придумаем. Зря группу создавали что ли\nПока на примете название \n' + states['answer']
        states['answer'] = ''
        states['game_state'] = False
        states['song_text'] = None
        states['hints_count'] = 3
        bot.send_message(message.chat.id, denied)
    else:
        bot.send_message(message.chat.id, 'Мы ещё не давали тебе текст фан)')


@bot.message_handler(commands=['start'])
def hello(message):
    letter = """Привет! Мы известная группа bring me the horizon, и у нас есть просьба для тебя фанат: мы никак не можем назвать свою новую песню. Можем скинуть тебе отрывок звякни пж))
[/start_game](/start_game) для начала игры
для ответа напишите **+Название песни**
"""
    bot.send_message(message.chat.id, letter)

@bot.message_handler(regexp='^\+.*$')
def guess(message):
    if states['game_state'] == True:
        user_input = message.text.strip().removeprefix('+')
        answer = states['answer']
        values = (user_input.title(), user_input.capitalize(), user_input.upper(), user_input.lower())
        print(user_input)
        if answer in values:
            states['answer'] = ''
            states['game_state'] = False
            states['hints_count'] = 3
            states['song_text'] = None
            bot.reply_to(message, 'Мы думаем это название подойдёт. Спасибо фан')
            
        else:
            bot.send_message(message.chat.id, 'Нам кажется это название не подходит')
    else:
        pass

bot.polling(none_stop=True)
