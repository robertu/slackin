from Bot import Bot

class MyBot(Bot):
    def test(self):
        print(self.ss)
    
bot = MyBot("xoxb-779874283382-788993604672-absKGQndADDnDNwYukXMWnZM","18fef276a83cc2f4d8d08b2ec86c7d77","0.0.0.0", 4004)
bot.run()