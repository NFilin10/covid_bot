import telebot
from covid import Covid
from telebot import types
from bs4 import BeautifulSoup
import requests
import config

#info about covid
covid = Covid()

#token
bot = telebot.TeleBot(config.token)

#start message
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'choose a country', reply_markup=markup)

#flags
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
world = types.KeyboardButton('🌎')
est = types.KeyboardButton('🇪🇪')
rus = types.KeyboardButton('🇷🇺')
fin = types.KeyboardButton('🇫🇮')
lv = types.KeyboardButton('🇱🇻')
usa = types.KeyboardButton('🇺🇸')
fr = types.KeyboardButton('🇫🇷')
es = types.KeyboardButton('🇪🇸')
it = types.KeyboardButton('🇮🇹')
uk = types.KeyboardButton('🇬🇧')
de = types.KeyboardButton('🇩🇪')
lt = types.KeyboardButton('🇱🇹')
markup.add(world, est, rus, fin, lv, usa, fr, es, it, uk, de, lt)

flags = {"🇪🇪": ["58", "estonia"], "🇷🇺": ["142", "russia"], "🇫🇮": ["62", "finland"], "🇱🇻": ["97", "latvia"], "🇺🇸": ["178", "usa"], "🇫🇷": ["63", "france"], "🇪🇸": ["162", "spain"], "🇮🇹": ["86", "italy"], "🇬🇧": ["181", "uk"], "🇩🇪": ["67", "germany"], "🇱🇹": ["103", "lithuania"]}

def cov(id, country, message):
    covid = Covid()
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response = requests.get("https://coronavirus-monitor.info/country/" + country, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='info_blk stat_block confirmed')
    comps = []
    print(id)
    location = covid.get_status_by_country_id(id)
    try:
        for item in items:
            comps.append({
                'cases': item.find('sup').get_text()
            })
        for title in comps:
            a = (title['cases'])

        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + a)
    except AttributeError:
        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + 'no data yet')

#flag function
@bot.message_handler(content_types=['text'])
def messages(message):
    if message.text in flags:
        users_input = message.text
        cov(flags[users_input][0], flags[users_input][1], message)
    elif message.text == '🌎':
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        bot.send_message(message.chat.id, 'World:' + '\n' + "Confirmed: " + str(confirmed) + '\n' + 'Active: '
                         + str(active) + '\n' + 'Recovered: ' + str(recovered) + '\n' + 'Deaths: ' + str(
            deaths) + '\n')
    else:
        bot.send_message(message.chat.id, "Try again")

#start bot
if  __name__ == '__main__':
    bot.polling(none_stop=True)
