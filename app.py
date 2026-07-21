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
                    model = genai.GenerativeModel('gemini-1.5-pro') 
                    
                    prompt = f"""
                    다음은 '{keyword}'에 대해 구글 검색에서 방금 수집한 최신 정보야:
                    {collected_info}
                    
                    위 정보를 바탕으로 네이버나 블로그스팟에서 사람들이 클릭하고 싶게 만드는 매력적인 블로그 포스팅을 작성해 줘.
                    인사말, 서론, 본론(구체적 정보), 결론 구조를 갖추고 가독성 좋게 이모지와 함께 작성해 줘.
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
