import pandas as pd
import json
import requests
import itertools
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime


def registrated_car_crawler(start_date='202201', end_date='202407'):
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=Mjc4NzI4OThmZWZiZmVmZjczMDQyNzg4MmZkNjBkYTg=&itmId=13103873443T1+13103873443T2+13103873443T3+13103873443T4+&objL1=ALL&objL2=13102873443B.0002+&objL3=13102873443C.0001+13102873443C.0002+13102873443C.0003+13102873443C.0004+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe={start_date}&endPrdDe={end_date}&outputFields=NM+ITM_NM+UNIT_NM+PRD_DE+&orgId=116&tblId=DT_MLTM_5498'
    response = requests.get(url)
    results = json.loads(response.text)
    total_car_list = []
    for item in results:
        if item.get('ITM_NM') == '계':
            continue
        car_ = {}
        car_['region'] = item.get('C1_NM')      
        car_['count'] = int(item.get('DT'))
        car_['type'] = item.get('C3_NM')
        car_['usage'] = item.get('ITM_NM')     
        car_['date'] = datetime.strptime(item.get('PRD_DE'), "%Y%m")
        total_car_list.append(car_)
        
    return pd.DataFrame(total_car_list)