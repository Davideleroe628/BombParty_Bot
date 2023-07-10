from wordlist import Wordlist


class Console:

    def __init__(self) -> None:
        self.wordlist = Wordlist()
        self.wordlist.lang = 'english'
        self.last_unkown = ''


    def ask_language(self):
        choice = {}
        for n, i in enumerate(self.wordlist.dicts):
            print(n + 1, i)
            choice[n + 1] = i
        try:
            lang = choice[int(input(f'\nChoose a language: '))]
        except Exception:
            print(f'First language choosen, {choice[1]}')
            lang = choice[1]
        self.wordlist.lang = lang


    def word_with(self, chars):
        print('\nWord with', chars, end=', ')
        word, n, tm = self.wordlist.get_word(chars)
        if word:
            print(f'{word}\n{n} matches ({tm}ms)')
            return word
        elif chars != self.last_unkown:
            print('\nNot found!', f'({tm}ms)')
            self.last_unkown = chars
            return "ERROR can't find word"
