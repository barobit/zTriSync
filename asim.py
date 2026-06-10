import streamlit as st

# 1. 페이지 레이아웃 가로 확장 설정
st.set_page_config(
    page_title="실시간 철인 3종 시뮬레이터",
    layout="wide"
)

# 2. 메인 안내 타이틀
st.title("🏃‍♂️ 실시간 철인 3종 경기 시뮬레이션 (2,000명)")
st.caption("2000명의 선수가 수영 ➡️ 사이클 ➡️ 마라톤 구간을 차례로 통과합니다. 점 위에 마우스를 올리면 정보가 업데이트됩니다.")

# 3. 레이아웃 분할 (구형/신형 버전 호환을 위해 개수 '2'를 명확하게 선언)
col1, col2 = st.columns(2)
with col1:
    game_speed = st.slider("🏃‍♂️ 경기 진행 속도", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
with col2:
    skill_gap = st.slider("⚡ 선수간 기량 격차", min_value=1.0, max_value=5.0, value=2.5, step=0.5)

# 4. 브라우저 보안 및 파이썬 문법 충돌을 원천 차단한 HTML5/JS 그래픽 코드
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; background-color: #111116; font-family: sans-serif; overflow: hidden; }
        canvas { display: block; background: #1a1a24; border-radius: 8px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); }
        
        #tooltip {
            position: absolute; background: rgba(20, 20, 30, 0.95); color: #fff;
            padding: 12px; border-radius: 8px; font-size: 12px; display: none;
            pointer-events: none; border: 1px solid #4f46e5; min-width: 160px; line-height: 1.5;
        }
        .stage-label {
            position: absolute; top: 15px; font-weight: bold; font-size: 13px;
            color: rgba(255,255,255,0.8); background: rgba(0,0,0,0.6);
            padding: 6px 14px; border-radius: 20px; pointer-events: none;
        }
        #live-box {
            position: absolute; bottom: 15px; left: 15px; background: rgba(0,0,0,0.7);
            padding: 12px; border-radius: 6px; color: #fff; font-size: 13px; min-width: 200px;
            border: 1px solid rgba(255,255,255,0.1); line-height: 1.6;
        }
    </style>
