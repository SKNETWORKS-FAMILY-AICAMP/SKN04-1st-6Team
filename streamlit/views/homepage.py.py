import pandas as pd
import json
import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우 'Malgun Gothic' 폰트를 사용
plt.rcParams['axes.unicode_minus'] = False 

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
            'count': int(item.get('DT').replace(',', '')),
            'type': item.get('C3_NM'),
            'usage': item.get('ITM_NM'),
            'date': item.get('PRD_DE')
        }
        total_car_list.append(car_)
    return pd.DataFrame(total_car_list)

st.title('차종 등록 대수 조회기')

start_date = st.text_input('시작 날짜 (YYYYMM 형식):', '202201')
end_date = st.text_input('종료 날짜 (YYYYMM 형식):', '202407')

if st.button('데이터 조회'):
    if start_date and end_date:
        df = registrated_car_crawler(start_date, end_date)
        if not df.empty:
            st.write(f'{start_date}부터 {end_date}까지의 차량 등록 데이터')
       
            st.dataframe(df)
            
            df['date'] = pd.to_datetime(df['date'], format='%Y%m')
            df['date_str'] = df['date'].dt.strftime('%Y-%m')

            # 지역별 등록 대수 차트
            st.subheader('지역별 등록 대수')
            region_count = df.groupby(['date_str', 'region'])['count'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            bar_plot = sns.barplot(x='region', y='count', data=region_count, palette='tab10')

            # 바의 너비 조정
            for bar in bar_plot.patches:
                bar.set_width(0.4)  # 바 두께 조정

            # x축 레이블을 중앙에 맞추기
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.title('지역별 등록 대수', fontsize=14)
            plt.ylabel('등록 대수', fontsize=12)
            plt.xlabel('지역', fontsize=12)

            # 레이아웃 조정
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)  # x축 레이블과 그래프 사이의 간격 조정
            plt.ticklabel_format(style='plain', axis='y')
            plt.legend([],[], frameon=False)  # 레전드 제거
            st.pyplot(plt)

            # 용도별 등록 대수 차트
            st.subheader('용도별 등록 대수')
            usage_count = df.groupby(['date_str', 'usage'])['count'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            bar_plot = sns.barplot(x='usage', y='count', data=usage_count, palette='tab10')

            # 바의 너비 조정
            for bar in bar_plot.patches:
                bar.set_width(0.4)  # 바 두께 조정

            # x축 레이블을 중앙에 맞추기
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.title('용도별 등록 대수', fontsize=14)
            plt.ylabel('등록 대수', fontsize=12)
            plt.xlabel('용도', fontsize=12)

            # 레이아웃 조정
            plt.tight_layout()
            plt.ticklabel_format(style='plain', axis='y')
            st.pyplot(plt)
            
            # 차종별 등록 대수 차트
            st.subheader('차종별 등록 대수')
            vehicle_type_count = df.groupby(['date_str', 'type'])['count'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            bar_plot = sns.barplot(x='type', y='count', data=vehicle_type_count, palette='tab10')

            # 바의 너비 조정
            for bar in bar_plot.patches:
                bar.set_width(0.4)  # 바 두께 조정

            # x축 레이블을 중앙에 맞추기
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.title('차종별 등록 대수', fontsize=14)
            plt.ylabel('등록 대수', fontsize=12)
            plt.xlabel('차종', fontsize=12)

            # 레이아웃 조정
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)  # x축 레이블과 그래프 사이의 간격 조정
            plt.ticklabel_format(style='plain', axis='y')
            plt.legend([],[], frameon=False)  # 레전드 제거
            st.pyplot(plt)

        else:
            st.write('데이터가 없습니다.')
    else:
        st.write('날짜를 입력해 주세요.')
