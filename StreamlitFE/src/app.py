import streamlit as st
from background import set_background
from pubgstats import PUBGStatsApp
from main import page1,page2

#세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'page1'

# 페이지 전환 함수
def navigate_to(page):
    st.session_state.page = page

if __name__ == '__main__':
    # 이미지 파일 경로 설정
    image_path = '../static/images/battleground1.png'
    # 배경 이미지 설정 함수 호출
    set_background(image_path)
    # 현재 페이지에 따라 다른 UI를 표시합니다.
    if st.session_state.page == 'page1':
        page1(navigate_to)
    elif st.session_state.page == 'page2':
        page2(navigate_to)


