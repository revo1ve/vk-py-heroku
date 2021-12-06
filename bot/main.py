import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

import pandas as pd

vk_session = vk_api.VkApi(token='af0697ce8a3851d732c3328a249ea45c7fc4dbd62cb55f9db0f86489760df89d31fbecd56a337fc6ebc58')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

#Lslongpoll = VkLongPoll(vk_session)
#Lsvk = vk_session.get_api()

sheet_url = 'https://docs.google.com/spreadsheets/d/11hUo2QLmWHdNsMI8lxxvlomE0HNztg_eos4lwMht2uM/edit#gid=2070277591'
url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url)

def send_msg(id, msg):
    vk_session.method('messages.send', {'user_id': id, 'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'hi':
                send_msg(id, 'Здарова карта')
            if msg == 'rc':
                rc = len(df) - 4
                send_msg(id, f'На меро зарегалось {rc} человек')
