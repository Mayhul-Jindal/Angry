import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser(description='Stream music from youtube on command line interface\n')
parser.add_argument('-pm' , '--play_music' , help='Enter name of the music you want to  play after -pm \"name_of_music\"')
# parser.add_argument('-pp' , '--play_playlist' , help='Play you playlist after -pp my')
args = parser.parse_args()
#---------------------------

options = Options()
options.add_argument('--Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(r'C:\Users\mayhul_jindal\Downloads\chromedriver_win32\chromedriver')
#---------------------------

def init_play_music():
    driver.get(f'https://www.youtube.com/results?search_query={args.play_music}')
    links = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.ID, "video-title")))
    for i in range(3):
        print(f'[{i+1}]: {links[i].get_attribute("title")}')
    while  True:
        ans = int(input('Enter your song:- '))
        if 0<ans <=3: 
            driver.find_element_by_xpath(f'/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{ans}]/div[1]/div/div[1]/div/h3/a').click()
            break
        else:
            print('enter valid input')

# login ni hora bc
def init_play_playlist():
    driver.get('https://www.youtube.com/feed/library')
    print('entered')
    driver.implicitly_wait(5)
    links = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , 'yt-simple-endpoint.style-scope.ytd-grid-playlist-renderer')))
    print(links)
    for i in range(len(links)):
        print(f'[{i+1}]: {links[i].get_attribute("title")}')
    while True:
        ans = int(input('Enter your playlist:- '))
        if 0<ans<len(links): 
            driver.find_element_by_xpath(f'/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[3]/div[3]/ytd-shelf-renderer/div[1]/div[2]/ytd-grid-renderer/div[1]/ytd-grid-playlist-renderer[{ans}]/h3/a').click()
            break
        else:
            print('enter valid input')

if args.play_music:
    init_play_music()
# elif args.play_playlist:
#     init_play_playlist()
else:
    driver.quit()

def play():
    driver.execute_script("document.getElementsByTagName('video')[0].play()")
def pause():
    driver.execute_script("document.getElementsByTagName('video')[0].pause()")
def stop():
    driver.quit()

while True:
    inp = input()
    if inp == '$play':
        print('Resumed.')
        play()
    elif inp == '$pause':
        print('Paused.')
        pause()
    elif inp == '$stop':
        print('Exiting the music player')
        stop()
        break
    else:
        pass