</head>
<body>

    <div class="stage-label" style="left: 2%;">🏊‍♂️ 1구간: 수영</div>
    <div class="stage-label" style="left: 36%;">🚴‍♂️ 2구간: 사이클</div>
    <div class="stage-label" style="left: 70%;">🏃‍♂️ 3구간: 마라톤</div>

    <!-- 실시간 인트라넷 기반 내장형 리더보드 (보안 우회 핵심) -->
    <div id="live-box"></div>
    <div id="tooltip"></div>
    <canvas id="raceCanvas"></canvas>

    <script>
        const canvas = document.getElementById('raceCanvas');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const liveBox = document.getElementById('live-box');

        const DOT_COUNT = 2000;
        const SPEED_MULTIPLIER = __SPEED_VAL__;
        const VARIANCE_FACTOR = __GAP_VAL__;
        
        let athletes = [];
        let hoveredAthlete = null;
        let frameCount = 0;

        function resizeCanvas() {
            canvas.width = window.innerWidth - 40;
            canvas.height = 480;
        }
        resizeCanvas();

        let zone1_end = canvas.width * 0.33;
        let zone2_end = canvas.width * 0.66;

        for (let i = 1; i <= DOT_COUNT; i++) {
            const baseSkill = 0.4 + Math.random() * VARIANCE_FACTOR;
            athletes.push({
                id: i, name: "선수 #" + i,
                x: Math.random() * 50 - 60,
                y: 50 + Math.random() * (canvas.height - 100),
                radius: 2.5,
                swimSpeed: (0.3 + Math.random() * 0.3) * baseSkill * SPEED_MULTIPLIER,
                cycleSpeed: (1.3 + Math.random() * 0.5) * baseSkill * SPEED_MULTIPLIER,
                runSpeed: (0.7 + Math.random() * 0.4) * baseSkill * SPEED_MULTIPLIER,
                stage: 'swim', color: '#38bdf8', distance: 0, rank: i,
                swimTime: null, cycleTime: null, finishTime: null
            });
        }

        function animate() {
            frameCount++;
            ctx.fillStyle = '#111116';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            zone1_end = canvas.width * 0.33;
            zone2_end = canvas.width * 0.66;

            ctx.fillStyle = 'rgba(56, 189, 248, 0.03)'; ctx.fillRect(0, 0, zone1_end, canvas.height);
            ctx.fillStyle = 'rgba(234, 179, 8, 0.02)'; ctx.fillRect(zone1_end, 0, zone2_end - zone1_end, canvas.height);
            ctx.fillStyle = 'rgba(239, 68, 68, 0.02)'; ctx.fillRect(zone2_end, 0, canvas.width - zone2_end, canvas.height);

            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(zone1_end, 0); ctx.lineTo(zone1_end, canvas.height); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(zone2_end, 0); ctx.lineTo(zone2_end, canvas.height); ctx.stroke();

            for (let i = 0; i < DOT_COUNT; i++) {
                let p = athletes[i];
                if (p.stage === 'swim') {
                    p.x += p.swimSpeed; p.y += (Math.sin(frameCount * 0.04 + p.id) * 0.15); p.color = '#38bdf8';
                    if (p.x >= zone1_end) { p.stage = 'cycle'; p.swimTime = (frameCount / 60).toFixed(1) + "초"; }
                } else if (p.stage === 'cycle') {
                    p.x += p.cycleSpeed; p.color = '#eab308';
                    if (p.x >= zone2_end) { p.stage = 'run'; p.cycleTime = (frameCount / 60).toFixed(1) + "초"; }
                } else if (p.stage === 'run') {
                    p.x += p.runSpeed; p.color = '#ef4444';
                    if (p.x >= canvas.width - 15) { p.stage = 'goal'; p.finishTime = (frameCount / 60).toFixed(1) + "초"; p.x = canvas.width - 8; }
                } else if (p.stage === 'goal') { p.color = '#22c55e'; }
                p.distance = p.x;
            }

            if (frameCount % 15 === 0) {
                let sorted = [...athletes].sort((a, b) => b.distance - a.distance);
                for (let r = 0; r < sorted.length; r++) { athletes[sorted[r].id - 1].rank = r + 1; }
                
                let top5 = sorted.slice(0, 5);
                let html = '<div style="font-weight:bold; color:#a7f3d0; margin-bottom:6px;">🏆 REAL-TIME TOP 5</div>';
                top5.forEach((p, idx) => {
                    let icon = p.stage === 'swim' ? '🏊‍♂️' : p.stage === 'cycle' ? '🚴‍♂️' : p.stage === 'run' ? '🏃‍♂️' : '🏁';
                    html += '<div style="display:flex; justify-content:space-between; width:180px;"><span>' + (idx+1) + '위 ' + p.name + '</span><span>' + icon + '</span></div>';
                });
                liveBox.innerHTML = html;
            }

            for (let i = 0; i < DOT_COUNT; i++) {
                let p = athletes[i];
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fillStyle = p.color;
                if (hoveredAthlete && hoveredAthlete.id === p.id) {
                    ctx.arc(p.x, p.y, p.radius + 3, 0, Math.PI * 2); ctx.fillStyle = '#ffffff';
                    ctx.shadowBlur = 12; ctx.shadowColor = '#ffffff';
                }
                ctx.fill(); ctx.shadowBlur = 0;
            }

            if (hoveredAthlete) {
                let cur = athletes[hoveredAthlete.id - 1];
                let stageKo = cur.stage === 'swim' ? '🏊‍♂️ 수영' : cur.stage === 'cycle' ? '🚴‍♂️ 사이클' : cur.stage === 'run' ? '🏃‍♂️ 마라톤' : '🏁 완주!';
                tooltip.innerHTML = `
                    <strong style="color:#67e8f9;">${cur.name}</strong><br/>
                    <b style="color:#facc15;">현재 순위: ${cur.rank}위</b><br/>
                    <div style="border-top:1px solid #334155; margin:5px 0;"></div>
                    종목: ${stageKo}<br/>
                    🏊‍♂️ 수영: ${cur.swimTime || '레이스 중'}<br/>
                    🚴‍♂️ 사이클: ${cur.cycleTime || (cur.stage === 'swim' ? '대기' : '레이스 중')}<br/>
                    🏁 최종 기록: ${cur.finishTime || '진행 중'}
                `;
            }
            requestAnimationFrame(animate);
        }

        canvas.addEventListener('mousemove', function(e) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
            let found = null;
            for (let i = DOT_COUNT - 1; i >= 0; i--) {
                let p = athletes[i];
                if (Math.hypot(p.x - mouseX, p.y - mouseY) < p.radius + 5) { found = p; break; }
            }
            if (found) {
                hoveredAthlete = found; tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 15) + 'px'; tooltip.style.top = (e.clientY + 15) + 'px';
            } else { hoveredAthlete = null; tooltip.style.display = 'none'; }
        });

        animate();
    </script>
</body>
</html>
"""

# 파이썬 고유 에러가 전혀 발생하지 않도록 문자열 타겟 치환(.replace) 처리 방식을 채택합니다.
html_code = html_template.replace("__SPEED_VAL__", str(game_speed)).replace("__GAP_VAL__", str(skill_gap))

st.components.v1.html(html_code, height=520, scrolling=False)
