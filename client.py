import requests
from playsound import playsound
import os
import numpy as np
import re
import json

from utils import response_log


with open('config.json') as f:
    cfg = json.load(f)
url = cfg['server_ip']


def get_gpt(name, chat):
    param={
        'name': name,
        'chat': chat,
    }
    res = requests.post(url+'/chat', json=param)
    res_json = res.json()
    
    if res_json == 'end':
        return

    answer = res_json['response']
    
    response_log(res_json)

    return answer

def get_tts(name, answer):
    with open('./prompt.txt', 'w', encoding='UTF-8') as f:
        f.write(answer)

    param={
        'name': name,
        'chat': answer
    }
    res = requests.post(url+'/tts', json=param)

    with open('./test.wav', 'wb') as f:
        f.write(res.content)

    # 그루브 뮤직 플레이어 안쓰고 음성출력 해야됨

    # tlen = int(audio.shape[0]/22050)+1

    os.system("test.wav")
    # time.sleep(1)
    # playsound('./test.wav')


def pickup_message(chat_chunk):
    message_list = [msg[2] for msg in chat_chunk]
    param={
        'message_list': message_list
    }
    res = requests.post(url+'/importance', json=param)

    res = res.content.decode()
    print(res)

    res = re.sub(r'[^0-9,]', '', res)
    res = res.split(',')
    
    score = [int(score) for score in res]
    idx = np.argmax(score)

    if max(score) <= 3:
        return -1

    return idx