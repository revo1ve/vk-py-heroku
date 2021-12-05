import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='af0697ce8a3851d732c3328a249ea45c7fc4dbd62cb55f9db0f86489760df89d31fbecd56a337fc6ebc58')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

#Lslongpoll = VkLongPoll(vk_session)
#Lsvk = vk_session.get_api()

def send_msg(id, msg):
    vk_session.method('messages.send', {'user_id': id, 'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'hi':
                send_msg(id, 'Илья гей')