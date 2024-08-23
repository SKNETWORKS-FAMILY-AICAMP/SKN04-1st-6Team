import streamlit as st
import re

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
    """ ,unsafe_allow_html = True)
    st.title('제조사별 Q&A')

    if 'active_qa' not in st.session_state:
        st.session_state.active_qa=None

    # 예시 Q&A 데이터
    qa_data = {'HYUNDAI': 
            [{"question": "현대 질문1 (데이터베이스)", "answer": "현대 답변1 (데이터베이스)"},
                {"question": "현대 질문2", "answer": "현대 답변3"},],
                'KIA': [
                    {"question": "기아 질문1 (데이터베이스)", "answer": "기아 답변1 (데이터베이스)"},
                    {"question": "기아 질문2", "answer": "기아 답변4"},]}

    # 버튼 생성 및 토글 기능 구현
    if st.button('현대 Q&A'):
        if st.session_state.active_qa == 'HYUNDAI':
            st.session_state.active_qa = None
        else:
            st.session_state.active_qa = 'HYUNDAI'

    if st.button('기아 Q&A'):
        if st.session_state.active_qa == 'KIA':
            st.session_state.active_qa = None
        else:
            st.session_state.active_qa = 'KIA'

    # 검색 기능
    if st.session_state.active_qa:
        search_query = st.text_input('🔍Search:', key=f'search_{st.session_state.active_qa}')
        
        if search_query:
            st.subheader(f"{st.session_state.active_qa.capitalize()} 검색 결과")
            found = False
            for qa in qa_data[st.session_state.active_qa]:
                if re.search(search_query, qa['question'], re.IGNORECASE) or re.search(search_query, qa['answer'], re.IGNORECASE):
                    with st.expander(qa['question'], expanded=False):
                        st.write(qa['answer'])
                    found = True
            if not found:
                st.write("검색 결과가 없습니다.")
        else:
            # 검색어가 없을 때 모든 Q&A 표시
            st.subheader(f"{st.session_state.active_qa.capitalize()} Q&A")
            for qa in qa_data[st.session_state.active_qa]:
                with st.expander(qa['question'], expanded=False):
                    st.write(qa['answer'])