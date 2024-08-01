import streamlit as st
import requests

def page1to2():
    st.session_state.page = "page2"
    # platform = st.session_state.platform
    # nickname = st.session_state.nickname
    # # Flask로 GET 요청 보내기
    # backend_url = f"http://xn--ip-vc7if6v5las1utzi:5000/user/{platform}/{nickname}"
    # params = {
    #     "platform": platform,
    #     "nickname": nickname
    # }
    # response = requests.get(backend_url, params=params)
    # if response.status_code == 200:
    #     st.session_state.player_stats = response.json()  # 응답 데이터를 JSON 형식으로 파싱하여 세션 상태에 저장
    #     st.write("Data sent successfully!")
    # else:
    #     st.write("Failed to send data.")

