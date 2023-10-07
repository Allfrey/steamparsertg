import telebot
import requests
from bs4 import BeautifulSoup
headers = {"Accept-Language": "ru-RU"}
bot = telebot.TeleBot('token')

bot = telebot.TeleBot('you token')
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
    response = requests.get(profile_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    profile_name = soup.select_one('.actual_persona_name').text.strip()
    two_name_element = soup.select_one('.header_real_name')
    two_name = two_name_element.text.strip() if two_name_element else 'Нет данных'
    profile_level_element = soup.select_one('.friendPlayerLevelNum')
    profile_level = profile_level_element.text.strip() if profile_level_element else 'Нет данных'
    profile_friend_element = soup.select('.profile_count_link_total')[-1]
    profile_friend = profile_friend_element.text.strip() if profile_friend_element else 'Нет данных'
    was_element = soup.select_one('.profile_in_game_name')
    was = was_element.text.strip() if was_element else 'Нет данных'
    profile_in_game_name_element = soup.select_one('.profile_in_game_name') 
    profile_in_game_name = profile_in_game_name_element.text.strip() if profile_in_game_name_element else 'Нет данных'
    games_purchased_element = soup.select('.profile_count_link_total')[1]
    games_purchased =  games_purchased_element.text.strip() if  games_purchased_element else 'Нет данных'
    groups_profile_element = soup.select('.profile_count_link_total')[-2]
    groups_profile = groups_profile_element.text.strip() if groups_profile_element else 'Нет данных'
    icons_element = soup.select('.profile_count_link_total')[0]
    icons = icons_element.text.strip() if icons_element else 'Нет данных'
    status_element = soup.select_one('.profile_in_game_header').text.strip()
    info_element = soup.select_one('.profile_summary')
    info = info_element.text.strip() if info_element else 'Нет данных'
    recent_activity_element = soup.select_one('.recentgame_recentplaytime')
    recent_activity = recent_activity_element.text.strip() if recent_activity_element else 'Нет данных'
    avatar_element = soup.select('.playerAvatarAutoSizeInner img')
    if len(avatar_element) > 0:
      avatar = avatar_element[0]['src']
    game1_element = soup.select('.game_name')[0]
    game1 = game1_element.text.strip() if game1_element else 'Нет данных'
    play_hours_element = soup.select('.game_info_details')[0]
    play_hours = play_hours_element.text.strip() if play_hours_element else 'Нет данных'
    game2_element = soup.select('.game_name')[1]
    game2 = game2_element.text.strip() if game2_element else 'Нет данных'
    play_hours2_element = soup.select('.game_info_details')[1]
    play_hours2 = play_hours2_element.text.strip() if play_hours2_element else 'Нет данных'
    game3_element = soup.select('.game_name')[2]
    game3 = game3_element.text.strip() if game3_element else 'Нет данных'
    play_hours3_element = soup.select('.game_info_details')[2]
    play_hours3 = play_hours3_element.text.strip() if play_hours3_element else 'Нет данных'
    ban_element = soup.select_one('.profile_ban')
    ban = ban_element.text.strip() if ban_element else 'Нет данных'
    ban_info_element = soup.select_one('.profile_ban_status')
    ban_info = ban_info_element.text.strip() if ban_info_element else 'Нет данных'

    bot.reply_to(message, f"Имя профиля: {profile_name}\nВторое имя\страна: {two_name}\nИнформация: {info}\nУровень профиля: {profile_level}\nСтатус: {status_element}\nИграет в: {profile_in_game_name}\nБыл в сети: {was}\nДрузей: {profile_friend}\n Баны: {ban}\n{ban_info}\nИгр куплено: {games_purchased}\nЗначков: {icons}\nГрупп: {groups_profile}\nНедавняя активность: {recent_activity}\nИгра: {game1} {play_hours}\nИгра2: {game2} {play_hours2}\nИгра3: {game3} {play_hours3}\nАватар: {avatar}")

bot.polling()
