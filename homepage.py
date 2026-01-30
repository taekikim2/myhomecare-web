# === [관리자 모드 (최종_완성_진짜_마지막.ver)] ===
elif menu == "🔒 관리자 모드":
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        # 탭이 4개로 늘어났습니다! (QR코드 추가)
        tab1, tab2, tab3, tab4 = st.tabs(["📝 블로그 글쓰기", "📊 시공 장부 (매출)", "🖼️ 사진 워터마크", "📱 QR코드 생성"])
        
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
                    st.write("📋 **최근 시공 내역**")
                    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
                except: st.dataframe(df)
            else: st.info("아직 데이터가 없습니다.")
            st.divider()
            st.write("✍️ **새로운 매출 & 후기 입력하기**")
            with st.form("sheet_form"):
                date = st.date_input("날짜")
                s_place = st.text_input("현장명")
                s_work = st.text_input("시공 내용")
                s_price = st.number_input("받은 금액 (원)", step=10000)
                s_note = st.text_input("비고")
                st.markdown("---")
                s_review = st.text_input("💬 고객 후기 (홈페이지 메인 노출)", placeholder="예: 사장님 최고!")
                submit_sheet = st.form_submit_button("💾 장부에 저장하기")
                if submit_sheet:
                    with st.spinner("저장 중..."):
                        if add_to_sheet(date, s_place, s_work, s_price, s_note, s_review):
                            st.success(f"✅ 저장 완료! {s_price}원 입력됨.")
                        else: st.error("저장 실패")
                            
        with tab3:
            st.subheader("📸 사진 도장 찍기 (워터마크)")
            uploaded_file = st.file_uploader("사진 파일을 드래그하거나 클릭해서 올리세요", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                default_text = "마이홈케어플러스 010-6533-3137"
                watermark_text = st.text_input("들어갈 문구", value=default_text)
                if st.button("도장 쾅! 찍기"):
                    with st.spinner("도장 찍는 중..."):
                        final_img, img_bytes = watermarker.add_watermark(uploaded_file, watermark_text)
                        st.success("완성! 다운로드하세요.")
                        st.image(final_img, caption="결과물", use_container_width=True)
                        st.download_button(label="💾 다운로드", data=img_bytes, file_name=f"watermarked_{uploaded_file.name}", mime="image/jpeg")

        # [NEW] 4번째 탭: QR코드 생성기
        with tab4:
            st.subheader("📱 홈페이지 QR코드 만들기")
            st.write("명함이나 작업 차량에 붙일 QR코드를 생성합니다.")
            
            # 사장님이 바꾼 예쁜 주소를 여기에 입력하게 합니다
            my_url = st.text_input("우리 홈페이지 주소 (https:// 포함)", "https://myhomecare-plus.streamlit.app")
            
            if st.button("QR코드 생성하기"):
                # 별도 설치 없이 구글 차트 API를 활용해서 즉석 생성 (가장 간편!)
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={my_url}"
                st.image(qr_url, caption="📷 핸드폰으로 찍어보세요!", width=300)
                st.markdown(f"**[Tip]** 위 이미지를 마우스 오른쪽 클릭 -> '이미지 저장' 하셔서 명함집에 보내시면 됩니다.")