import streamlit as st
import base64
from background import set_background
st.set_page_config(layout="wide") # 화면 구성 wide

def main():
    # 이미지 파일 경로 설정
    image_path = '../static/images/battleground1.png'
    # 배경 이미지 설정 함수 호출
    set_background(image_path)
    # 상단에 배경 이미지를 설정한 헤더 추가
    st.markdown('<div class="title">Whitezone Analysis Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">Battle Anywhere</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



