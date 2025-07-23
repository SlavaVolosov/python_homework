# Task 1
def hello():
    return 'Hello!'

# Task 2
def greet(name: str) -> str:
    return f'Hello, {name.title()}!'

# Task 3
def calc(operand1, operand2, op='multiply'):
    div_zero_error_msg = 'You can\'t divide by 0!'
    type_error_msg = 'You can\'t multiply those values!'
    
    try:
        if not (isinstance(operand1, (int, float)) and isinstance(operand2, (int, float))):
            raise TypeError(type_error_msg)
        match op:
            case 'add':
                return operand1 + operand2
            case 'subtract':
                return operand1 - operand2
            case 'multiply':
                return operand1 * operand2
            case 'divide':
                if operand2 == 0:
                    raise ZeroDivisionError(div_zero_error_msg)
                return operand1 / operand2
            case 'modulo':
                if operand2 == 0:
                    raise ZeroDivisionError(div_zero_error_msg)
                return operand1 % operand2
            case 'int_divide':
                if operand2 == 0:
                    raise ZeroDivisionError(div_zero_error_msg)
                return operand1 // operand2
            case 'power':
                return operand1 ** operand2
            case _:
                raise ValueError(f'Unknown operation: {op}')
    except (TypeError, ZeroDivisionError, ValueError) as e:
        return str(e)

# Task 4
def data_type_conversion(value, type):
    try:
        match type:
            case 'float':
                return float(value)
            case 'int':
                return int(value)
            case 'str':
                return str(value)
            case _:
                raise ValueError(f'You can\'t convert {value} into a {type}.')
    except (ValueError, TypeError) as e:
        return f'You can\'t convert {value} into a {type}.'

# Task 5
def grade(*args):
    try:
        scores = [float(x) for x in args]
        if not scores:
            raise ValueError
        avg = sum(scores) / len(scores)
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    except Exception:
        return 'Invalid data was provided.'

# Task 6
def repeat(s, count):
    try:
        s = str(s)
        count = int(count)
        return ''.join(s for _ in range(count))
    except Exception:
        return 'Invalid input.'

# Task 7
def student_scores(mode, **kwargs):
    try:
        if not kwargs:
            raise ValueError
        scores = {k: v for k, v in kwargs.items()}
        if mode == 'best':
            return max(scores, key=scores.get)
        elif mode == 'mean':
            return sum(scores.values()) / len(scores)
        else:
            raise ValueError
    except Exception:
        return 'Invalid input.'

# Task 8
def titleize(text):
    little_words = {'a', 'on', 'an', 'the', 'of', 'and', 'is', 'in'}
    words = text.split()
    if not words:
        return ''
    result = []
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        elif word.lower() in little_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    return ' '.join(result)

# Task 9
def hangman(secret, guess):
    try:
        secret = str(secret)
        guess = set(str(guess))
        return ''.join(c if c in guess else '_' for c in secret)
    except Exception:
        return 'Invalid input.'

# Task 10
def pig_latin(text):
    def convert_word(word):
        vowels = 'aeiou'
        word = word.strip().lower()
        if not word:
            return ''

        if word[0] in vowels:
            return word + 'ay'

        for i, c in enumerate(word):
            if c in vowels:

                if i > 0 and word[i-1:i+1] == 'qu':
                    # considers a special case of word "qubit"
                    continue
                return word[i:] + word[:i] + 'ay'
        # No vowels found
        return word + 'ay'
    return ' '.join(convert_word(w) for w in text.split())
