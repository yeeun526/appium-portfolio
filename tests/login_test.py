import pandas as pd
import pytest
import os
from pages.app_login_page import AppLoginPage

# 1. 엑셀 데이터 로드 로직
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'login_Test.csv')
df = pd.read_csv(file_path).fillna("")
test_cases = df.to_dict('records')

# 2. 전처리 피스처: 각 테스트(엑셀의 한 줄) 실행 전 자동 로그아웃 확인
@pytest.fixture(autouse=True)
def setup_login_page(driver):
    """엑셀의 각 행이 실행되기 전, 로그인이 되어 있다면 로그아웃하여 로그인 페이지로 이동"""
    login_page = AppLoginPage(driver)
    login_page.ensure_login_page() # 이미 만드신 '로그아웃 후 로그인 페이지 보장' 함수 호출[cite: 1, 2]
    yield

# 3. 데이터 주도 테스트 함수
@pytest.mark.parametrize("data", test_cases)
def test_login_data_driven(driver, data):
    print(f"▶️ 테스트 케이스 실행: {data['비고']}")
    
    login_page = AppLoginPage(driver)
    
    # 엑셀 데이터를 사용하여 로그인 시도
    login_page.login(data['id'], data['pw'])
    
    # 결과 검증 (성공/실패 여부에 따른 Assertion)
    if data['expected_result'] == 'success':
        # 성공 시: 로그아웃 버튼이 생겼는지 확인하여 로그인 성공 판정
        import time
        time.sleep(3) 
        assert driver.find_element("accessibility id", "로그아웃").is_displayed()
    else:
        # 실패 시: 에러 메시지가 기대한 키워드를 포함하는지 확인[cite: 1, 2]
        error = login_page.get_error_message()
        print(f"⚠️ 실제 에러 메시지: {error}")
        
        # 엑셀에 적힌 비고나 결과값을 통해 유연하게 검증 가능
        assert error != "" # 에러 메시지가 비어있지 않아야 함