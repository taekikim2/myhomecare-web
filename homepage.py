import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# [핵심] 우리가 만든 파일들을 불러옵니다!
import prompts      # 블로그 글쓰기 대본
import calculator   # 견적 계산기

# 1. 페이지 설정
st.set_page_config(page_title="마이홈케어플러스", page_icon="🏠", layout="wide")

# 2. 스타일 설정
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .kakao-btn {
        background-color: #FEE500; color: #3C1E1E; padding: 10px 20px;
        border-radius: 10px; text-decoration: none; font-weight: bold;
        display: block; text-align: center; margin: 10px 0;
    }
    .service-box {
        background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #1E3A8A;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.markdown("""<a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">💬 카카오톡 무료 상담</a>""", unsafe_allow_html=True)
    st.markdown("### 📞 010-6533-3137")

# --- 구글 시트 연결 함수 ---
def add_to_sheet(date, place, work, price, note):
    try:
        raw_key = st.secrets["GOOGLE_SHEET_KEY"]
        try:
            json_key = json.loads(raw_key, strict=False)
        except json.JSONDecodeError:
            json_key = json.loads(raw_key.replace('\n', '\\n'), strict=False)

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
        client = gspread.authorize(creds)
        sheet = client.open("마이홈케어 시공장부").sheet1
        sheet.append_row([str(date), place, work, price, note])
        return True
    except Exception as e:
        st.error(f"장부 저장 실패: {e}")
        return False

# === 메인 화면 기능들 ===

if menu == "홈":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    try: st.image("after.jpg", use_container_width=True)
    except: st.info("사진 필요")
    st.info("💧 누수 탐지 | 🛁 욕실 리모델링 | 🛠️ 종합 집수리")

# === [업그레이드된 서비스 소개] ===
elif menu == "서비스 소개":
    st.header("🛠️ 마이홈케어플러스 전문 시공")
    st.write("부산/경남 대표 홈케어! 아래 모든 항목을 직접 시공합니다.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💧 누수 & 방수 전문")
        st.markdown("""
        <div class="service-box">
            <b>1. 누수 출장 점검</b><br>
            - 정확한 원인 파악 및 전문가 소견서 발급
        </div>
        <div class="service-box">
            <b>2. 누수 탐지 (책임 시공)</b><br>
            - 청음식/가스식 첨단 장비 보유<br>
            - 못 찾으면 비용 0원!
        </div>
        <div class="service-box">
            <b>3. 욕실 방수 공사</b><br>
            - 철거부터 방수, 타일 마감까지 원스톱 해결
        </div>
        <div class="service-box">
            <b>4. 외부 창틀 로프 코킹</b><br>
            - 아파트 베란다 빗물 누수 완벽 차단 (로프 작업)
        </div>
        <div class="service-box">
            <b>5. 욕조 배수구 교체</b><br>
            - 욕조 파손 없이 배수구만 교체하는 특수 기술
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🛁 생활 설비 & 인테리어")
        st.markdown("""
        <div class="service-box">
            <b>6. 도배 (실크/합지)</b><br>
            - 부분 도배부터 전체 도배까지 깔끔한 마감
        </div>
        <div class="service-box">
            <b>7. 각종 수전(수도꼭지) 교체</b><br>
            - 주방, 세면대, 샤워기, 베란다 수전 등
        </div>
        <div class="service-box">
            <b>8. 양변기 교체</b><br>
            - 치마형, 투피스 등 최신 도기 설치 및 폐기물 처리
        </div>
        <div class="service-box">
            <b>9. 샤워기 설치</b><br>
            - 해바라기 샤워기, 선반형 샤워기 설치
        </div>
        <div class="service-box">
            <b>10. 환풍기 교체</b><br>
            - 힘 쎈 환풍기, 댐퍼형(냄새 차단) 환풍기 교체
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 이 외에도 집수리와 관련된 모든 상담이 가능합니다.")

elif menu == "시공 갤러리":
    st.header("✨ 시공 전/후 비교")
    try:
        image_comparison(img1="before.jpg", img2="after.jpg", label1="Before", label2="After", width=700, in_memory=True)
    except: st.error("사진 파일 필요")

elif menu == "출장 지역":
    st.header("📍 출장 가능 지역")
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    folium.Circle(location=[35.1796, 129.0756], radius=20000, color="red", fill=True, fill_opacity=0.1).add_to(m)
    st_folium(m, width=800, height=500)

elif menu == "견적 문의":
    # calculator.py 파일에 있는 기능을 실행합니다!
    calculator.show_estimate()

# === [관리자 모드] ===
elif menu == "🔒 관리자 모드":
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        tab1, tab2 = st.tabs(["📝 블로그 글쓰기", "📊 시공 장부 적기"])
        
        with tab1:
            st.subheader("블로그 포스팅 (Gemini 2.5)")
            with st.form("blog_form"):
                col1, col2 = st.columns(2)
                with col1:
                    topic = st.selectbox("공사 종류", ["누수 탐지", "욕실 방수", "수전 교체", "화장실 리모델링", "기타"])
                    location = st.text_input("현장 위치", "부산 해운대구 좌동")
                detail = st.text_area("작업 내용", height=100)
                submit_blog = st.form_submit_button("글 생성")
                
                if submit_blog:
                    try:
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        final_prompt = prompts.get_blog_prompt(topic, location, detail)
                        with st.spinner("AI가 글을 쓰는 중..."):
                            response = model.generate_content(final_prompt)
                            st.code(response.text)
                    except Exception as e: st.error(f"에러: {e}")

        with tab2:
            st.subheader("오늘의 매출 장부")
            with st.form("sheet_form"):
                date = st.date_input("날짜")
                s_place = st.text_input("현장명")
                s_work = st.text_input("시공 내용")
                s_price = st.number_input("받은 금액 (원)", step=10000)
                s_note = st.text_input("비고")
                
                submit_sheet = st.form_submit_button("💾 장부에 저장하기")
                
                if submit_sheet:
                    with st.spinner("엑셀에 적는 중..."):
                        if add_to_sheet(date, s_place, s_work, s_price, s_note):
                            st.success(f"✅ 저장 완료! {s_price}원 입력됨.")