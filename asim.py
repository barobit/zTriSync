import streamlit as st
import streamlit.components.v1 as components
import os

# =========================================================================
# 1. 스트림릿 대시보드 기본 환경 설정 (와이드 레이아웃)
# =========================================================================
st.set_page_config(page_title="철인 3종 시뮬레이터", layout="wide")
st.title("🏃‍♂️ 현실 고증 실시간 철인 3종 시뮬레이션 (2,000명)")

# =========================================================================
# 2. [사이드바 패치] 슬라이더 조작 메뉴를 왼쪽 사이드바로 이동 (접고 펴기 기능 자동 지원)
# =========================================================================
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    st.write("메뉴를 숨기려면 왼쪽 상단의 **<** 버튼을 누르세요.")
    st.markdown("---")
    
    # 사이드바 전용 슬라이더 컴포넌트 선언
    game_speed = st.slider("🏃‍♂️ 경기 진행 속도", 0.5, 3.0, 1.5, 0.5)
    skill_gap = st.slider("⚡ 선수간 기량 격차", 1.0, 5.0, 3.0, 0.5)
    start_interval = st.slider("⏱️ 조별 출발 간격 (초)", 0.2, 2.0, 0.4, 0.1)

# =========================================================================
# 3. 외부 race.html 자바스크립트 그래픽 파일 연동 엔진 가동
# =========================================================================
html_filename = "race.html"

if os.path.exists(html_filename):
    with open(html_filename, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    # 사이드바로 이동한 파이썬 변수를 HTML 내부 치환 태그와 실시간 교체 매핑
    rendered_html = html_template.replace(
        "__SPEED_VAL__", str(game_speed)
    ).replace(
        "__GAP_VAL__", str(skill_gap)
    ).replace(
        "__INTERVAL_VAL__", str(start_interval)
    )
    
    # 캔버스 박스 규격에 맞춰 아이프레임 상자 높이를 깔끔하게 밀착 정렬
    components.html(rendered_html, height=260, scrolling=False)
else:
    st.error(f"❌ '{html_filename}' 파일이 같은 폴더에 없습니다. 파이썬 파일과 같은 자리에 복사해 주세요.")
