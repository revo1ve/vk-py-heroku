import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

import pandas as pd

vk_session = vk_api.VkApi(token='42853ead70045753424554372fd10d60942801fbcace3a0128e4b6d8d6df56cbf89922db63b3d19af179c')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

url = None

help_str = '''rc - количество регистраций на меро /n
              cu [url] - изменить url таблицы регистраций'''

def change_url(new_url):
    global url
    url = new_url.replace('/edit#gid=', '/export?format=csv&gid=')

def send_msg(id, msg):
    vk_session.method('messages.send', {'user_id': id, 'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg in ['Привет', 'Ку', 'Здарова', 'Прив']:
                send_msg(id, 'Здарова карта 😎')
            if msg == 'help':
                send_msg(id, help_str)
            if msg == 'rc':
                if url == None:
                    send_msg(id, 'Ошибка: url не задан')
                else:
                    df = pd.read_csv(url)
                    rc = len(df)
                    send_msg(id, f'На меро зарегалось {rc} человек')
            split_msg = msg.split()
            if msg.split()[0] == 'cu':
                if len(split_msg) == 2:
                    change_url(split_msg[1])
                    send_msg(id, f'Новый url: {url}')
                else:
                    send_msg(id, 'Ошибка: неверный формат команды, верный формат - cu [url]')
