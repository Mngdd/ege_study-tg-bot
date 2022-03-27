from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # чтоб не качать 24/7 новые драйвера хрома
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image, ImageOps


def get_website_screenshot(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # не открывать окно хрома
    chrome_options.add_argument('--start-maximized')  # фул скрин

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    time.sleep(2)
    print('searching for task...')
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
    element.screenshot('task_ege_math.png')
    driver.quit()
    ImageOps.expand(Image.open('task_ege_math.png'), border=10, fill='white').save('task_ege_math.png')
    return 'task_ege_math.png'


# get_website_screenshot('https://math-ege.sdamgia.ru/problem?id=26662')
