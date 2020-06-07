from selenium import webdriver
from time import sleep
import sys
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

# initTime y datetime.now() se usan para terminar el programa con un timeout si tarda mucho con un error

def trySearchSong(songName, driver, initTime):
    if (datetime.now() - initTime).seconds > 10:
        print("Canción no encontrada")
        quit()
    try:
        driver.find_element_by_xpath('//input[@id= "search"]').send_keys(songName)
    except NoSuchElementException:
        trySearchSong(songName, driver, initTime)



def tryVideoRenderer(driver, initTime):
    if (datetime.now() - initTime).seconds > 10:
        print("Problema al abrir el vídeo en YouTube")
        quit()
    try:
        driver.find_element_by_xpath('//ytd-video-renderer').click()
    except NoSuchElementException:
        tryVideoRenderer(driver, initTime)


def trySendDownloadURL(driver, url, initTime):
    if (datetime.now() - initTime).seconds > 10:
        print("Problema al enviar el link del vídeo")
        quit()
    try:
        driver.find_element_by_xpath('//input[@name="video"]').send_keys(url)
    except NoSuchElementException:
        trySendDownloadURL(driver, url, initTime)


def tryCreateLink(driver, initTime):
    download_link = 'https://ytmp3.cc/'
    while download_link[:11] == 'https://ytm':      ##### Muy poco robusto. Hay que encontrar otra forma (!= link descarga[:n] NO sirve)
        if (datetime.now() - initTime).seconds > 10:
            print("Problema al crear el link de descarga")
            quit()
        try:
            download_link = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').get_property(
                "href")
        except NoSuchElementException:
            tryCreateLink(driver, initTime)
    return download_link


class newYoutubeTab:
    def __init__(self, songName):
        # Chrome general config
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

        # Si hay que buscar manualmente el driver:
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver/chromedriver", options=self.options)

        # YouTube search
        self.driver.get("https://youtube.com")

        self.initTime = datetime.now()
        trySearchSong(songName, self.driver, self.initTime)
        self.driver.find_element_by_xpath('//button[@id="search-icon-legacy"]').click()

        self.initTime = datetime.now()
        tryVideoRenderer(self.driver, self.initTime)
        self.url = self.driver.current_url

        # Music download page search
        self.driver.get("https://ytmp3.cc/en13/")
        self.initTime = datetime.now()
        trySendDownloadURL(self.driver, self.url, self.initTime)
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()

        # Create link and name the file
        self.initTime = datetime.now()
        self.download_link = tryCreateLink(self.driver, self.initTime)
        self.file_name = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[1]').get_attribute(
            'innerHTML')
        self.driver.close()
        self.driver.quit()

        self.key = input('¿Descargar ' + "\033[1m" + self.file_name + "\033[0m" + '? (y)')
        if self.key == "":
            urllib.request.urlretrieve(self.download_link, '/home/Music/' + self.file_name + '.mp3')
        else:
            if self.key[0] == 'y' or self.key[0] == 'Y' or self.key == "":
                urllib.request.urlretrieve(self.download_link, '/home/Music/' + self.file_name + '.mp3')
            else:
                print("Operación cancelada")


song = sys.argv[1]
bot = newYoutubeTab(song)
