# Task 4

def make_hangman(secret_word):
    guesses = []
    def hangman_closure(letter):
        nonlocal guesses
        if letter in guesses:
            print(f"You already tried letter '{letter}'.")
            return False
        guesses.append(letter)
        word = ''.join(letter if letter in guesses else '_' for letter in secret_word)
        print(f'Progress so far: {word}')

        if letter in secret_word:
            print(f"Good guess: '{letter}' is in the word.")
        else:
            print(f"Wrong guess: '{letter}' is not in the word.")

        if '_' not in word:
            return True
        else:
            return False
    return hangman_closure

guess = make_hangman(input('Enter the secret word: '))

while not guess(user_guess := input('Guess a letter: ')):
    if user_guess == 'exit':
        print('Exiting the game.')
        break
    if len(user_guess) > 1 or not user_guess.isalpha():
        print(f"Invalid input: '{user_guess}'. Please guess a single letter.")

print('Congratulations! You\'ve guessed the word.')






