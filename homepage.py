import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import io
import pandas as pd
from datetime import datetime
import random # 후기 랜덤으로 보여주기 위해 추가

# 파일 불러오기
import prompts      
import calculator
import watermarker

# 1. 페이지 설정
st.set_page_config(page_title="마이홈케어플러스", page_icon="🏠", layout="wide")

# 2. 디자인(CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    
    .hero-title { font-size: 3rem; color: #1E3A8A; font-weight: 900; line-height: 1.2; margin-bottom: 20px; }
    .hero-subtitle { font-size: 1.3rem; color: #444; font-weight: 500; margin-bottom: 30px; }
    .highlight { color: #d32f2f; font-weight: bold; }

    .feature-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08); text-align: center; border: 1px solid #f0f0f0; height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover { transform: translateY(-5px); }
    .feature-icon { font-size: 3rem; margin-bottom: 15px; }
    .feature-title { font-weight: bold; font-size: 1.2rem; color: #1E3A8A; margin-bottom: 10px; }
    .feature-text { font-size: 1rem; color: #666; line-height: 1.6; }

    /* 후기 카드 스타일 (NEW) */
    .review-card {
        background-color: #FFF8E1; padding: 20px; border-radius: 15px;
        border: 1px solid #FFECB3; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stars { color: #FFD700; font-size: 1.2rem; }
    .review-text { font-size: 1.1rem; font-weight: bold; color: #333; margin: 10px 0; }
    .review-info { font-size: 0.9rem; color: #666; text-align: right; }

    .kakao-btn {
        background-color: #FEE500; color: #3C1E1E; padding: 12px 20px;
        border-radius: 8px; text-decoration: none; font-weight: bold;
        display: block; text-align: center; margin: 10px 0; font-size: 1rem;
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
    st.markdown("부산/경남 집수리의 모든 것")
    st.divider()
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.divider()
    st.markdown("""<a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">💬 카카오톡 무료 상담</a>""", unsafe_allow_html=True)
    st.markdown("### 📞 010-6533-3137")

# --- 구글 시트 연결 설정 ---
def get_google_sheet():
    try:
        raw_key = st.secrets["GOOGLE_SHEET_KEY"]
        try:
            json_key = json.loads(raw_key, strict=False)
        except json.JSONDecodeError:
            json_key = json.loads(raw_key.replace('\n', '\\n'), strict=False)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
        client = gspread.authorize(creds)
        return client.open("마이홈케어 시공장부").sheet1
    except: return None

# [업그레이드] 후기(review)까지 저장하도록 수정
def add_to_sheet(date, place, work, price, note, review):
    sheet = get_google_sheet()
    if sheet:
        try:
            # 6번째 칸(후기)까지 저장
            sheet.append_row([str(date), place, work, price, note, review])
            return True
        except: return False
    return False

def load_data():
    sheet = get_google_sheet()
    if sheet:
        try:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except: return pd.DataFrame()
    return pd.DataFrame()

# === [메인 화면] ===
if menu == "홈":
    hero_col1, hero_col2 = st.columns([4, 6], gap="large")
    with hero_col1:
        st.markdown('<h1 class="hero-title">지긋지긋한 누수,<br>확실하게 잡습니다.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">부산/경남 1등 홈케어 전문가<br><span class="highlight">"못 고치면 10원도 받지 않겠습니다."</span></p>', unsafe_allow_html=True)
        st.write("") 
        st.info("💡 지금 바로 전문가와 상담하세요!")
        st.markdown("### 📞 010-6533-3137 (긴급출동)")
    with hero_col2:
        st.write("")
        tab1, tab2, tab3 = st.tabs(["🛁 욕실 리모델링", "💧 누수 탐지", "🧱 방수 공사"])
        with tab1:
            try: image_comparison(img1="case1_before.jpg", img2="case1_after.jpg", label1="철거 전", label2="리모델링 완료", width=800, in_memory=True)
            except: st.warning("case1_before.jpg, case1_after.jpg 사진을 올려주세요!")
        with tab2:
            try: image_comparison(img1="case2_before.jpg", img2="case2_after.jpg", label1="누수 피해", label2="탐지 및 복구", width=800, in_memory=True)
            except: st.warning("case2_before.jpg, case2_after.jpg 사진을 올려주세요!")
        with tab3:
            try: image_comparison(img1="case3_before.jpg", img2="case3_after.jpg", label1="방수 전", label2="방수 완료", width=800, in_memory=True)
            except: st.warning("case3_before.jpg, case3_after.jpg 사진을 올려주세요!")
    
    st.divider()

    # === [NEW] 고객 후기 섹션 ===
    st.subheader("⭐⭐⭐⭐⭐ 고객님들의 찐 후기")
    
    # 데이터 가져오기
    df = load_data()
    
    if not df.empty and '후기' in df.columns:
        # 후기가 비어있지 않은 것만 골라냄
        reviews = df[df['후기'].astype(str).str.strip() != ""]
        
        if not reviews.empty:
            # 최신순으로 3개만 보여주거나, 랜덤으로 보여줌
            recent_reviews = reviews.tail(3).iloc[::-1] # 최신 3개 역순
            
            r_col1, r_col2, r_col3 = st.columns(3)
            
            # 후기 카드를 예쁘게 보여줌
            for idx, row in enumerate(recent_reviews.itertuples()):
                # 내용이 너무 길면 자르기
                short_review = row.후기[:50] + "..." if len(str(row.후기)) > 50 else row.후기
                
                # HTML로 예쁜 카드 만들기
                card_html = f"""
                <div class="review-card">
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <div class="review-text">"{short_review}"</div>
                    <div class="review-info">{row.현장명} 고객님<br>({row.시공내용})</div>
                </div>
                """
                
                if idx % 3 == 0: r_col1.markdown(card_html, unsafe_allow_html=True)
                elif idx % 3 == 1: r_col2.markdown(card_html, unsafe_allow_html=True)
                else: r_col3.markdown(card_html, unsafe_allow_html=True)
                
        else:
            st.info("아직 등록된 후기가 없습니다. 첫 번째 주인공이 되어주세요!")
    else:
        st.info("후기 데이터를 불러오는 중입니다...")

    st.divider()
    
    st.subheader("왜 마이홈케어플러스인가요?")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><div class="feature-title">첨단 장비 정밀 탐지</div><div class="feature-text">청음식/가스식 최신 장비 보유.<br>미세한 누수까지 찾아냅니다.</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><div class="feature-icon">🛡️</div><div class="feature-title">책임 시공 보장</div><div class="feature-text">누수 원인을 못 찾으면<br>비용을 일절 받지 않습니다.</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feature-card"><div class="feature-icon">🚀</div><div class="feature-title">부산 전 지역 긴급출동</div><div class="feature-text">해운대, 수영, 동래 어디든<br>빠르게 달려갑니다.</div></div>', unsafe_allow_html=True)

# === [나머지 메뉴들 (생략 - 기존과 동일)] ===
elif menu == "서비스 소개":
    st.header("🛠️ 마이홈케어플러스 전문 시공")
    st.write("부산/경남 대표 홈케어! 아래 모든 항목을 직접 시공합니다.")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💧 누수 & 방수 전문")
        st.markdown('<div class="service-box"><b>1. 누수 출장 점검</b><br>- 정확한 원인 파악 및 전문가 소견서 발급</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>2. 누수 탐지 (책임 시공)</b><br>- 청음식/가스식 첨단 장비 보유<br>- 못 찾으면 비용 0원!</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>3. 욕실 방수 공사</b><br>- 철거부터 방수, 타일 마감까지 원스톱 해결</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>4. 외부 창틀 로프 코킹</b><br>- 아파트 베란다 빗물 누수 완벽 차단 (로프 작업)</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>5. 욕조 배수구 교체</b><br>- 욕조 파손 없이 배수구만 교체하는 특수 기술</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("🛁 생활 설비 & 인테리어")
        st.markdown('<div class="service-box"><b>6. 도배 (실크/합지)</b><br>- 부분 도배부터 전체 도배까지 깔끔한 마감</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>7. 각종 수전(수도꼭지) 교체</b><br>- 주방, 세면대, 샤워기, 베란다 수전 등</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>8. 양변기 교체</b><br>- 치마형, 투피스 등 최신 도기 설치 및 폐기물 처리</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>9. 샤워기 설치</b><br>- 해바라기 샤워기, 선반형 샤워기 설치</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>10. 환풍기 교체</b><br>- 힘 쎈 환풍기, 댐퍼형(냄새 차단) 환풍기 교체</div>', unsafe_allow_html=True)

elif menu == "시공 갤러리":
    st.header("✨ 시공 전/후 비교")
    try: image_comparison(img1="before.jpg", img2="after.jpg", label1="Before", label2="After", width=700, in_memory=True)
    except: st.error("사진 파일 필요")

elif menu == "출장 지역":
    st.header("📍 출장 가능 지역")
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    folium.Circle(location=[35.1796, 129.0756], radius=20000, color="red", fill=True, fill_opacity=0.1).add_to(m)
    st_folium(m, width=800, height=500)

elif menu == "견적 문의":
    calculator.show_estimate()

# === [관리자 모드 (후기 입력 기능 추가!)] ===
elif menu == "🔒 관리자 모드":
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        tab1, tab2, tab3 = st.tabs(["📝 블로그 글쓰기", "📊 시공 장부 (매출)", "🖼️ 사진 워터마크"])
        
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
            st.subheader("📊 마이홈케어 매출 현황")
            df = load_data()
            if not df.empty and '금액' in df.columns:
                try:
                    df['금액'] = df['금액'].astype(str).str.replace(',', '').astype(int)
                    total_revenue = df['금액'].sum()
                    count_work = len(df)
                    m1, m2 = st.columns(2)
                    m1.metric("💰 누적 총 매출", f"{total_revenue:,}원")
                    m2.metric("🔨 총 시공 건수", f"{count_work}건")
                    st.divider()
                    st.write("📋 **최근 시공 내역** (엑셀 내용)")
                    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
                except: st.dataframe(df)
            else: st.info("아직 데이터가 없습니다.")

            st.divider()
            
            # [기존 기능 + 후기 입력칸 추가]
            st.write("✍️ **새로운 매출 & 후기 입력하기**")
            with st.form("sheet_form"):
                date = st.date_input("날짜")
                s_place = st.text_input("현장명 (예: 좌동 벽산아파트)")
                s_work = st.text_input("시공 내용")
                s_price = st.number_input("받은 금액 (원)", step=10000)
                s_note = st.text_input("비고 (자재비 등)")
                
                # [여기가 핵심!] 후기 입력칸
                st.markdown("---")
                s_review = st.text_input("💬 고객 후기 (홈페이지 메인에 노출됩니다!)", placeholder="예: 사장님이 너무 친절하고 꼼꼼하게 봐주셨어요!")
                
                submit_sheet = st.form_submit_button("💾 장부에 저장하기")
                
                if submit_sheet:
                    with st.spinner("엑셀에 적는 중..."):
                        # 후기(s_review)까지 같이 저장!
                        if add_to_sheet(date, s_place, s_work, s_price, s_note, s_review):
                            st.success(f"✅ 저장 완료! {s_price}원 입력됨.")
                        else:
                            st.error("저장 실패. (엑셀에 '후기' 열을 만드셨나요?)")
                            
        with tab3:
            st.subheader("📸 사진 도장 찍기 (워터마크)")
            uploaded_file = st.file_uploader("사진 파일을 드래그하거나 클릭해서 올리세요", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                default_text = "마이홈케어플러스 010-6533-3137"
                watermark_text = st.text_input("들어갈 문구", value=default_text)
                if st.button("도장 쾅! 찍기"):
                    with st.spinner("열심히 도장 찍는 중..."):
                        final_img, img_bytes = watermarker.add_watermark(uploaded_file, watermark_text)
                        st.success("완성! 아래 버튼을 눌러 다운로드하세요.")
                        st.image(final_img, caption="워터마크 적용된 사진", use_container_width=True)
                        st.download_button(label="💾 완성된 사진 다운로드", data=img_bytes, file_name=f"watermarked_{uploaded_file.name}", mime="image/jpeg")