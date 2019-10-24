import unittest
from slackin import botRtm

mybot = botRtm.Bot(name='botTest', slack_token='xoxb-779874283382-787468923938-hi4zafVFWLe5enjdfT6pyu6N')



class TestMyBot(unittest.TestCase):

    def test_run(self):
        self.assert (mybot.run())

unittest.main()