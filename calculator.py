import streamlit as st

def show_estimate():
    st.header("💰 3초 예상 견적")
    st.write("원하시는 시공을 선택하시면 대략적인 금액 범위를 알려드립니다.")
    
    # 1. 스타일 설정 (깔끔한 박스 디자인)
    st.markdown("""
        <style>
        .price-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
            color: #1E3A8A;
            border: 2px solid #1E3A8A;
            margin-bottom: 20px;
        }
        .warning-text {
            color: #d32f2f;
            font-weight: bold;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. 입력 화면
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            work_type = st.selectbox("시공 종류 선택", [
                "누수 출장 점검",
                "누수 탐지 (공사 별도)",
                "욕실 방수 공사",
                "외부 창틀 로프 코킹",
                "욕조 배수구 교체",
                "도배 (실크/합지)",
                "수전(수도꼭지) 교체",
                "양변기 교체",
                "샤워기 교체",
                "환풍기 교체"
            ])
        with col2:
            # 평수가 필요한 항목일 때만 슬라이더가 의미가 있음
            size = st.slider("평수 (아파트 공급면적 기준)", 10, 60, 32)
            
    # 3. 가격 계산 로직 (사장님이 불러주신 단가표 반영)
    min_price = 0
    max_price = 0
    note = "" # 추가 설명 (자재비 별도 등)

    if work_type == "누수 출장 점검":
        min_price = 50000
        max_price = 100000
        note = "※ 단순 점검 및 소견서 발급 비용입니다."
        
    elif work_type == "누수 탐지 (공사 별도)":
        min_price = 400000
        max_price = 600000
        note = "※ 탐지 장비를 사용하는 정밀 탐지 비용입니다. (못 찾으면 0원)"

    elif work_type == "욕실 방수 공사":
        min_price = 1500000
        max_price = 2500000
        note = "※ 철거 범위와 방수 공법에 따라 비용이 달라집니다."

    elif work_type == "외부 창틀 로프 코킹":
        # 평당 17,000원 계산
        price_per_pyeong = 17000
        calc_price = size * price_per_pyeong
        min_price = calc_price
        max_price = calc_price
        note = f"※ {size}평 기준 예상 견적입니다. (작업 난이도에 따라 변동)"

    elif work_type == "욕조 배수구 교체":
        min_price = 150000
        max_price = 200000
        note = "※ 욕조 측면 타공이나 절단이 필요할 수 있습니다."

    elif work_type == "도배 (실크/합지)":
        # 32평 기준 190만원 -> 평당 약 6만원 꼴로 역산해서 계산
        # (단순 계산을 위해 32평일 때 190만원이 나오도록 설정)
        base_rate = 2000000 / 32 
        calc_price = int(base_rate * size)
        
        # 도배는 변수가 많으므로 범위를 조금 넓게 잡음 (±10%)
        min_price = int(calc_price * 0.9 / 10000) * 10000 
        max_price = int(calc_price * 1.1 / 10000) * 10000
        note = f"※ {size}평 전체 도배 기준 (짐 유무, 벽지 종류에 따라 변동)"

    elif work_type == "수전(수도꼭지) 교체":
        min_price = 50000
        max_price = 100000
        note = "※ 설치 인건비 기준 (제품 구매 비용 별도)"

    elif work_type == "양변기 교체":
        min_price = 100000
        max_price = 150000
        note = "※ 설치 인건비 및 폐기물 처리 포함 (제품 구매 비용 별도)"

    elif work_type == "샤워기 교체":
        min_price = 800000
        max_price = 150000
        note = "※ 해바라기 샤워기 등 특수 제품 설치비 (제품 비용 별도)"

    elif work_type == "환풍기 교체":
        min_price = 70000
        max_price = 120000
        note = "※ 설치 인건비 기준 (제품 비용 별도)"

    # 4. 결과 출력 버튼
    if st.button("견적 확인하기"):
        st.markdown(f"""
            <div class="price-box">
                예상 비용: {min_price:,}원 ~ {max_price:,}원
            </div>
        """, unsafe_allow_html=True)
        
        if note:
            st.info(note)
            
        st.divider()
        st.markdown("""
            <div class='warning-text'>
            ⚠️ 주의사항 (필독)<br>
            1. 위 견적은 예상 금액이며, 현장 상황과 작업 여건에 따라 실제 비용은 달라질 수 있습니다.<br>
            2. '설치비' 항목은 제품(자재) 가격이 포함되지 않은 순수 시공비입니다.<br>
            3. 엘리베이터 없는 고층, 야간 작업 등 특수 상황은 추가 비용이 발생할 수 있습니다.
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("📞 **상세 견적 문의: 010-6533-3137**")