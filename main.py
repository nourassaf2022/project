from datetime import datetime
import requests
from constants import *
from telegram.ext import *


clients_weather_type = {}

def start_command(update, context):
    chat_id = update.message.chat_id
    print('start from chat id: {}'.format(chat_id))
    bot_msg = "مرحبا، أدخل إحدى الخيارات التالية"    
    context.bot.send_message(chat_id=chat_id,
                            text=bot_msg,
                            reply_markup=KB_MAIN)

def message_handler(update, context):
    user_msg = update.message.text
    chat_id = update.message.chat_id
    print(user_msg)
    
    weather_type = ""
    if user_msg == "طقس اليوم":
        weather_type = "current"
    if user_msg == "الطقس الاسبوعي":
        weather_type = "weekly"

    if weather_type!="":
        clients_weather_type[chat_id] = weather_type
        bot_msg = "يرجى اختيار المحافظة"
        context.bot.send_message(chat_id=chat_id,
                                    text=bot_msg,
                                    reply_markup=KB_GOVERNORATES)

    else:
        if user_msg in GOVERNORATES_AR:
            gov_ar = user_msg
            index = GOVERNORATES_AR.index(gov_ar)
            gov_en = GOVERNORATES_EN[index]
            
            # get weather type
            weather_type = clients_weather_type[chat_id] if chat_id in clients_weather_type else "current"
            
            # get the weather and send the message
            if weather_type == "current":
                bot_msg = get_current_weather(gov_en)
            else:
                bot_msg = get_weekly_weather(gov_en)
        else:
            bot_msg = "اختيار خاطئ، أدخل إحدى الخيارات التالية"

        context.bot.send_message(chat_id=chat_id,
                                text=bot_msg,
                                reply_markup=KB_MAIN)

def get_current_weather(city):
    url = BASE_URL + "/weather?units=metric&q={}".format(city)
    res = requests.get(url,headers={'X-RapidAPI-Key':RAPID_API_KEY,'X-RapidAPI-Host':RAPID_API_HOST})
    status = res.status_code
    if (status == 200):
        res = res.json()
        msg = "{} {}°\nClouds: {}%\nHumidity: {}%\nWind: {}m/s\nPressure: {}hpa".format(
            res['weather'][0]['description'],
            res['main']['temp'],
            res['clouds']['all'],
            res['main']['humidity'],
            res['wind']['speed'],
            res['main']['pressure'],
        )
        return msg
    return "عذراً حصل خطأ تقني"

def get_weekly_weather(city):
    url = BASE_URL + "/climate/month?units=metric&q={}".format(city)
    res = requests.get(url,headers={'X-RapidAPI-Key':RAPID_API_KEY,'X-RapidAPI-Host':RAPID_API_HOST})
    status = res.status_code
    if (status == 200):
        res = res.json()
        weather_days = res['list']
        msg = ""
        for i in range(7):
            weather = weather_days[i]
            dt = datetime.fromtimestamp(weather['dt'])
            day = DAYS[dt.weekday()]
            average_min = weather['temp']['average_min']
            average_max = weather['temp']['average_max']
            humidity = weather['humidity']
            wind_speed = weather['wind_speed']
            
            msg = msg + "{} {}° - {}°\nHumidity: {}%\nWind: {}m/s\n\n".format(day, average_min, average_max, humidity, wind_speed)
        return msg
    return "عذراً حصل خطأ تقني"

def main():
    updater = Updater(BOT_API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text,message_handler))
    updater.start_polling()
    updater.idle()


print('Bot Started...')
main()


# pip install python-telegram-bot
# pip install requests
