import datetime
from pathlib import Path
from time import sleep
import random
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.config import CONFIG
import logging


def web_wait(by, name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, name))
        )
    except:
        driver.quit()


real_filepath = os.path.split(os.path.realpath(__file__))[0]
os.chdir(real_filepath)

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO)

DRIVER_PATH = Path('../drivers/').joinpath(str(CONFIG['webdriver']['chrome']['version'])).joinpath(
    CONFIG['webdriver']['chrome']['platform'])
DRIVER_PATH_WINDOWS = DRIVER_PATH / 'chromedriver'

options = Options()

if not CONFIG['browser']:
    options.add_argument("--headless")

options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(DRIVER_PATH_WINDOWS, options=options)
driver.get('https://www.plemiona.pl/')

logging.info('Logging in...')
driver.find_element_by_id('user').send_keys(CONFIG['credentials']['login'])
driver.find_element_by_id('password').send_keys(CONFIG['credentials']['password'])
driver.find_element_by_class_name('btn-login').click()

web_wait(By.CLASS_NAME, "world-select")
logging.info('Successfully logged in!')

while (True):
    logging.info(f'Entering world {CONFIG["game"]["world"]}')
    driver.get(f'https://www.plemiona.pl/page/play/pl{CONFIG["game"]["world"]}')
    web_wait(By.CLASS_NAME, "menu")
    sleep_to_date = None
    mission_was_launched = False
    for village in CONFIG["game"]["villages"]:
        max_sleep_time = -1
        script = open(f'../config/{village}.js', 'r').read()
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
                time_str = scav_option.find_element_by_class_name('return-countdown').text
                remaining_time = datetime.datetime.strptime(time_str, '%H:%M:%S')
                remaining_time = datetime.timedelta(hours=remaining_time.hour, minutes=remaining_time.minute,
                                                    seconds=remaining_time.second)
                if remaining_time.total_seconds() > max_sleep_time:
                    sleep_to_date_village = datetime.datetime.now() + remaining_time
                    max_sleep_time = remaining_time.total_seconds()
                if sleep_to_date is None:
                    sleep_to_date = sleep_to_date_village
                elif sleep_to_date > sleep_to_date_village:
                    sleep_to_date = sleep_to_date_village
                logging.info(scav_option.find_element_by_class_name('title').text + ' -> active, ' + time_str + ' left')

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

        scavenge_options.reverse()
        status.reverse()

        if 'active' not in status:
            logging.info('Available to send new scavenger mission!')
            missions_to_launch = [scav_mission for scav_mission, status in zip(scavenge_options, status) if
                                  status == 'inactive']
            for mission in missions_to_launch:
                logging.info('Launching js script')
                driver.execute_script(script)
                mission_was_launched = True
                try:
                    alert = driver.switch_to.alert
                    logging.info(alert.text)
                    alert.accept()
                except:
                    pass
                sleep(1)
                logging.info('Launching mission')
                mission.find_element_by_class_name('btn').click()
                sleep(1)
            continue
        else:
            logging.info('Can not send mission :(')
    try:
        if mission_was_launched:
            sleep_to_date = None
        sleep_time = sleep_to_date - datetime.datetime.now()
        sleep_time_seconds = sleep_time.total_seconds() + random.randint(3, 9)
        logging.info(f'Waiting {sleep_time_seconds} seconds ({sleep_time})')
    except:
        sleep_time_seconds = 5
        logging.info(f'Waiting {sleep_time_seconds} seconds')
    driver.refresh()
    sleep(sleep_time_seconds)
