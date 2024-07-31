import streamlit as st

def page1(navigate_to):
    # 상단에 배경 이미지를 설정한 헤더 추가
    st.markdown('<div class="centered">SSB.GG</div>', unsafe_allow_html=True)
    # 페이지 여백을 설정하는 div 시작
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 5])
        with col1:
            platform = st.selectbox(" ", ["kakao", "steam"], key="platform")
        with col2:
            # user_input = st.text_input("",placeholder="닉네임을 입력하세요", on_change=navigate_to, args=("page2"))
            # if user_input:
            #     st.session_state.user_input = user_input
            #     navigate_to("page2")
            user_input = st.text_input("닉네임 입력", placeholder="닉네임을 입력하세요", key="user_input")
            if st.button("Submit"):
                if user_input:
                    st.session_state.user_input = user_input  # 유저 입력값을 세션 상태에 저장
                    navigate_to("page2")  # 페이지 2로 이동
        st.markdown('</div>', unsafe_allow_html=True)
def page2(navigate_to):
    st.title("Page 2")
    st.write("This is the second page.")
    st.write(f"플랫폼: {st.session_state.get('platform', 'N/A')}")
    st.write(f"닉네임: {st.session_state.get('user_input', 'N/A')}")
    if st.button("Back to Page 1"):
        navigate_to('page1')




