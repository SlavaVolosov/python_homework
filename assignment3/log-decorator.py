import logging
logger = logging.getLogger(__name__ + '_parameter_log')
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler('./decorator.log', 'a'))

# Task 1
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f'function: {func.__name__} positional parameters: {args or 'none'} keyword parameters: {kwargs or 'none'} return: {result or 'none'}'
    return wrapper


@logger_decorator
def useless_func():
    does_nothing = 1 + 1

useless_func_result = useless_func()
print(useless_func_result)
logger.log(logging.INFO, useless_func_result)


@logger_decorator
def true_returning_func(*args):
    return True

true_returning_func_result = true_returning_func('q', 'wer', 23, ['q', 'w', 'e', 'r'], {'q': 221, 'w': 22})
print(true_returning_func_result)
logger.log(logging.INFO, true_returning_func_result)


@logger_decorator
def logger_decorator_returning_func(**kwargs):
    return logger_decorator

logger_decorator_returning_func_result = logger_decorator_returning_func(first_param=21, second_param='asd', third_param=[1, 2, 3, 4, 5])
print(logger_decorator_returning_func_result)
logger.log(logging.INFO, logger_decorator_returning_func_result)
