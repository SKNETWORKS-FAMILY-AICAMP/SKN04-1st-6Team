import pandas as pd
import json
import requests
import streamlit as st
from datetime import datetime

def hompage():
    # Streamlit UI
    st.title('차량 등록 대수 조회기')

    # 사용자 입력 받기
    start_date = st.text_input('시작 날짜 (YYYYMM 형식):', '202401')
    end_date = st.text_input('종료 날짜 (YYYYMM 형식):', '202407')

    #날짜 포맷 변경 YYYYMM -> YYYY-MM
    def format_date(date_str, format: str='%Y년%m월'):
        return datetime.strptime(date_str, '%Y%m').strftime(format)

    # 데이터 로드 및 필터링
    if st.button('조회'):
        if start_date and end_date:
            conn = st.connection('postgresql', type='sql')
            start_date_ = format_date(start_date, '%Y-%m-%d')
            end_date_ = format_date(end_date, '%Y-%m-%d')
            df = conn.query(f"SELECT * FROM registererd_car WHERE date >= '{start_date_}' AND date <= '{end_date_}'")
            #df = registrated_car_crawler(start_date, end_date)
            
            st.divider()

            start_date_formatted = format_date(start_date)
            end_date_formatted = format_date(end_date)

            if not df.empty:
                st.subheader(f'{start_date_formatted}부터 {end_date_formatted}까지의 차량 등록 데이터')


                tabs = st.tabs(['월별 전국', '차종별', '용도별'])
                
                with tabs[0]:
                # 월별 전국 차량 등록 대수 증감추이
                    st.subheader('월별 전국 차량 등록 대수 증감추이')
                    df['count_int'] = pd.to_numeric(df['count'], errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
                    count_data = df.groupby('date')['count_int'].sum().reset_index()
                    count_data.sort_values('date', inplace=True)
                    count_data['percent_change'] = count_data['count_int'].diff()
                    count_data = count_data.dropna()  # NaN 값 제거
                    count_data.rename(columns={'date': '날짜', 'percent_change': '등록대수'}, inplace=True)

                    st.line_chart(count_data.set_index('날짜')['등록대수'])

                with tabs[1]:
                    # 차종별 등록 대수 증감추이
                    st.subheader('차종별 등록 대수 증감추이')
                    df['count_int'] = pd.to_numeric(df['count'], errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
                    line_data = df.groupby(['date', 'type'])['count_int'].sum().reset_index()
                    line_data.sort_values(['type', 'date'], inplace=True)
                    
                    # 각 차종에 대해 증감추이 계산
                    line_data_pivot = line_data.pivot(index='date', columns='type', values='count_int').fillna(0)
                    percent_change_data = line_data_pivot.diff()

                    # Streamlit의 line_chart에 전달
                    st.line_chart(percent_change_data)

                with tabs[2]:    
                    # 용도별 등록 대수 증감추이
                    st.subheader('용도별 등록 대수 증감추이')
                    df['count_int'] = pd.to_numeric(df['count'], errors='coerce')  # 숫자로 변환, 오류는 NaN 처리
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
