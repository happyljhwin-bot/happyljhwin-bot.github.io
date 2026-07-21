import streamlit as st

# 1. 홈페이지 기본 설정 (항상 최상단에 위치)
st.set_page_config(page_title="나만의 콘텐츠 사령부", page_icon="🚀", layout="wide")

# 2. 비밀번호 확인 함수 정의
def check_password():
    """사용자가 올바른 비밀번호를 입력했는지 확인합니다."""
    
    # 세션 상태에 비밀번호 인증 여부가 없다면 기본값(False)으로 설정
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # 이미 인증을 통과했다면 True 반환
    if st.session_state["password_correct"]:
        return True

    # 인증을 통과하지 못했다면 비밀번호 입력 폼을 보여줌
    st.title("🔒 사령부 접근 권한 확인")
    
    # 비밀번호 입력 창 (type="password"로 설정하여 입력값이 별표로 보임)
    pwd_attempt = st.text_input("비밀번호를 입력하세요:", type="password")
    
    if st.button("접속"):
        # st.secrets를 통해 클라우드에 안전하게 저장된 비밀번호와 비교
        # (로컬 테스트를 위해 잠시 하드코딩된 비밀번호 '1234'로 테스트할 수도 있습니다)
        # 배포 시에는 st.secrets["admin_password"] 를 사용합니다.
        
        # 현재는 로컬 테스트 및 배포 직전이므로, 임시로 "my_password123!"을 사용합니다.
        # 추후 클라우드 배포 시 이 부분을 st.secrets["password"] 로 변경할 것입니다.
        if pwd_attempt == "my_password123!": 
            st.session_state["password_correct"] = True
            st.rerun() # 화면 새로고침하여 메인 화면으로 이동
        else:
            st.error("비밀번호가 틀렸습니다.")
            
    return False

# 3. 메인 로직 실행
# 비밀번호가 맞을 때만 아래의 사령부 화면이 그려집니다.
if check_password():
    # ------------------- 여기서부터 진짜 사령부 화면 -------------------
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
            keyword = st.text_input("💡 메인 키워드:")
            search_button = st.button("정보 수집 및 글 작성 시작")
            
        with col2:
            st.subheader("실시간 작업 결과")
            if search_button and keyword:
                st.write(f"'{keyword}' 검색 중...")
                st.write("제미나이 API 대기 중...")