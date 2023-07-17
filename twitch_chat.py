import socket
import re
import threading
import time
import json

from client import get_gpt, get_tts, pickup_message
from utils import twitch_chat_log


with open('config.json') as f:
    cfg = json.load(f)

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'ai_riya_bot'
token = cfg["oauth"]
channel = '#ai_riya'


IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC.connect((server, port))

IRC.send(f"PASS {token}\n".encode('utf-8'))
IRC.send(f"NICK {nickname}\n".encode('utf-8'))
IRC.send(f"JOIN {channel}\n".encode('utf-8'))

MESSAGE_REGEX = re.compile(r'^:(?P<username>[^!]+)![^@]+@[^\.]+\.tmi\.twitch\.tv PRIVMSG #(?P<channel>[^ ]+) :(?P<message>.+)\r\n$')

chat_list = []

def handle_messages(IRC):
    while True:
        resp = IRC.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            IRC.send("PONG\n".encode('utf-8'))
        else:
            match = MESSAGE_REGEX.match(resp)
            if match:
                username = match.group('username')
                channel = match.group('channel')
                message = match.group('message')

                chat_list.append([username, channel, message])

thread = threading.Thread(target=handle_messages, args=(IRC,))
thread.start()

final_len = 0
flag_stack = 0

while True:
    print(chat_list)
    len_chat = len(chat_list)
    # 여기 수정해서 현재 있는 chat_list에서 우선순위 해서 하나 뽑는걸로 변경
    if len_chat > final_len:
        chat_chunk = chat_list[final_len:len_chat]
        twitch_chat_log(chat_chunk)
        
        reversed(chat_chunk)
        idx = pickup_message(chat_chunk)

        final_len = len_chat
        
        if idx == -1:
            flag_stack += 1
            continue

        answer = get_gpt(chat_chunk[idx][0], chat_chunk[idx][2])
        get_tts(chat_chunk[idx][0], answer)

        print(f'message: {chat_chunk[idx][2]}')
        print(f'answer: {answer}')
    # else:
    #     flag_stack += 1

    # if flag_stack >= 60:
    #     # 일정시간동안 채팅이 없거나 영양가 없는 채팅만 있을때 혼잣말 하게 하기
    #     message = "리야님 아무 얘기 해줘요"
    #     answer = get_gpt('', message)
    #     get_tts('', answer)
        
    #     flag_stack = 0

    time.sleep(0.5)