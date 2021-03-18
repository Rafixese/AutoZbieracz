from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import CONFIG
import logging


def web_wait(by, name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, name))
        )
    except:
        driver.quit()


logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO)

DRIVER_PATH = Path('../drivers/').joinpath(str(CONFIG['webdriver']['chrome']['version'])).joinpath(
    CONFIG['webdriver']['chrome']['platform'])
DRIVER_PATH_WINDOWS = DRIVER_PATH / 'chromedriver'

driver = webdriver.Chrome(DRIVER_PATH_WINDOWS)
driver.get('https://www.plemiona.pl/')

logging.info('Logging in...')
driver.find_element_by_id('user').send_keys(CONFIG['credentials']['login'])
driver.find_element_by_id('password').send_keys(CONFIG['credentials']['password'])
driver.find_element_by_class_name('btn-login').click()
logging.info('Successfully logged in!')

web_wait(By.CLASS_NAME, "world-select")

logging.info(f'Entering world {CONFIG["game"]["world"]}')
driver.get(f'https://www.plemiona.pl/page/play/pl{CONFIG["game"]["world"]}')

web_wait(By.CLASS_NAME, "menu")
while (True):
    for village in CONFIG["game"]["villages"]:
        logging.info(f'Entering village {village}')
        driver.get(
            f'https://pl{CONFIG["game"]["world"]}.plemiona.pl/game.php?village={village}&screen=place&mode=scavenge')
        web_wait(By.CLASS_NAME, "scavenge-option")
        scavenge_options = driver.find_elements_by_class_name('scavenge-option')
        status = []
        logging.info('Status: ')
        for scav_option in scavenge_options:
            try:
                scav_option.find_element_by_class_name('inactive-view')
                status.append('inactive')
                logging.info(scav_option.find_element_by_class_name('title').text + ' -> inactive')
                continue
            except:
                pass

            try:
                scav_option.find_element_by_class_name('active-view')
                status.append('active')
                logging.info(scav_option.find_element_by_class_name('title').text + ' -> active')
                continue
            except:
                pass

            try:
                scav_option.find_element_by_class_name('locked-view')
                status.append('locked')
                logging.info(scav_option.find_element_by_class_name('title').text + ' -> locked')
                continue
            except:
                pass

        if 'active' not in status:
            logging.info('Available to send new scavenger mission!')
        else:
            logging.info('Can not send mission :(')
    logging.info(f'Waiting {CONFIG["bot"]["wait_time"]} seconds.')
    sleep(CONFIG['bot']['wait_time'])
