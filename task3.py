import telebot
import random

token = 'my_token'
bot = telebot.TeleBot(token)
lives = 10
letter = ''
word_variants = ['banana', 'apple', 'peach', 'apricot', 'pineapple', 'avocado', 'mango',
                 'coconut', 'cherry', 'lemon', 'lime', 'grape', 'orange', 'pear', 'watermelon']
word_right = ''
word_in_game = ''


@bot.message_handler(commands=['help'])
def help_com(message):
    bot.send_message(message.chat.id, 'If you want to play the game, enter /start')


@bot.message_handler(commands=['start'])
def start_conv(message):
    sent = bot.send_message(message, "Hi there!\nWhat's your name?")
    bot.register_next_step_handler(sent, start_game)


def start_game(message):
    global lives, word_right, word_in_game, word_variants, letter
    try:
        chat_id = message.chat.id
    except Exception:
        bot.reply_to(message, 'oooops')
    bot.send_message(chat_id, 'Nice to meet you ' + message.text)
    word_right = random.choice(word_variants)
    word_in_game = '*' * len(word_right)
    bot.send_message(message.chat.id, 'Let\'s play with me!')
    bot.send_message(message.chat.id,
                     'You have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))
    bot.send_message(message.from_user.id, 'Enter one character!')
    bot.register_next_step_handler(message, start_alg)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def start_alg(message):
    global lives, word_right, word_in_game, word_variants, letter
    letter = message.text.lower()
    while '*' in word_in_game and lives > 0:
        bot.send_message(message.chat.id,
                         'You have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))
        if letter in word_right:
            index = -1
            while word_in_game.count(letter) != word_right.count(letter):
                index = word_right.find(letter, index + 1)
                word_in_game = word_in_game[:index] + letter + word_in_game[index + 1:]
        else:
            lives -= 1
            bot.send_message(message.chat.id, 'There is no such letter in the word! You lost 1 live!')
            bot.send_message(message.chat.id, 'You have {live} lives'.format(live=lives))
    if lives <= 0:
        bot.send_message(message.chat.id, 'Unfortunately, you are lost all your lives!\nOur word was {in_word}'.format(
            in_word=word_right))
        msg = bot.send_message(message.from_user.id, 'If you want to play again, just enter /start!')
        lives = 10
        bot.register_next_step_handler(msg, start_conv)
    else:
        bot.send_message(message.chat.id, 'OMG! You are a winner! Our word was {in_word}'.format(in_word=word_right))
        msg = bot.send_message(message.from_user.id, 'If you want to play again, just enter /start!')
        lives = 10
        bot.register_next_step_handler(msg, start_conv)


bot.polling(none_stop=True)
