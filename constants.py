import telegram

BOT_API_KEY = '5328821508:AAHWnEOvh1lGITa0BhaNgLQ9HJulngvAYb8' # https://t.me/python_wheather_bot

BASE_URL = "https://community-open-weather-map.p.rapidapi.com"
RAPID_API_KEY = "8435e3b835mshcf8322310756be3p1e3038jsn5b8c35f02c10"
RAPID_API_HOST = "community-open-weather-map.p.rapidapi.com"

KB_MAIN = telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton('طقس اليوم')],
    [telegram.KeyboardButton('الطقس الاسبوعي')],
])

GOVERNORATES_AR = ["دمشق","حلب","اللاذقية","حمص","حماة","طرطوس"]
GOVERNORATES_EN = ["Damascus","Aleppo","Latakia","Homs","Hama","Tartous"]

KB_GOVERNORATES = telegram.ReplyKeyboardMarkup([ [telegram.KeyboardButton(g)] for g in GOVERNORATES_AR ])

DAYS = ['الاثنين','الثلاثاء','الاربعاء','الخميس','الجمعة','السبت','الأحد']
