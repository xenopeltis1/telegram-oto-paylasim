import requests
from typing import Dict
import time
import threading
import datetime


class TelegramBot:
    token = "telegram bot tokeni yaz"
    chatid = "paylaşımların yapılacağı telegram kanalının chat id'si"
    dhook = 'discord webhook yaz'
    banned_hours = [0,1,2,3,4,5,6,7,8]
    admins = ['hkeydesign']


    @classmethod
    def log(cmd,message):
        r = requests.post(TelegramBot.dhook,data={
        'content':f'```{message}```'
        })
        post = True

        if str(r) != '<Response [204]>':
            post = False

        return post


    @classmethod
    def timenow(cmd):
        time = datetime.datetime.now()
        hour = time.hour
        time = True

        if hour in TelegramBot.banned_hours:
            time = False

        return time


    @classmethod
    def checkit(cmd) -> Dict[str, str]:
        r = requests.get(f'https://api.telegram.org/bot{TelegramBot.token}/getUpdates').json()
        
        status = True
        message = None
        author = None

        try:
            message = r['result'][-1]['message']['text']
            author = r['result'][-1]['message']['chat']['username']
        except:
            status = False
        
        result = {
            'status':status,
            'message':message,
            'author':author
        }

        return result


    @classmethod
    def share(cmd,message):
        msg = {'text': message}
        r = requests.post(
            f'https://api.telegram.org/bot{TelegramBot.token}/sendMessage?chat_id={TelegramBot.chatid}',
            data=f'{msg}\nXenopeltis tarafından yapılmıştır, açık kaynak kodludur.').json()
        
        stats = f'Durum : {r["ok"]}\nPaylaşılan Mesaj : {message}'

        return stats

posts = []
posted = []

def checking(posts):
    while True:
        data = TelegramBot.checkit()

        if data['status'] == True:
            if data['author'] in TelegramBot.admins and data['message'] not in posts and data['message'] not in posted:
                posts.append(data['message'])
                log_message = f'Yeni bir mesaj eklendi. Zamanı gelince paylaşacağım rahat ol :)\nMesaj : {data["message"]}'
                TelegramBot.log(log_message)


        print(f'Paylaşılacaklar : {posts}')
            
        time.sleep(1)



def sh(posts):
    while True:
        
        if TelegramBot.timenow() == True:
            try:
                if posts[0] not in posted:
                    st = TelegramBot.share(posts[0])
                    posted.append(posts[0])
                    posts.pop(0)
                    log_message = f'Paylaşım yapıldı !\n{st}'
                    TelegramBot.log(log_message)
                else:
                    posts.pop(0)

            except IndexError:
                log_message = f'Paylaşacak bir şey yok.'
                TelegramBot.log(log_message)
        else:
            log_message = 'Gece gece paylaşım mı yapılır aga :D Kafayı mı sıyırdın ?'
            TelegramBot.log(log_message)

        time.sleep(20)


x = threading.Thread(target=checking, args=(posts,))
x.start()

y = threading.Thread(target=sh, args=(posts,))
y.start()
