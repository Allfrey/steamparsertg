import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('6401526019:AAHxDiEj7K-APzuZG6QANZW1abadgnlWAY8')
translations = {
    'Currently Online': 'В сети',
    'Currently In-Game': 'В игре',
    'Currently Offline': 'Не в сети'}
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на профиль Steam для парсинга.")

@bot.message_handler(func=lambda message: True)
def parse_profile(message):
    profile_url = message.text
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем информацию из профиля Steam
    profile_name = soup.select_one('.actual_persona_name').text.strip()
    two_name_element = soup.select_one('.header_real_name')
    two_name = two_name_element.text.strip() if two_name_element else 'Нет данных'
    profile_level_element = soup.select_one('.friendPlayerLevelNum')
    profile_level = profile_level_element.text.strip() if profile_level_element else 'Нет данных'
    profile_friend_element = soup.select('.profile_count_link_total')[-1]
    profile_friend = profile_friend_element.text.strip() if profile_friend_element else 'Нет данных'
    was_element = soup.find('div.profile_in_game_name')
    was = was_element.text.strip() if was_element else 'Нет данных'
    profile_in_game_name_element = soup.select_one('.profile_in_game_name') 
    profile_in_game_name = profile_in_game_name_element.text.strip() if profile_in_game_name_element else 'Нет данных'
    games_purchased_element = soup.select('.profile_count_link_total')[1]
    games_purchased =  games_purchased_element.text.strip() if  games_purchased_element else 'Нет данных'
    groups_profile_element = soup.select('.profile_count_link_total')[-2]
    groups_profile = groups_profile_element.text.strip() if groups_profile_element else 'Нет данных'
    icons_element = soup.select('.profile_count_link_total')[0]
    icons = icons_element.text.strip() if icons_element else 'Нет данных'
    status_element = soup.select_one('.profile_in_game_header')
    info_element = soup.select_one('.profile_summary')
    info = info_element.text.strip() if info_element else 'Нет данных'
    recent_activity_element = soup.select_one('.recentgame_recentplaytime')
    if status_element:
     english_status = status_element.text.strip()
    russian_status = translations.get(english_status, english_status)
    if recent_activity_element:
     english_recent_activity = recent_activity_element.text.strip()
    hours = english_recent_activity.split(' ')[0] 
    russian_recent_activity = f"{hours} ч. за последние 2 недели"
    avatar_element = soup.select('.playerAvatarAutoSizeInner img')
    if len(avatar_element) > 0:
      avatar = avatar_element[0]['src']
    
    
    bot.reply_to(message, f"Имя профиля: {profile_name}\nВторое имя\страна: {two_name}\nИнформация: {info}\nУровень профиля: {profile_level}\nСтатус: {russian_status}\nИграет в: {profile_in_game_name}\nБыл в сети: {was}\nДрузей: {profile_friend}\nИгр куплено: {games_purchased}\nЗначков: {icons}\nГрупп: {groups_profile}\nНедавняя активность: {russian_recent_activity}\nАватар: {avatar}")

bot.polling()
