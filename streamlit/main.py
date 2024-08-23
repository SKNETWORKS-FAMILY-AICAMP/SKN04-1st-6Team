import streamlit as st
from streamlit_option_menu import option_menu
from views.car_faq_page import car_faq_page


with st.sidebar:
    choice = option_menu("Menu", ["홈","Q&A"],
                         icons=['house', 'question-circle'],
                         
    )

if choice == '홈':
    pass

if choice == "Q&A":
    car_faq_page()
