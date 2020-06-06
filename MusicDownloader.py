from selenium import webdriver
from time import sleep
import sys
import urllib.request

class newYoutubeTab:
    def __init__(self, songName):
        # Chrome general config
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

        #Si hay que buscar manualmente el driver:
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver/chromedriver", options=self.options)

        # YouTube search
        self.driver.get("https://youtube.com")
        sleep(0.1)
        self.driver.find_element_by_xpath('//input[@id= "search"]').send_keys(songName)
        self.driver.find_element_by_xpath('//button[@id="search-icon-legacy"]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//ytd-video-renderer').click()
        self.url = self.driver.current_url

        # Music download page search
        self.driver.get("https://ytmp3.cc/en13/")
        sleep(0.1)
        self.driver.find_element_by_xpath('//input[@name="video"]').send_keys(self.url)
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()
        sleep(0.5)

        # Create link and name the file
        download_link = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').get_property("href")
        self.file_name = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[1]').get_attribute('innerHTML')
        self.driver.close()
        self.driver.quit()

        self.key = input('¿Descargar ' + "\033[1m" + self.file_name + "\033[0m" + '? (y)')
        if self.key == "":
            urllib.request.urlretrieve(download_link, '/INSERT_MUSIC_FOLDER' + self.file_name + '.mp3')
        else:
            if self.key[0] == 'y' or self.key[0] == 'Y' or self.key == "":
                urllib.request.urlretrieve(download_link, '/INSERT_MUSIC_FOLDER' + self.file_name + '.mp3')
            else:
                print("Operación cancelada")

song = sys.argv[1]
bot = newYoutubeTab(song)
