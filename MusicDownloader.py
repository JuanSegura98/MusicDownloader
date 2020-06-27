from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from getkey import getkey, keys
from time import sleep
import sys
from os import system
import urllib.request
from datetime import datetime


EXECUTABLE_CHROMEDRIVER_PATH = "/usr/bin/chromedriver/chromedriver"
MUSIC_DIRECTORY = '/home/juans/Music/'

# initTime used to timeout if the program hungs

# Interactive menu for -o:
def choosingMenu(list):
    chosen = 0
    key = '\0'
    system('clear')
    while key != '\n':
      print('Select an option:')

      for element in list:
        if element == list[chosen]:		# Outputs chosen object with the format
            print("\033[7m"+element+"\033[27m")
        else:
            print(element)

      key = getkey()
      if key == keys.DOWN and chosen < len(list) - 1:
        chosen += 1
      if key == keys.UP and chosen > 0:
        chosen -= 1

      system('clear')

    return list[chosen]


def trySearchSong(songName, driver, initTime):
    if (datetime.now() - initTime).seconds > 10:
        print("Song not found")
        quit()
    try:
        driver.find_element_by_xpath('//input[@id= "search"]').send_keys(songName)
    except NoSuchElementException:
        trySearchSong(songName, driver, initTime)



def tryVideoRenderer(driver, initTime, vidnumber = 1):
    if (datetime.now() - initTime).seconds > 10:
        print("Problem opening the video in YouTube")
        quit()
    try:
        driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{0}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string'.format(vidnumber)).click()
    except NoSuchElementException:
        tryVideoRenderer(driver, initTime, vidnumber)


def trySendDownloadURL(driver, url, initTime):
    if (datetime.now() - initTime).seconds > 10:
        print("Problem when trying to send the video URL")
        quit()
    try:
        driver.find_element_by_xpath('//input[@name="video"]').send_keys(url)
    except NoSuchElementException:
        trySendDownloadURL(driver, url, initTime)


def tryCreateLink(driver, initTime):
    download_link = 'https://ytmp3.cc/'
    while download_link[:11] == 'https://ytm':      ##### Not robust. Need to find another way (!= download_link[:n] does NOT work)
        if (datetime.now() - initTime).seconds > 10:
            print("Problem when creating the download link")
            quit()
        try:
            download_link = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').get_property(
                "href")
        except NoSuchElementException:
            tryCreateLink(driver, initTime)
    return download_link


class newYoutubeTab:
    def __init__(self, songName, noconfirm = 0):
        # Chrome general config
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

        # If the driver needs to be allocated:
        self.driver = webdriver.Chrome(executable_path=EXECUTABLE_CHROMEDRIVER_PATH, options=self.options)

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

        if not noconfirm:
            # Confirmation
            self.key = input('Download ' + "\033[1m" + self.file_name + "\033[0m" + '? (y)')
            if self.key == "" or self.key == "y" or self.key == "Y":
                urllib.request.urlretrieve(self.download_link, MUSIC_DIRECTORY + self.file_name + '.mp3')
            else:
                print("Canceled operation")

        if noconfirm == 1:  # Direct download
            print("Downloading {}".format(self.file_name))
            urllib.request.urlretrieve(self.download_link, MUSIC_DIRECTORY + self.file_name + '.mp3')


class multipleYoutubeTab:
    def __init__(self, songName):
        # Chrome general config
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

        # If the driver needs to be allocated:
        self.drivers = []
        for j in range(3):
            self.drivers.append(webdriver.Chrome(executable_path=EXECUTABLE_CHROMEDRIVER_PATH, options=self.options))

        # YouTube search
        for j in self.drivers:
            j.get("https://youtube.com")
            self.initTime = datetime.now()
            trySearchSong(songName, j, self.initTime)
            j.find_element_by_xpath('//button[@id="search-icon-legacy"]').click()

        self.video = 1   # Video number (begins at 1)
        self. url = []
        for j in self.drivers:      # We store both the song names and their corresponding URLs
            self.initTime = datetime.now()
            tryVideoRenderer(j, self.initTime, self.video)
            self.url.append(j.current_url)
            self.video += 1

        # Music download page search
        self.video = 1
        for j in self.drivers:
            j.get("https://ytmp3.cc/en13/")
            self.initTime = datetime.now()
            trySendDownloadURL(j, self.url[self.video - 1], self.initTime)
            j.find_element_by_xpath('//input[@type="submit"]').click()
            self.video += 1

        # Create the actual link - file pair which will be downloaded
        self.video = 1
        self.file_name = []
        self.file_link = []
        for j in self.drivers:
            name = 'Please insert a valid video URL'
            while name == 'Please insert a valid video URL':
                name = j.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[1]').get_attribute('innerHTML').strip()

            # self.initTime = datetime.now()
            self.file_name.append(name)
            self.file_link.append(tryCreateLink(j, datetime.now()))
            self.video += 1
            j.close()
            j.quit()

        self.file_name.append('Cancel')		# Adding a cancel option
        chosenSong = choosingMenu(self.file_name)

        if chosenSong == 'Cancel':
            print('Canceling...')
            quit()
        else:
            i = 0
            self.chosen_link = 'Error when choosing the corect link'
            for song in self.file_name:
                if song != chosenSong:
                    i += 1
                else:
                    self.chosen_link = self.file_link[i]
                    break
        if self.chosen_link == 'Error when choosing the corect link':
            print(self.chosen_link)
            quit()
        else:
            print('Downloading ' + chosenSong)
            urllib.request.urlretrieve(self.chosen_link, MUSIC_DIRECTORY + chosenSong + '.mp3')



arguments = len(sys.argv)

if arguments == 1 or sys.argv[1] == '-h' or sys.argv[1] =='-H':      # If no arguments are given or user requests help
    print('Welcome to MusicDownloader for bash! To download a single song, use:')
    print('\tpython3 MusicDownloader.py [options] "<Song name>"')
    print("If the song's or the artist's name is just one word, quotation marks can be ommited.")
    print("\n")
    print("Options:")
    print('-y\t\tFor an interactive-less download')
    print("-o\t\tLets you choose from different results that contain your song name.")
    print("-l <filename>\t\tTo download a list of songs")
    quit()

if arguments == 2:      # Normal mode (no arguments)
    song = sys.argv[1]
    bot = newYoutubeTab(song)
    quit()

if arguments == 3:
    if sys.argv[1] == '-y':     # Accept all (no confirmation asked, direct download)
        song = sys.argv[2]
        bot = newYoutubeTab(song, 1)

    if sys.argv[1] == '-l':     # From a list (file with individual songs in each line. Automatic -y
        file = str(sys.argv[2])
        f = open(file, "r")
        for line in f:
            if len(line) > 2:
                print("Searching {}...".format(line))
                bot = newYoutubeTab(line, 1)

    if sys.argv[1] == '-o':     # Extended option. It presents you the 3 top results of your query and allows you to choose
        song = sys.argv[2]
        bot = multipleYoutubeTab(song)

    quit()

