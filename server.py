import random
import requests
import json


class telegram_chatbot():

    def __init__(self):
        self.token = "1402169347:AAEPgpcKZVw3PEKHDn3wgLHYInuRpu5mnl8"
        self.base = "https://api.telegram.org/bot"+self.token+"/"

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

thisdict = {
    "hi": ["Hi!", "I am glad! You are talking to me."],
    "hello": ["hi there", "hello"],
    "how old are you?": ["I am 18 years old.", "18 years young!"],
    "where are you from?": ["I am from ComputerLand", "I am from America."],
    "have you product?": ["Yes, Coockies 2 $", "No, I haven't anything."],
    "are they quality?": ["Yes, they are excellent", "No, they are very bad."]
}


def greeting(sentence):
    get_sent = thisdict.get(sentence)
    if get_sent:
        rnd = random.randint(0, 1)
        responce = thisdict[sentence.lower()][rnd]
    else:
        responce = "I am sorry. I don't understand you."
    return responce


bot = telegram_chatbot()


def make_reply(msg):
    reply = None
    if msg is not None:
        reply = greeting(msg)
    return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)
            bot.send_message(reply, from_)
