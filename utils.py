import json
import datetime

path = './log'

def _response_reformatting(response):
    log = {}
    for key, value in response.items():
        log[key] = value

    return log

def response_log(response):
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log = _response_reformatting(response)
    with open(f'{path}/response/{date}.json', 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent='\t')


today = datetime.date.today()
def twitch_chat_log(chat_chunk):
    with open(f'{path}/twitchchat/{today}.txt', 'a', encoding='utf-8') as chat_log:
        for username, channel, message in chat_chunk:
            chat_log.write(f'{username}: {message}\n')