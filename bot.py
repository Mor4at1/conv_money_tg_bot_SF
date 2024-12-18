import telebot
from config import TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)

# команда /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я могу помочь тебе узнать актуальные цены валют. Просто напиши запрос в следующем формате:\n'
                          '[ВАЛЮТА1] [ВАЛЮТА2] [КОЛИЧЕСТВО]\n'
                          '\n'
                          'Примеры:\n'
                          'Если ты хочешь узнать, сколько долларов (USD) можно получить за 1000 российских рублей (RUB), напиши:\n'
                          'RUB USD 1000\n'
                          '\n'
                          'Если ты хочешь узнать, сколько евро (EUR) можно получить за 500 долларов (USD), напиши:\n'
                          'USD EUR 500\n'
                          '\n'
                          'Для получения списка доступных валют напиши /values')

# команда /values
@bot.message_handler(commands=['values'])
def values(message):
    bot.reply_to(message, 'Доступные валюты: \nRUB - Российский рубль \nUSD - Доллар США\nEUR - Евро')

# основной обработчик конвертации валюты
@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    text = message.text.split()

    # Проверка на правильный формат
    if len(text) != 3:
        bot.reply_to(message, 'Ошибка: неверный формат запроса. Пример: USD RUB 1000')
        return  # Выход из функции, если формат неправильный

    base, quote, amount = text[0].upper(), text[1].upper(), text[2]

    # Проверка, чтобы валюта не была одинаковой
    if base == quote:
        bot.reply_to(message, f"Ошибка: Невозможно конвертировать {base} в {quote} , так как это одна и та же валюта.")
        return

    # Проверка на поддерживаемые валюты
    available_currencies = ['USD', 'EUR', 'RUB']
    if base not in available_currencies or quote not in available_currencies:
        bot.reply_to(message, f'Ошибка: поддерживаемые валюты: {", ".join(available_currencies)}'
                              f'\nДля получения списка доступных валют напиши /values')
        return  # Выход из функции при ошибке с валютами

        # Заменяем запятую на точку в количестве (если есть)
    amount = amount.replace(',', '.')

    # Проверка на положительное число
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        bot.reply_to(message, 'Ошибка: количество должно быть положительным числом.')
        return  # Выход из функции при ошибке с количеством

    try:
        # Получаем цену через API
        price = CryptoConverter.get_price(base, quote, amount)

        # Округляем результат
        amount = int(amount) if amount.is_integer() else round(amount, 2)
        price = round(price, 2)

        # Ответ пользователю
        bot.reply_to(message, f'{amount} {base} = {price} {quote}')

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {str(e)}')
    except Exception as e:
        bot.reply_to(message, f'Произошла неизвестная ошибка: {str(e)}')

if __name__ == '__main__':
    bot.polling(none_stop=True)