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


@bot.message_handler(commands=['start'])
def start_message(message):
    global lives, word_right, word_variants, word_in_game
    bot.send_message(message.chat.id, 'Hello! Let\'s play!')
    word_right = random.choice(word_variants)
    word_in_game = "." * len(word_right)
    bot.send_message(message.chat.id, 'Lives count: {live}\nOur word: {word}'.format(live=lives, word=word_in_game))
    bot.register_next_step_handler(message, game)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Hello! Welcome to the game!\nIf you want to start enter /start.')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def game(message):
    global letter, word_right, word_in_game, lives
    while "." in word_in_game and lives > 0:
        bot.send_message(message.chat.id, 'Lives count: {live}'.format(live=lives))
        bot.send_message(message.chat.id, 'Word: {n_word}'.format(n_word=word_in_game))
        letter = message.text.lower()
        if letter in word_right:
            index = -1
            while word_in_game.count(letter) != word_right.count(letter):
                index = word_right.find(letter, index + 1)
                word_in_game = word_in_game[:index] + letter + word_in_game[index + 1:]
        else:
            bot.send_message(message.chat.id, 'We haven\'t such letter')
            lives -= 1
            bot.send_message(message.chat.id, 'Lives count: {live}'.format(live=lives))

    if lives <= 0:
        bot.send_message(message.chat.id, 'Game over')
        bot.send_message(message.chat.id, 'Right word: {our_word}'.format(our_word=word_right))
        bot.send_message(message.chat.id, "Enter /start to start again!")
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, 'Our word was {our_word}'.format(our_word=word_right))
        bot.send_message(message.chat.id, 'You are win!')
        bot.send_message(message.chat.id, "Enter /start to start again!")
        bot.register_next_step_handler(message, start_message)


bot.polling(none_stop=True)
