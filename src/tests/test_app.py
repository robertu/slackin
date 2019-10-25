import unittest
import time
from slackin import botRtm

class TestBot(botRtm.Bot):
    def cmd_hello(self, data=None, args=[]):
        return 'Hello'

mybot = TestBot(name='botTest', slack_token='xoxb-779874283382-787468923938-hi4zafVFWLe5enjdfT6pyu6N')


class TestBotResponse(unittest.TestCase):
    def testHello(self):
        mess = mybot.client.chat_postMessage(
            channel='DPLDHSYBG',
            text="botTest hello"
        )
        time.sleep(5)
        self.assertEqual("botTest hello", mess.data['message']['text'])

unittest.main()   

