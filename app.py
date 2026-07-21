import streamlit as st
import google.generativeai as genai
import requests

# 1. 홈페이지 기본 설정
st.set_page_config(page_title="나만의 콘텐츠 사령부", page_icon="🚀", layout="wide")

# 2. 비밀 금고에서 암호와 API 키 불러오기
ADMIN_PASSWORD = st.secrets["admin_password"]
GEMINI_API_KEY = st.secrets["gemini_key"]
SERPAPI_KEY = st.secrets["serpapi_key"]

# 3. 비밀번호 확인 로직
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔒 사령부 접근 권한 확인")
    pwd_attempt = st.text_input("비밀번호를 입력하세요:", type="password")
    
    if st.button("접속"):
        if pwd_attempt == ADMIN_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")
    return False

# 4. 메인 사령부 화면 및 1번 에이전트 작동
if check_password():
    st.sidebar.title("🛠️ 자동화 메뉴")
    menu = st.sidebar.radio(
        "작업을 선택하세요:",
        ["1. 블로그 포스팅 (정보 수집기)", "2. 인스타 카드뉴스", "3. 유튜브 쇼츠 대본"]
    )

    st.title("🚀 자동화 수익 파이프라인 대시보드")
    st.markdown("---")

    if menu == "1. 블로그 포스팅 (정보 수집기)":
        st.header("📝 1번 에이전트: 트렌드 정보 수집 및 블로그 작성")
        
        # 💡 [신규 추가된 부분] 플랫폼별 작성 지침 설정 창
        with st.expander("⚙️ 플랫폼별 작성 지침 (가이드라인) 설정", expanded=True):
            st.info("💡 네이버 블로그, 구글 블로그 등 타겟에 맞춰 아래 규칙을 자유롭게 수정하고 추가하세요.")
            blog_guideline = st.text_area(
                "📝 현재 적용된 작성 지침 (자유롭게 수정 가능):",
                value="1. 말투: 이웃과 대화하듯 친근하고 공감하는 말투 (~했어요, ~랍니다, ~네요) 사용.\n2. 가독성: 모바일 화면을 고려하여 2~3문장마다 반드시 줄바꿈할 것.\n3. 구조: 시선을 끄는 제목 -> 공감 가는 서론 -> 구체적인 본론 -> 행동을 유도하는 결론(댓글/공감 유도) 순으로 작성.\n4. 꾸미기: 문단마다 내용에 어울리는 이모지를 적절히 배치할 것.\n5. 금지사항: AI가 쓴 것처럼 보이는 딱딱한 번역투('~에 대해 알아보겠습니다' 등) 절대 금지.",
                height=180
            )
        
        st.markdown("---")

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("검색 설정")
            keyword = st.text_input("💡 메인 키워드 (예: 최신 국내 여행지, 맛집 등):")
            search_button = st.button("정보 수집 및 글 작성 시작")
            
        with col2:
            st.subheader("실시간 작업 결과")
            if search_button and keyword:
                try:
                    # [단계 1] SerpAPI로 구글 검색 정보 긁어오기
                    st.info(f"🔍 구글에서 '{keyword}' 관련 최신 정보를 수집 중입니다...")
                    search_url = f"https://serpapi.com/search.json?q={keyword}&hl=ko&gl=kr&api_key={SERPAPI_KEY}"
                    response = requests.get(search_url)
                    search_data = response.json()
                    
                    # 검색 결과에서 요약 텍스트만 추출
                    snippets = [item.get("snippet", "") for item in search_data.get("organic_results", [])]
                    collected_info = " ".join(snippets)
                    st.success("✅ 정보 수집 완료! AI가 분석하여 블로그 글을 작성합니다...")
                    
                    # [단계 2] 제미나이(Gemini) AI로 블로그 글 자동 작성
                    genai.configure(api_key=GEMINI_API_KEY)
                    model = genai.GenerativeModel('models/gemini-3.5-flash')

                    # 💡 [프롬프트 수정된 부분] 위에서 설정한 지침(blog_guideline)을 AI에게 전달
                    prompt = f"""
                    다음은 '{keyword}'에 대해 구글 검색에서 방금 수집한 최신 정보야:
                    {collected_info}
                    
                    위 정보를 바탕으로 블로그 포스팅을 작성해 줘. 
                    단, 아래의 [특별 작성 지침]을 무조건 엄격하게 지켜서 작성해야 해!
                    
                    [특별 작성 지침]
                    {blog_guideline}
                    """
                    
                    result = model.generate_content(prompt)
                    st.markdown("### ✨ 완성된 블로그 포스팅")
                    st.write(result.text)
                    
                except Exception as e:
                    error_msg = str(e)
                    # API 크레딧 고갈(429 에러) 발생 시 대처 안내
                    if "429" in error_msg or "prepayment credits are depleted" in error_msg:
                        st.error("🚨 제미나이 API 호출 한도 초과(429 에러): 결제 크레딧이 모두 소진되었습니다. AI Studio(https://ai.studio/projects)에서 결제 상태와 잔여 크레딧을 확인해 주세요.")
                    else:
                        st.error(f"오류가 발생했습니다: {error_msg}")
