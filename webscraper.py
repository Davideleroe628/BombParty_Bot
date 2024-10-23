from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep as delay

from const import *


class Webscraper:

    def __init__(self) -> None:
        chrome_driver = ChromeDriverManager().install()
        self.driver = Chrome(service=Service(chrome_driver))
        self.wait = WebDriverWait(self.driver, 5)
        self.servers = ['falcon', 'phoenix']
        self.server = None
        self._open_website()
        #self._create_room()
        self._login()


    def _open_website(self):
        self.driver.set_window_rect(-7, 0, 1294, 1407)
        self.driver.get(LINK)


    def _create_room(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                'label[for="gameRadio-bombparty"]')))
        self.driver.find_element(By.CSS_SELECTOR, 'label[for="'
                                 'gameRadio-bombparty"]').click()
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'roomName')))
        room_name_element = self.driver.find_element(By.CLASS_NAME, 'roomName')
        room_name_element.clear()
        room_name_element.send_keys(ROOM_NAME)
        self.driver.find_element(By.XPATH, "//button[@class='styled'"
                                 " and @data-text='play']").click()
        #self._set_english()


    def _login(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                "input.styled.nickname[placeholder='Il tuo nome']")))
        bot_name_element = self.driver.find_element(By.CSS_SELECTOR,
                "input.styled.nickname[placeholder='Il tuo nome']")
        bot_name_element.clear()
        self.driver.execute_script("arguments[0].value = arguments[1]",
            bot_name_element, BOT_NAME)
        self.driver.find_element(By.XPATH,
                        "//button[contains(text(), 'OK')]").click()


    def _enter_iframe(self):
        if self.server is None:
            for ip in self.servers:
                try:
                    iframe = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, f'iframe[src="https://{ip}.jklm.fun'
                                          '/games/bombparty"]')))
                    self.driver.switch_to.frame(iframe)
                    print(f'Server is {ip}')
                    self.server = ip
                    return iframe
                except Exception:
                    print(f'not {ip} server')
            input("Iframe's server not in list")

        else:
            iframe = self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, f'iframe[src="https://{self.server}.jklm.fun'
                                  '/games/bombparty"]')))
            self.driver.switch_to.frame(iframe)
            return iframe


    def _set_english(self):
        self._enter_iframe()
        input('press enter')
        self.driver.find_element(By.XPATH,
                            "//button[@class='toggleRules']").click()
        self.driver.find_element(By.XPATH,
            '//option[@value="en" and text()="Inglese"]').click()
        self.driver.find_element(By.CSS_SELECTOR, "button.toggleRules").click()
        self.driver.switch_to.default_content()


    def try_join_game(self):
        self._enter_iframe()
        if not self.driver.find_element(
                By.XPATH, "//div[@class='join']").is_displayed():
            return False
        join_button = self.driver.find_element(By.XPATH, "//button[contains"
                                    "(@class, 'styled') and contains(@class,"
                                    "'joinRound') and @data-text='joinGame']")
        join_button.click()
        self.driver.switch_to.default_content()
        return True


    def get_sillab(self):
        self._enter_iframe()
        sillable = self.driver.find_element(By.CLASS_NAME, 'syllable').text
        self.driver.switch_to.default_content()
        return sillable.lower()


    def is_my_turn(self):
        self._enter_iframe()
        element = self.driver.find_element(By.CLASS_NAME, 'selfTurn')
        my_turn = element is not None and element.is_displayed()
        self.driver.switch_to.default_content()
        return my_turn


    def write(self, word):
        self._enter_iframe()
        try:
            input_element = self.driver.find_element(By.XPATH,
                '//input[@type="text" and @maxlength="30" and @autocomplete="off"'
                ' and @autocorrect="off" and @autocapitalize="off" and @spellcheck='
                '"false" and contains(@class, "styled")]')
            input_element.send_keys(word)
            delay(.001)
            input_element.find_element(By.XPATH, "./ancestor::form").submit()
        except Exception:
            print('\nError trying to write\n')
        self.driver.switch_to.default_content()
