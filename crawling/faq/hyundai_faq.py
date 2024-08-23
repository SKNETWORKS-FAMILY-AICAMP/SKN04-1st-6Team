def hyundai_crawler():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import html
    import time
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    import requests
    from selenium.webdriver import ActionChains


    # 드라이버 초기화 및 웹페이지 열기
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.hyundai.com/kr/ko/e/customer/center/faq')
    
    # 화면 크기 설정 및 스크롤 이동
    driver.set_window_size(1920, 1080)
    time.sleep(0.2)
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.5)

    # FAQ 답변을 담을 리스트 초기화
    hyundai_FAQ = []
    for i in range(1, 10):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div/div/div[3]/section/div[2]/div/div[2]/section/div/div[1]/div[1]/ul/li[{i}]/button/span'))
        )
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1.5)

        # 페이지 번호 가져오기 및 페이지 이동
        bs = BeautifulSoup(driver.page_source, 'lxml')
        button_no = len((bs.select("div.pagenation button")[2:-2]))
        time.sleep(1)
        button_no = 2
        for page in range(1, button_no):
            # 질문지 열고 닫으며, 답변 정보수집하기
            for j in range(1, 11):
                try:
                    # JavaScript로 질문 클릭
                    question_button = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{j}]/button/div')
                    driver.execute_script("arguments[0].click();", question_button)
                    time.sleep(1)

                    # 질문 & 답변 추출
                    bs = BeautifulSoup(driver.page_source, 'lxml')
                    items = bs.select("div.list-wrap div.list-item")
                    
                    for item in items:
                        title = item.select_one("button.list-title .list-content").text.strip()
                        content_element = item.select_one("div.conts")
                        if content_element is not None:
                            content_raw = content_element.decode_contents().strip()
                            content_clean = html.unescape(BeautifulSoup(content_raw, "lxml").text.strip())
                            hyundai_FAQ.append({
                                'id' : "H",
                                'question': title,
                                'answer': content_clean
                            })


                   
                    driver.execute_script("arguments[0].click();", question_button)
                    time.sleep(1)
                    
                except Exception as e:
                    continue
                    # print(f"Error processing question {j}: {e}") # 이 코드만 pass로 처리하면 에러 안 뜰듯
            
            # 다음 페이지로 이동 
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'#app > div.contant-area > section > div.l-container-body > div > div.l-contents-mid > section > div > div:nth-child(3) > div.pagenation.pagenation > div > ul > li:nth-child({page}) > button'))
            )
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(1.5)


    # 드라이버 종료
    driver.quit()
    # 결과 출력
    return pd.DataFrame(hyundai_FAQ)