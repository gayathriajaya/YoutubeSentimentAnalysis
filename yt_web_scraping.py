from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def yt_scrapper(url):
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-extensions")

    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    comments = []
    writers = []
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    time.sleep(5)
    try:
        driver.find_element(By.XPATH, '//button[contains(@aria-label,"Reject")]').click()
        time.sleep(7)
    except:
        pass

    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button'))).click()

    # pause.click()
    # time.sleep(0.2)

    driver.execute_script("window.scrollTo(0,500)")
    time.sleep(5)

    video_title = driver.find_element(By.XPATH, '//*[@id="title"]//h1/*').text
    video_owner = driver.find_element(By.XPATH, '//*[@id="top-row"]//*[@id="text"]/a').text
    views = driver.find_element(By.XPATH, '//*[@id="info"]//span [1]').text
    total_comments = driver.find_element(By.XPATH, '//h2[@id="count"]//span').text

    print('Video Title: ', video_title)
    print('Video Owner: ', video_owner)
    print('Video number of views: ', views)
    print('Video total comments: ', total_comments)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    # comment_count = driver.find_element(By.XPATH,'//h2[@id="count"]').text.split()[0]
    while True:
        # Scroll down till "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(4)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



    comments_ele = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
    writer_ele = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')

    for i in range(len(comments_ele)):
        comments.append(comments_ele[i].text)
        writers.append(writer_ele[i].text)
    driver.quit()

    yt_comments = {'Writer': writers, 'Comment': comments}
    yt_comment_df = pd.DataFrame(yt_comments)
    comments_file = yt_comment_df.to_csv('Youtube_comments.csv')

    # comments_file = pd.read_csv('Youtube_comments.csv')

    return comments_file, video_title, video_owner, views, total_comments
