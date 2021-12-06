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
              cu [url] - изменить url таблицы регистраций'''

def change_url(new_url):
    new_config = configparser.ConfigParser()
    new_config['Forms'] = {'url': new_url.replace('/edit#gid=', '/export?format=csv&gid=')}
    with open(current_directory + '/config.ini', 'w') as cfgfile:
      new_config.write(cfgfile)

def get_url():
    config = configparser.ConfigParser()
    config.read(current_directory + '/config.ini')
    return config['Forms']['url']

def send_msg(id, msg):
    vk_session.method('messages.send', {'user_id': id, 'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg in ['привет', 'ку', 'здарова', 'прив']:
                send_msg(id, 'Здарова карта 😎')
            if msg == 'help':
                send_msg(id, help_str)
            if msg == 'rc':
                url = get_url()
                send_msg(id, url)
                if url == '':
                    send_msg(id, 'Ошибка: url не задан')
                else:
                    try:
                      df = pd.read_csv(url)
                    except FileNotFoundError:
                      send_msg(id, 'Ошибка: Файл не найден')
                    else:
                      rc = len(df)
                      send_msg(id, f'На меро зарегалось {rc} человек')
            split_msg = msg.split()
            if split_msg[0] == 'cu':
                if len(split_msg) == 2:
                    change_url(split_msg[1])
                    send_msg(id, f'Новый url: {url}')
                else:
                    send_msg(id, 'Ошибка: неверный формат команды, верный формат - cu [url]')
