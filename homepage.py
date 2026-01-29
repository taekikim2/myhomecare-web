import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
import prompts
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

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
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.markdown("""<a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">💬 카카오톡 무료 상담</a>""", unsafe_allow_html=True)
    st.markdown("### 📞 010-6533-3137")

# --- 구글 시트 연결 함수 (로봇 부르기) ---
def add_to_sheet(date, place, work, price, note):
    try:
        # Secrets에서 키 꺼내기
        json_key = json.loads(st.secrets["GOOGLE_SHEET_KEY"])
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
        client = gspread.authorize(creds)
        
        # 엑셀 파일 열기 (이름이 똑같아야 해요!)
        sheet = client.open("마이홈케어 시공장부").sheet1
        sheet.append_row([str(date), place, work, price, note])
        return True
    except Exception as e:
        st.error(f"장부 저장 실패: {e}")
        return False

# === 메인 기능 ===
if menu == "홈":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    try: st.image("after.jpg", use_container_width=True)
    except: st.info("사진 필요")
    st.info("💧 누수 탐지 | 🛁 욕실 리모델링 | 🛠️ 종합 집수리")

elif menu == "서비스 소개":
    st.header("🛠️ 전문 시공 분야")
    st.write("누수 탐지, 방수 공사, 욕실 리모델링, 수전 교체 등 집수리 전반")

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
    st.header("📝 상담 신청")
    st.write("010-6533-3137 문자/전화 환영")

# === [관리자 모드: 블로그 + 장부] ===
elif menu == "🔒 관리자 모드":
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        
        # 탭을 나눠서 깔끔하게!
        tab1, tab2 = st.tabs(["📝 블로그 글쓰기", "📊 시공 장부 적기"])
        
        # [기능 1] 블로그 글쓰기
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

        # [기능 2] 시공 장부 (NEW!)
        with tab2:
            st.subheader("오늘의 매출 장부")
            with st.form("sheet_form"):
                date = st.date_input("날짜")
                s_place = st.text_input("현장명 (예: 좌동 벽산아파트)")
                s_work = st.text_input("시공 내용 (예: 변기 교체)")
                s_price = st.number_input("받은 금액 (원)", step=10000)
                s_note = st.text_input("비고 (자재비 등)")
                
                submit_sheet = st.form_submit_button("💾 장부에 저장하기")
                
                if submit_sheet:
                    with st.spinner("엑셀에 적는 중..."):
                        if add_to_sheet(date, s_place, s_work, s_price, s_note):
                            st.success(f"✅ 저장 완료! {s_price}원 입력됨.")
                        else:
                            st.error("저장 실패. 설정을 확인하세요.")