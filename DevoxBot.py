import time

from const import *
from console import Console
from webscraper import Webscraper


class Main:

    def __init__(self) -> None:
        self.console = Console()
        self.scraper = Webscraper()
        self.wordlist = self.console.wordlist
        self.playing = False


    def mainloop(self):
        while True:

            if self.scraper.is_my_turn():
                syllable = self.scraper.get_sillab()
                word = self.console.word_with(syllable)
                self.scraper.write(word)
                time.sleep(DELAY)



if __name__ == '__main__':
    main = Main()
    main.mainloop()
