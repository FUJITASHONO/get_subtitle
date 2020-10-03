def open_file(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from urllib.parse import urljoin
    from urllib.parse import urlparse
    import time
    # Seleniumをあらゆる環境で起動させるChromeオプション
    options = Options()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    # options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

    executable_path = "" #chromedriver.exeのパス
    driver = webdriver.Chrome(executable_path = executable_path) #chromedriverのパス
    driver.get(url)
    time.sleep(20)
    driver.implicitly_wait(10)

    for i in range(0,15):
        html = driver.page_source
        title = driver.title
        #titleを取るのが早すぎると，"Animelon"というタイトルを取ってしまう
        if title == "Animelon":
            print("get Animelon ")
            time.sleep(3)
            pass
        else:
            print(title, end = ",")
            print(url)
            #サーバーエラーになった場合，ファイルopenできないため，もう一度chromeを立ち上げ直す
            try:
                f = open("../data/subtitles/"+str(title)+".tsv", mode = "w", encoding='utf-8',newline='')#保存したファイルのパス
                break
            except:
                driver.close()
                driver.quit()
                time.sleep(5)
                driver = webdriver.Chrome(executable_path = executable_path)#chromedriverのパス
                driver.get(url)
    return title, driver, f

def get_japanese_elements(driver):
    from bs4 import BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    japanese_elements = soup.find_all("span", class_="japanese subtitle")
    return japanese_elements

def get_english_elements(driver):
    from bs4 import BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    engilish_elements=soup.find_all("span", class_="english subtitle")
    return engilish_elements

def get_japanese_text(driver):
    from text_process import Text_process
    import time
    japanese_elements = get_japanese_elements(driver)
    for n in range(0,15): #回数が多いほど確実に字幕が取れるが，計算量が多くなり，時間も長くなる
        if len(japanese_elements) == 0:
            play(driver)
            time.sleep(0.01)
            japanese_elements = get_japanese_elements(driver)
            pause(driver)
        else:
            #print(n) #何回目で字幕が取れたかの確認
            break
    if len(japanese_elements) == 0:
        japanese_text = ""
    else:
        japanese_element = str(japanese_elements[0])
        japanese_text = Text_process.clean_word(Text_process.remove_bracket(japanese_element))
    return japanese_text

def get_english_text(driver):
    from text_process import Text_process
    import time
    english_elements = get_english_elements(driver)
    for n in range(0,15):
        if len(english_elements) == 0:
            play(driver)
            time.sleep(0.01)
            english_elements = get_english_elements(driver)
            pause(driver)
        else:
            #print(n) #何回目で字幕が取れたかの確認
            break
    if len(english_elements) == 0:
        english_text = ""
    else:
        english_element = str(english_elements[0])
        english_text = Text_process.clean_word(Text_process.remove_bracket(english_element))
    return english_text

def judge_finish(former_japanese_text, japanese_text, former_english_text, english_text, driver, url):
    import time
    #取ってきた英語と日本語が前と同じもので，最後60秒に入ったら終了
    if former_japanese_text == japanese_text and former_english_text == english_text:
        for i in range(0,100):
            try:
                current_time_element = driver.find_element_by_css_selector("span[ng-bind='playerValues.currentTime | secondsToTime']")
                current_time = current_time_element.text
                total_time_element = driver.find_element_by_css_selector("span[ng-bind='playerValues.duration | secondsToTime']")
                total_time = total_time_element.text
                diff = diff_time(current_time, total_time)
                if diff < 60:
                    judge = True
                    print("judge_True")
                else:
                    judge = False
                break
            except:
                time.sleep(0.1)
                pass
    #次のEPに入ったら終了
    elif url != driver.current_url:
        judge = True
    else:
        judge = False
    return judge

def diff_time(current_time, total_time):
    current_time_minute = current_time[0:-3]
    current_time_second = current_time[-2:]
    total_time_minute = total_time[0:-3]
    total_time_second = total_time[-2:]
    diff_minute = int(total_time_minute) - int(current_time_minute)
    diff_second = int(total_time_second) - int(current_time_second)
    return diff_minute*60 + diff_second

def play(driver):
    import time
    for c in range(0,2000):
        elements=driver.find_elements_by_class_name("btn")
        click_element = 0
        for e in elements:
            try:
                if e.get_attribute("data-original-title")=="play":
                    click_element = e
                    break
            except:
                pass
        if click_element != 0:
            try:
                click_element.click()
                break
            except:
                pass
        time.sleep(0.01)
    
def pause(driver):
    import time
    for c in range(0,2000):
        elements=driver.find_elements_by_class_name("btn")
        click_element = 0
        for e in elements:
            try:
                if e.get_attribute("data-original-title")=="pause":
                    click_element = e
                    break
            except:
                pass
        if click_element != 0:
            try:
                click_element.click()
                break
            except:
                pass
        time.sleep(0.01)
    
def Next(driver, play_or_pause):
    import time
    for i in range(0,100):
        elements=driver.find_elements_by_class_name("btn")
        next_bottun = 0
        for e in elements:
            try:
                if e.get_attribute("data-original-title") == "next dialogue":
                    next_bottun = e
                    break
            except:
                pass
        if next_bottun != 0:
            try:
                if play_or_pause == "pause":
                    next_bottun.click()
                else:      #Nextボタンが効いてないとき,play,next,pauseを押す．
                    play(driver)
                    time.sleep(0.01)
                    next_bottun.click()
                    pause(driver)
                break
            except:
                pass
        time.sleep(0.01)

class Scrayping:
    def scrayping(url):
        import time
        import re
        import urllib.robotparser
        import numpy as np
        import csv
        
        title, driver, f = open_file(url)
        #念のためtitleがAnimelonではないことを確認
        if title != "Animelon":       
            writer = csv.writer(f, delimiter='\t')
            play_or_pause = "pause"
            #最初の次へボタン
            Next(driver, play_or_pause)
            for i in range(0,100):
                japanese_elements = get_japanese_elements(driver)
                english_elements = get_english_elements(driver)
                #英語か日本語が取れるまでNextボタンを押す
                if len(japanese_elements) !=0 or len(english_elements) != 0:
                    break
                else:
                    time.sleep(0.1)
                    Next(driver, play_or_pause)

            former_japanese_text = [] #一個前の日本語字幕
            former_english_text = [] #一個前の英語字幕
            text_array = [] #字幕配列
            for i in range(0, 10000):
                pair_text =[] #日本語と英語のペア
                #日本語字幕取得
                japanese_text = get_japanese_text(driver)
                pair_text.append(japanese_text)
                #英語字幕取得
                english_text = get_english_text(driver)
                pair_text.append(english_text)

                #最後の字幕かどうかの判定
                if judge_finish(former_japanese_text, japanese_text, former_english_text, english_text, driver, url) == True:
                    break
                    
                #Nextボタンが効いてない(同じ字幕が現れている)とき,play stopを押してから，もう一度pair_textを取る
                if former_japanese_text == japanese_text and former_english_text == english_text or pair_text==["", ""]:
                    play_or_pause = "play"
                    pass
                else:
                    text_array.append(pair_text)
                    play_or_pause = "pause"
                Next(driver, play_or_pause)
                    
                former_japanese_text = japanese_text
                former_english_text = english_text
                
            #ファイル書き込み
            for p in text_array:
                writer.writerow(p)
            driver.close()
            driver.quit()
            f.close()
            time.sleep(20)
        else:
            driver.close()
            driver.quit()
            time.sleep(30)