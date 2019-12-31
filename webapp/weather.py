import requests
from flask import current_app  # Позволяет обращаться к текущему приложению фласк


def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'key': current_app.config['WEATHER_API_KEY'],
        'q': city_name,
        'num_of_days': 1,
        'format': 'json',
        'lang': 'ru'
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()  # Сгенерирует исключение, если сервер ответил кодом 4хх или 5хх
        weather = result.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False

    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
