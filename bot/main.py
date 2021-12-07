import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

import pandas as pd
import configparser
import pathlib

current_directory = str(pathlib.Path(__file__).parent.resolve())

vk_session = vk_api.VkApi(token='42853ead70045753424554372fd10d60942801fbcace3a0128e4b6d8d6df56cbf89922db63b3d19af179c')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

help_str = '''rc - количество регистраций на меро
              gu - текущий url таблицы регистраций
              cu [url] - изменить url таблицы регистраций'''

def change_url(new_url):
    new_config = configparser.ConfigParser()
    new_config['Forms'] = {'url': new_url}
    with open(current_directory + '/config.ini', 'w') as cfgfile:
      new_config.write(cfgfile)

def get_url():
    config = configparser.ConfigParser()
    config.read(current_directory + '/config.ini')
    return config['Forms']['url']
  
def add_id(id):
    config = configparser.ConfigParser()
    config.read(current_directory + '/config.ini')
    ids = config['Admins']['ids']
    if str(id) in ids.split():
      send_msg(id, f'У тебя уже есть права админа')
      return
    config.set('Admins', 'ids', f'{ids} {id}')
    with open(current_directory + '/config.ini', 'w') as cfgfile:
      config.write(cfgfile)
    send_msg(id, f'Права админа получены')
      
def check_id(id):
    config = configparser.ConfigParser()
    config.read(current_directory + '/config.ini')
    return str(id) in config['Admins']['ids'].split()

def send_msg(id, msg):
    vk_session.method('messages.send', {'user_id': id, 'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            split_msg = event.text.split()
            id = event.user_id
            if msg in ['привет', 'ку', 'здарова', 'прив']:
                send_msg(id, 'Здарова карта 😎')
            elif msg == 'joker':
                add_id(id)
            elif msg == 'help':
                if not check_id(id):
                    continue
                send_msg(id, help_str)
            elif msg == 'rc':
                if not check_id(id):
                    continue
                url = get_url()
                if url == '':
                    send_msg(id, 'Ошибка: url не задан')
                else:
                    try:
                      df = pd.read_csv(url.replace('/edit?resourcekey#gid=', '/export?format=csv&gid='))
                      rc = len(df)
                      send_msg(id, f'Регистраций: {rc}')
                    except Exception as e:
                      send_msg(id, e)
            elif msg == 'gu':
                if not check_id(id):
                    continue
                send_msg(id, f'Текущий url: {get_url()}')
            elif split_msg[0] == 'cu':
                if not check_id(id):
                    continue
                if len(split_msg) == 2:
                    change_url(split_msg[1])
                else:
                    send_msg(id, 'Ошибка: неверный формат команды, верный формат - cu [url]')
            else:
                send_msg(id, 'Каво? Не понял')
