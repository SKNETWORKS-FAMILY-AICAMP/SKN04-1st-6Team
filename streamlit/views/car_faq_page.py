import streamlit as st
import re
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def fetch_qa_data():
    # 데이터베이스에서 Q&A 데이터 가져오기
    conn = st.connection('postgresql', type='sql')
    df = conn.query('SELECT * FROM car_corp')
    df1 = conn.query('SELECT * FROM car_faq')
    return df, df1

def process_qa_data(df):
    # 데이터프레임을 딕셔너리 형태로 변환
    qa_data = {'K': [], 'H': []}
    for _, row in df.iterrows():
        qa_data[row['id']].append({
            "question": row['question'],
            "answer": row['answer']
        })
    return qa_data

def car_faq_page():
    st.markdown("""
    <style>
        .stButton > button {
        width: 100%;
        height: 60%;
        font-size: 22px;
        margin-bottom: 10px;
        border: 1px;}
    </style>
    """, unsafe_allow_html=True)
    st.title('제조사별 Q&A')

    if 'active_qa' not in st.session_state:
        st.session_state.active_qa = None

    # 데이터베이스에서 Q&A 데이터 가져오기
    df_corp, df_faq = fetch_qa_data()
    qa_data = process_qa_data(df_faq)

    # 버튼 생성 및 토글 기능 구현
    if st.button('현대 Q&A'):
        if st.session_state.active_qa == 'H':
            st.session_state.active_qa = None
        else:
            st.session_state.active_qa = 'H'

    if st.button('기아 Q&A'):
        if st.session_state.active_qa == 'K':
            st.session_state.active_qa = None
        else:
            st.session_state.active_qa = 'K'

    # 검색 기능
    if st.session_state.active_qa:
        brand_name = '현대' if st.session_state.active_qa == 'H' else '기아'
        search_query = st.text_input('🔍Search:', key=f'search_{st.session_state.active_qa}')
        
        if search_query:
            st.subheader(f"{brand_name} 검색 결과")
            found = False
            for qa in qa_data[st.session_state.active_qa]:
                # 문자열로 변환하여 검색
                question = str(qa['question'])
                answer = str(qa['answer'])
                if re.search(search_query, question, re.IGNORECASE) or re.search(search_query, answer, re.IGNORECASE):
                    with st.expander(question, expanded=False):
                        st.write(answer)
                    found = True
            if not found:
                st.write("검색 결과가 없습니다.")
        else:
            # 검색어가 없을 때 모든 Q&A 표시
            st.subheader(f"{brand_name} Q&A")
            for qa in qa_data[st.session_state.active_qa]:
                with st.expander(str(qa['question']), expanded=False):
                    st.write(str(qa['answer']))