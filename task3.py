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


@bot.message_handler(commands=['start'], content_types=['text'])
def start_conv(message):
    global lives, word_right, word_in_game, word_variants, letter
    word_right = random.choice(word_variants)
    word_in_game = '*' * len(word_right)
    bot.send_message(message.chat.id, 'Let\'s play with me!')
    bot.send_message(message.chat.id, 'You have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))
    bot.register_next_step_handler(message, start_game)


def start_game(message):
    global lives, word_right, word_in_game, word_variants, letter
    letter = message.text.lower()
    if letter.isalpha() and len(letter) == 1:
        if letter in word_right:
            bot.register_next_step_handler(message, is_letter)
        else:
            bot.register_next_step_handler(message, no_letter)
    else:
        msg = bot.send_message(message.chat.id, 'You should enter 1 letter!')
        bot.register_next_step_handler(msg, start_game)


def is_letter(message):
    global lives, word_right, word_in_game, word_variants, letter
    if '*' in word_in_game:
        index = -1
        while word_in_game.count(letter) != word_right.count(letter):
            index = word_right.find(letter, index + 1)
            word_in_game = word_in_game[:index] + letter + word_in_game[index + 1:]
        bot.send_message(message.chat.id,
                         'You have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))
        bot.register_next_step_handler(message, start_game)
    if word_in_game.count('*') == 0:
        if lives <= 0:
            bot.send_message(message.chat.id,
                             'Unfortunately, you are lost all your lives!\nOur word was {in_word}'.format(in_word=word_right))
            lives = 10
            msg = bot.send_message(message.from_user.id, 'If you want to play again, just enter /start!')
            bot.register_next_step_handler(msg, start_conv)
        else:
            bot.send_message(message.chat.id,
                             'OMG! You are a winner! Our word was {in_word}'.format(in_word=word_right))
            lives = 10
            msg = bot.send_message(message.from_user.id, 'If you want to play again, just enter /start!')
            bot.register_next_step_handler(msg, start_conv)


def no_letter(message):
    global lives, word_right, word_in_game, word_variants, letter
    lives -= 1
    bot.send_message(message.chat.id, 'There is no such letter in the word! You lost 1 live!\nYou have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))
    """bot.send_message(message.chat.id,
                     'You have {live} lives\nWord: {in_word}'.format(live=lives, in_word=word_in_game))"""
    bot.register_next_step_handler(message, start_game)
    if lives <= 0:
        bot.send_message(message.chat.id,
                         'Unfortunately, you are lost all your lives!\nOur word was {in_word}'.format(
                             in_word=word_right))
        msg = bot.send_message(message.from_user.id, 'If you want to play again, just enter /start!')
        lives = 10
        bot.register_next_step_handler(msg, start_game)


bot.polling()
