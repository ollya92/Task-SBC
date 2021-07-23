import random

# количество жизней
lives = 10

# список слов, из к-рых выбирать
word_variants = ['banana', 'apple', 'peach', 'apricot', 'pineapple', 'avocado', 'mango',
                 'coconut', 'cherry', 'lemon', 'lime', 'grape', 'orange', 'pear', 'watermelon']

# слово для игры
word_right = random.choice(word_variants)

# отображение количества букв в игровом слове
word_in_game = "_" * len(word_right)

while ("_" in word_in_game) and lives > 0:
    print("Lives count: ", lives)
    print(word_in_game)
    letter = input("Input character: ")

    # есть ли буква в слове
    letter = letter.lower()
    if letter in word_right:
        print("You are right! We have this letter in the word!")
        index = -1

        # замена символов в игровом слове
        while word_in_game.count(letter) != word_right.count(letter):
            index = word_right.find(letter, index + 1)
            word_in_game = word_in_game[:index] + letter + word_in_game[index + 1:]
    else:
        lives -= 1
        print("We haven't such letter in the word!")
    print("*" * 10)

if lives > 0:
    print(word_right)
    print("You are winner!")
else:
    print("Right word:", word_right)
    print("Game over")
