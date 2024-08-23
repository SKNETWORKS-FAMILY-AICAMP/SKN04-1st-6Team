import pandas as pd
import json
import requests
import streamlit as st

def registrated_car_crawler(start_date='202201', end_date='202407'):
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=Mjc4NzI4OThmZWZiZmVmZjczMDQyNzg4MmZkNjBkYTg=&itmId=13103873443T1+13103873443T2+13103873443T3+13103873443T4+&objL1=ALL&objL2=13102873443B.0002+&objL3=13102873443C.0001+13102873443C.0002+13102873443C.0003+13102873443C.0004+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe={start_date}&endPrdDe={end_date}&outputFields=NM+ITM_NM+UNIT_NM+PRD_DE+&orgId=116&tblId=DT_MLTM_5498'
    response = requests.get(url)
    results = json.loads(response.text)
    total_car_list = []
    for item in results:
        if item.get('ITM_NM') == '계':
            continue
        car_ = {
            'region': item.get('C1_NM'),
            'count': item.get('DT'),
            'type': item.get('C3_NM'),
            'usage': item.get('ITM_NM'),
            'date': item.get('PRD_DE')
        }
        total_car_list.append(car_)
        
    return pd.DataFrame(total_car_list)

# Streamlit UI
st.title('차종 등록 대수 조회기')

# 사용자 입력 받기
start_date = st.text_input('시작 날짜 (YYYYMM 형식):', '202401')
end_date = st.text_input('종료 날짜 (YYYYMM 형식):', '202407')

# 데이터 로드 및 필터링
if st.button('데이터 조회'):
    if start_date and end_date:
        df = registrated_car_crawler(start_date, end_date)
        
        if not df.empty:
            st.write(f'{start_date}부터 {end_date}까지의 차량 등록 데이터')

            # 데이터 표시
            st.dataframe(df)

            # 월별 전국 차량 등록 대수 증감률
            st.subheader('월별 전국 차량 등록 대수 증감추이')
            df['count_int'] = pd.to_numeric(df['count'].str.replace(',', ''), errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
            count_data = df.groupby('date')['count_int'].sum().reset_index()
            count_data.sort_values('date', inplace=True)
            count_data['percent_change'] = count_data['count_int'].diff()
            count_data = count_data.dropna()  # NaN 값 제거
            count_data.rename(columns={'date': '날짜', 'percent_change': '등록대수'}, inplace=True)
            
            st.line_chart(count_data.set_index('날짜')['등록대수'])

            # 차종별 등록 대수 증감률
            st.subheader('차종별 등록 대수 증감추이')
            df['count_int'] = pd.to_numeric(df['count'].str.replace(',', ''), errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
            line_data = df.groupby(['date', 'type'])['count_int'].sum().reset_index()
            line_data.sort_values(['type', 'date'], inplace=True)
            
            # 각 차종에 대해 증감추이 계산
            line_data_pivot = line_data.pivot(index='date', columns='type', values='count_int').fillna(0)
            percent_change_data = line_data_pivot.diff()

            # Streamlit의 line_chart에 전달
            st.line_chart(percent_change_data)
            
            # 용도별 등록 대수 증감률
            st.subheader('용도별 등록 대수 증감추이')
            df['count_int'] = pd.to_numeric(df['count'].str.replace(',', ''), errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
            line_data = df.groupby(['date', 'usage'])['count_int'].sum().reset_index()
            line_data.sort_values(['usage', 'date'], inplace=True)

            # 각 차량의 용도에 대해 증감추이 계산
            line_data_pivot = line_data.pivot(index='date', columns='usage', values='count_int').fillna(0)
            percent_change_data = line_data_pivot.diff()

            # Streamlit의 line_chart에 전달
            st.line_chart(percent_change_data)

        else:
            st.write('데이터가 없습니다.')
    else:
        st.write('날짜를 입력해 주세요.')
