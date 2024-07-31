import streamlit as st
from background import set_background
from pubgstats import PUBGStatsApp

def main():
    # 이미지 파일 경로 설정
    image_path = '../static/images/battleground1.png'
    # 배경 이미지 설정 함수 호출
    set_background(image_path)
    # 상단에 배경 이미지를 설정한 헤더 추가
    st.markdown('<div class="title">Whitezone Analysis Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">Battle Anywhere</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    # 이미지 파일 경로 설정
    image_path = '../static/images/battleground1.png'
    # 배경 이미지 설정 함수 호출
    set_background(image_path)
    # 상단에 배경 이미지를 설정한 헤더 추가
    st.markdown('<div class="centered">SSB.GG</div>', unsafe_allow_html=True)
    # 페이지 여백을 설정하는 div 시작
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 5])
        with col1:
            platform = st.selectbox(" ", ["kakao", "steam"])
        with col2:
            user_input = st.text_input(" ", placeholder="닉네임을 입력하세요")
        st.markdown('</div>', unsafe_allow_html=True)


