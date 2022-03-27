from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # чтоб не качать 24/7 новые драйвера хрома
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image, ImageOps


def get_website_screenshot(url, obj, usr_id, rand_num):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # не открывать окно хрома
    chrome_options.add_argument('--start-maximized')  # фул скрин

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    time.sleep(2)
    print('task search...')
    try:
        element = driver.find_element(By.CLASS_NAME, "nobreak")
    except:
        print(f'GOT ERROR AT {url}')
        return 'error_pic.png'
    print('maximizing the window...')
    width = 2560
    height = 1440
    driver.set_window_size(width, height)
    time.sleep(2)
    print('taking a screenshot!')
    name = f'task-{obj}-{usr_id}_{rand_num}.png'
    element.screenshot(name)
    driver.quit()
    ImageOps.expand(Image.open(name), border=10, fill='white').save(name)
    return name
