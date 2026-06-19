import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import random

st.set_page_config(page_title="철인 3종 시뮬레이터", layout="wide")
st.title("🏃‍♂️ 현실 고증 실시간 철인 3종 시뮬레이션 (2,000명)")

if 'players_db' not in st.session_state:
    names = ["김철수", "이영희", "박민수", "최진우", "정다은", "홍길동", "이수민", "강호동", "유재석", "신동엽"]
    sample_data = []
    for i, name in enumerate(names, start=101):
        status = random.choice(["FINISH", "FINISH", "RACING", "RACING"])
        total_time = f"02:{random.randint(0,59):02d}:{random.randint(0,59):02d}" if status == "FINISH" else "00:00:00"
        sample_data.append({"player_id": i, "name": name, "age": random.randint(20, 85), "total_time": total_time, "status": status})
    st.session_state['players_db'] = sample_data

with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    game_speed = st.slider("🏃‍♂️ 경기 진행 속도", 0.5, 3.0, 1.5, 0.5)
    skill_gap = st.slider("⚡ 선수간 기량 격차", 1.0, 5.0, 3.0, 0.5)
    start_interval = st.slider("⏱️ 조별 출발 간격 (초)", 0.2, 2.0, 0.4, 0.1)

html_filename = "race.html"
if os.path.exists(html_filename):
    with open(html_filename, "r", encoding="utf-8") as f:
        html_template = f.read()
    rendered_html = html_template.replace("__SPEED_VAL__", str(game_speed)).replace("__GAP_VAL__", str(skill_gap)).replace("__INTERVAL_VAL__", str(start_interval))
    components.html(rendered_html, height=280, scrolling=False)
else:
    st.error(f"❌ '{html_filename}' 파일이 없습니다. 파이썬 파일과 같은 폴더에 넣어주세요.")

st.markdown("---")
st.subheader("🏆 명예의 전당 - 연령대별 완주자 성적 리스트")

df_all = pd.DataFrame(st.session_state['players_db'])
df_finished = df_all[df_all['status'] == 'FINISH'].copy()

if not df_finished.empty:
    age_bins = [20, 30, 40, 50, 60, 70, 100]
    age_labels = ['20대', '30대', '40대', '50대', '60대', '70대 이상']
    df_finished['연령대'] = pd.cut(df_finished['age'], bins=age_bins, labels=age_labels, right=False)
    df_finished['그룹 순위'] = df_finished.groupby('연령대', observed=False)['total_time'].rank(method='min').astype(int)
    df_finished = df_finished.sort_values(by=['연령대', '그룹 순위'])
    df_finished = df_finished.rename(columns={'player_id': '선수 번호', 'name': '이름', 'age': '나이', 'total_time': '최종 기록', 'status': '상태'})
    
    show_columns = ['연령대', '그룹 순위', '선수 번호', '이름', '나이', '최종 기록']
    st.dataframe(df_finished[show_columns].set_index(['연령대', '그룹 순위']), width='stretch')
    
    st.markdown("##### 🔍 특정 연령대만 모아보기")
    selected_group = st.selectbox("조회할 연령대를 선택하세요", age_labels)
    filtered_df = df_finished[df_finished['연령대'] == selected_group].set_index('그룹 순위')
    st.dataframe(filtered_df[['선수 번호', '이름', '나이', '최종 기록']], width='stretch')
else:
    st.warning("⏳ 아직 완주한 선수가 없습니다.")
