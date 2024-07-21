async def get_first_text(username):
    return f"*Здравствуйте {username}\nдобро пожаловать на курс обмена*"


async def get_command_exchange():
    return f"*Используйте формат команды:\nот до суммы\nпример:USD RUB 10*"


async def error_message():
    return f"*Некорректный код валюты или невозможно получить курс обмена*"


async def command_error():
    return f"*Произошла ошибка при обработке команды*"


async def value_error_message():
    return f"*Сумма должна быть числом*"


async def error_rates():
    return f"Пожалуйста, введите валюты, для которых вы хотите просмотреть курсы. Например: `/rates USD UZS EUR`'"


async def rate_error():
    return f'*На данный момент невозможно получить курсы валют. Пожалуйста, повторите попытку позже*'


async def get_rates(rates_message):
    rates_message = f'*Текущие обменные курсы: {rates_message}*'
    return rates_message
