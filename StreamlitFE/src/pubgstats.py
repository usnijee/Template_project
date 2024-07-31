import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from getAPIToJson import getApiToJson
import base64

class PUBGStatsApp:
    def __init__(self):
        self.api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwOTczZWUxMC0wOTZlLTAxM2QtY2NlNi0zMmFkODc5M2Q4OGIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzE4MDM0MTc4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImhlaGViYWxzc2EifQ.ADpdC0UInjTkDeVJXNjtZvMf4rNQAyrzQqWuPGvuteE'

    # base64로 인코딩된 이미지를 반환하는 함수
    def get_base64(self,bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # 상단 배경 이미지를 설정하는 함수
    def set_background(self,png_file):
        bin_str = self.get_base64(png_file)
        css = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                        url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .title {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px;
            color: black;
            font-size: 3rem;
            font-weight: bold;
        }}
        .content {{
            display: grid;
            justify-content: center;
            align-items: center;
            height: 80vh;
            color: black;
            font-size: 2rem;
            font-weight: bold;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def run(self):
        # st.set_page_config(layout="wide")
        image_path = '../static/images/battleground1.png'
        self.set_background(image_path)
        st.title('배틀그라운드 전적검색')
        self.display_ui()

    def display_ui(self):
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                self.platform = st.selectbox("플랫폼 선택:", ["kakao", "steam"])
            with col2:
                self.user_input = st.text_input("닉네임 입력:")

        if self.user_input:
            self.GA = getApiToJson(self.platform, self.user_input, self.api_key)
            self.display_player_stats()

    def display_player_stats(self):
        player_id = self.GA.getPlayerId()
        st.write(player_id)
        
        match_id_list = self.GA.getMatchIdList()
        
        if match_id_list:
            data = self.collect_match_data(match_id_list)
            self.display_data(data)
        else:
            st.write("매치를 찾을 수 없습니다.")

    def collect_match_data(self, match_id_list):
        data = []
        for match_id in match_id_list:
            match_info = self.GA.getOtherApiToJson('/matches/' + match_id)
            match_data = self.parse_match_data(match_info)
            if match_data:
                data.append(match_data)
        return data

    def parse_match_data(self, match_info):
        when_played = match_info['data']['attributes']['createdAt']
        time_event = datetime.strptime(when_played, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - time_event
        days, seconds = time_difference.days, time_difference.seconds
        hours, minutes = seconds // 3600, (seconds % 3600) // 60
        seconds = seconds % 60

        game_mode = self.get_game_mode(match_info['data']['attributes']['gameMode'])
        match_type = self.get_match_type(match_info['data']['attributes']['matchType'])
        map_name = self.get_map_name(match_info['data']['attributes']['mapName'])

        for included_item in match_info['included']:
            try:
                stats = included_item['attributes']['stats']
                if stats['name'] == self.user_input:
                    move_distance = str(round(float(stats['rideDistance']) + float(stats['swimDistance']) + float(stats['walkDistance'])) / 1000)
                    return {
                        '플레이 시각': f"{days}일 {hours}시간 {minutes}분 {seconds}초 전",
                        '모드': game_mode,
                        '타입': match_type,
                        '맵': map_name,
                        '등수': stats['winPlace'],
                        '킬': stats['kills'],
                        '기절': stats['DBNOs'],
                        '피해량': round(stats['damageDealt']),
                        '이동거리': move_distance + "km",
                        '생존 시간': f"{stats['timeSurvived'] // 60:02}:{stats['timeSurvived'] % 60:02}"
                    }
            except KeyError:
                pass
        return None

    def get_game_mode(self, game_mode):
        modes = {'squad': "스쿼드", 'duo': "듀오", 'solo': "솔로"}
        return modes.get(game_mode, game_mode)

    def get_match_type(self, match_type):
        return "경쟁전" if match_type == 'competitive' else match_type

    def get_map_name(self, map_name):
        maps = {
            "Desert_Main": "Miramar",
            "Erangel_Main": "Erangel",
            "Savage_Main": "Sanhok",
            "Neon_Main": "Deston",
            "Tiger_Main": "Taego",
            "DihorOtok_Main": "Karakin",
            "Baltic_Main": "Vikendi"
        }
        return maps.get(map_name, map_name)

    def display_data(self, data):
        df = pd.DataFrame(data)
        for i, row in enumerate(data):
            with st.expander(f"Match {i + 1}"):
                st.write(f"모드: {row['모드']}")
                st.write(f"타입: {row['타입']}")
                st.write(f"맵: {row['맵']}")
                st.write(f"등수: {row['등수']}")
                st.write(f"킬: {row['킬']}")
                st.write(f"기절: {row['기절']}")
                st.write(f"피해량: {row['피해량']}")
                st.write(f"이동거리: {row['이동거리']}")
                st.write(f"생존 시간: {row['생존 시간']}")


