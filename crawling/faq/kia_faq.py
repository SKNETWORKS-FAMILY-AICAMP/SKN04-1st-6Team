import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml

def kia_faq_crawl() ->pd.DataFrame:
    '''
    기아 홈페이지에서 질문과 답변을 데이터프레임 형식으로 출력합니다
    출력값은 데이터프레임 형식입니다
    '''
    #기아 홈페이지 접속
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.kia.com/kr/customer-service/center/faq')
    time.sleep(5)
    bs = BeautifulSoup(driver.page_source, 'lxml')

    #질문과 답변 생성
    kia_questions = []
    kia_answers = []
    #질문 크롤링
    page_questions = bs.select('.cmp-accordion__title')
    for question in page_questions:
        kia_questions.append(question.text.strip())
    print('question crawled')

    #답변크롤링
    kia_answer = bs.select('.faqinner__wrap div')
    for answer in kia_answer:
        kia_answers.append(answer.text.strip())
    kia_answers = [s for s in kia_answers if s!='']
    print('answer crawled')
    
    #데이터프레임 만들기
    data_list=[]
    for question, answer in zip(kia_questions, kia_answers):
        temp = {'id':'K', 'question':question,'answer':answer}
        data_list.append(temp)
    return pd.DataFrame(data_list)
