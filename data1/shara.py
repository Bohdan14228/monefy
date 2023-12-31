import re

months_dict = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь',
               '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
               }

pattern = re.compile(r'(\d{1,2}\.\d{1,2}\.\d{4})')

categories = ['Еда🍔', 'Одежда🧤', 'Счета📕', 'Спорт🥊', 'Транспорт♿️', 'Связь📡', 'Здоровье💊']
